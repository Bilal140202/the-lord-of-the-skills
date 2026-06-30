# Cookbook — the referee for the fleet framework you already run

> You don't adopt DOS *instead of* LangGraph, CrewAI, AutoGen, or an Agents SDK —
> you bolt the referee onto the one in production. Every orchestrator has a
> **believe-the-agent point**: the place a worker's "done" is folded into control
> flow as if it were a fact, and the place parallel workers touch shared files with
> no admission check. These recipes find that point in each framework and route it
> through a kernel verdict instead. **No framework swap, no rewrite — one function
> at one seam.**

Each recipe is the same two moves wearing that framework's clothes:

1. **`verify` at the "done" seam** — wherever the framework consumes a completion
   claim (a conditional edge, a termination condition, an output guardrail, a task
   callback), ask `dos.oracle.is_shipped` instead of reading the agent's message.
2. **`arbitrate` at the dispatch seam** — before the framework starts a worker on a
   file region, ask `dos.arbiter.arbitrate` whether that region is free.

The DOS side is identical everywhere (it's the [Python cookbook](cookbook-python-api.md)'s
Recipe 1 + 3); only the bind point changes. Honesty labels (this repo's own
discipline): every snippet marked **ran** had its DOS-bearing seam *executed* on
2026-06-10 against the shipped package and the framework version named — the
worker side is scripted, no model behind it, because the *control flow* is what's
being demonstrated. What was **not** run here is a full agent loop with a live
LLM; the seam behavior is what these recipes claim, and that part is witnessed.

> **Runnable form.** Recipes 0–4 also live as executable files under
> [`../fleet_frameworks/`](../fleet_frameworks/), pinned by
> `tests/test_fleet_framework_examples.py` — Recipe 0 runs in every suite run;
> each framework recipe runs wherever its framework is installed (and skips
> cleanly where it isn't). So the seams below are re-executed by CI, not just
> pasted here.

---

## Recipe 0 — the universal pattern (framework-free) · **ran**

Two functions. Everything below is one of these, relocated:

```python
import dos
from dos import oracle, arbiter

cfg = dos.default_config("/path/to/repo")   # or config.load_workspace_config(repo)

def verified_done(plan: str, phase: str) -> bool:
    """An agent SAID it shipped (plan, phase). Ask git, not the agent."""
    return oracle.is_shipped(plan, phase, cfg=cfg).shipped

def admit(lane: str, tree: list[str], live_leases: list[dict]):
    """May a worker start on this file region without colliding?"""
    return arbiter.arbitrate(
        requested_lane=lane, requested_kind="cluster",
        requested_tree=tree, live_leases=live_leases, config=cfg,
    )
```

Output of the full runnable version (a throwaway repo with one real
`AUTH1: …` commit), run 2026-06-10 against `dos-kernel` v0.21.0:

```
verified_done('AUTH', 'AUTH1') = True
verified_done('AUTH', 'AUTH2') = False
verdict detail: shipped=True source=grep-subject sha=f0d01bc
admit api (no leases): acquire -> api
admit api (api held):  refuse - all concurrent cluster lanes are held by live loops — no free lane to auto-pick. Wait for one to finish, then re-invoke.
```

That's the whole adapter. A `verified_done` that returns `False` means *no
artifact backs the claim* — the agent's cheerful "all work completed!" never
enters into it.

The verify half also ships pre-wrapped: `dos.verified` is this same gate as a
decorator / context manager, so a code path *cannot run* on an unverified claim
instead of remembering to check
([Python cookbook Recipe 8](cookbook-python-api.md)):

```python
from dos import verified

@verified("AUTH", "AUTH2", workspace="/path/to/repo")
def publish():   # raises NotShippedError until git evidence says AUTH2 shipped
    ...
```

## Recipe 1 — LangGraph: a referee node + a verdict-routed edge · **ran**

**The believe-the-agent point:** a conditional edge that routes on the worker
node's own output ("if the agent says done, go to END").

**The fix:** insert a `referee` node between the worker and the routing decision,
and make the conditional edge read the *verdict* field — which only the referee
writes, from git — never the worker's `report`:

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import dos
from dos import oracle

cfg = dos.default_config("/path/to/repo")

class FleetState(TypedDict):
    plan: str
    phase: str
    report: str      # what the agent SAYS (never trusted)
    verdict: str     # what git says (the only thing routed on)
    attempts: int

def worker(state: FleetState) -> dict:
    # your real agent node goes here — this one lies on purpose:
    return {"report": f"{state['phase']} is done — all work completed!",
            "attempts": state["attempts"] + 1}

def referee(state: FleetState) -> dict:
    v = oracle.is_shipped(state["plan"], state["phase"], cfg=cfg)
    return {"verdict": "SHIPPED" if v.shipped else "NOT_SHIPPED"}

def route(state: FleetState) -> str:
    if state["verdict"] == "SHIPPED":
        return "land"
    return "redispatch" if state["attempts"] < 2 else "give_up"

g = StateGraph(FleetState)
g.add_node("worker", worker)
g.add_node("referee", referee)
g.add_edge(START, "worker")
g.add_edge("worker", "referee")           # every "done" goes through the referee
g.add_conditional_edges("referee", route,
                        {"redispatch": "worker", "land": END, "give_up": END})
app = g.compile()
```

Run verbatim (langgraph 1.2.4, no LLM — the control flow is the demo), 2026-06-10:

```
dispatch on AUTH2 (nothing ever landed):
  worker said: 'AUTH2 is done — all work completed!'
  git says:    NOT_SHIPPED (via none)
  worker said: 'AUTH2 is done — all work completed!'
  git says:    NOT_SHIPPED (via none)
  -> final: NOT_SHIPPED after 2 attempt(s) — the lie never routed as done

dispatch on AUTH1 (a real commit backs it):
  worker said: 'AUTH1 is done — all work completed!'
  git says:    SHIPPED 1507b97 (via grep-subject)
  -> final: SHIPPED after 1 attempt(s) — landed on git's word, not the agent's
```

The worker claimed completion both times with identical confidence. Only the
claim git could back was allowed to end the run as done.

For the **dispatch seam**: call `admit(...)` (Recipe 0) in the node that fans out
parallel workers, and skip/queue any worker whose region comes back `refuse` —
same shape as the [Python cookbook Recipe 7](cookbook-python-api.md).

## Recipe 2 — CrewAI: a verify tool + a post-kickoff gate · **ran**

**The believe-the-agent point:** `crew.kickoff()` returns when the agents decide
they're finished; the `CrewOutput` is their narration of what happened.

**The fix** is two-layered. Give the agents the referee as a tool (so a
well-prompted agent can check itself mid-run), and — because a tool the agent
*may* call is advisory, not a gate — verify the claims yourself after `kickoff()`
returns, before anything downstream consumes them:

```python
from crewai.tools import tool
import dos
from dos import oracle

cfg = dos.default_config("/path/to/repo")

@tool("verify_shipped")
def verify_shipped(plan: str, phase: str) -> str:
    """Did (plan, phase) actually ship? Answered from git history, never from
    an agent's report. Returns SHIPPED or NOT_SHIPPED."""
    v = oracle.is_shipped(plan, phase, cfg=cfg)
    return f"SHIPPED via {v.source}" if v.shipped else "NOT_SHIPPED — no artifact backs this"

# ... agents=[Agent(..., tools=[verify_shipped]), ...] ...

result = crew.kickoff()
# the gate — independent of anything any agent said in `result`:
for plan, phase in dispatched_units:
    if not oracle.is_shipped(plan, phase, cfg=cfg).shipped:
        redispatch(plan, phase)   # the crew's "done" was not backed by git
```

The second layer is the one that holds: it reads zero bytes of crew output.

The tool itself, executed (crewai 1.14.6, 2026-06-10):

```
tool.run AUTH1 -> SHIPPED via grep-subject
tool.run AUTH2 -> NOT_SHIPPED — no artifact backs this
```

## Recipe 3 — AutoGen: a termination condition only git can satisfy · **ran**

**The believe-the-agent point:** AgentChat teams stop on conditions like
`TextMentionTermination("TERMINATE")` — i.e. *the run ends because an agent said
the magic word.* That is the cheap lie's favorite door: claiming done is exactly
how an agent ends a run it's stuck on.

**The fix:** a custom `TerminationCondition` that treats the magic word as a
*claim* and only actually stops the team when the oracle backs it:

```python
from autogen_agentchat.base import TerminationCondition, TerminatedException
from autogen_agentchat.messages import StopMessage
import dos
from dos import oracle

cfg = dos.default_config("/path/to/repo")

class ShippedTermination(TerminationCondition):
    """Stop only when (plan, phase) verifiably shipped — an agent saying
    'TERMINATE' is a claim, not a stop."""
    def __init__(self, plan: str, phase: str):
        self._plan, self._phase, self._done = plan, phase, False

    @property
    def terminated(self) -> bool:
        return self._done

    async def __call__(self, messages) -> StopMessage | None:
        if self._done:
            raise TerminatedException("already terminated")
        claims_done = any("TERMINATE" in str(getattr(m, "content", ""))
                          for m in messages)
        if claims_done and oracle.is_shipped(self._plan, self._phase, cfg=cfg).shipped:
            self._done = True
            return StopMessage(content="verified: shipped per git ancestry",
                               source="dos")
        return None        # claim unbacked (or no claim) — the run keeps going

    async def reset(self) -> None:
        self._done = False

# team = RoundRobinGroupChat(agents, termination_condition=ShippedTermination("AUTH", "AUTH2"))
```

Compose it with a budget stop (`ShippedTermination(...) | MaxMessageTermination(50)`)
so an honestly-stuck run still ends — refusing to *believe* "done" is not the same
as running forever.

The condition, executed against scripted messages (autogen-agentchat 0.7.5,
2026-06-10) — a lying `TERMINATE` on an unshipped phase returns `None` (the run
keeps going); the same word on a phase git backs returns the `StopMessage`:

```
lying TERMINATE on AUTH2  -> None (run keeps going)
honest TERMINATE on AUTH1 -> StopMessage(content='verified: shipped per git ancestry', source='dos')
composes with MaxMessageTermination via `|` (OrTerminationCondition)
```

## Recipe 4 — OpenAI Agents SDK: an output guardrail with a git tripwire · **ran**

**The believe-the-agent point:** the run ends when the agent produces a final
output; handoffs and downstream code consume that output as the result.

**The fix:** an `output_guardrail` whose tripwire is the oracle — a final answer
that claims a ship which git can't see trips the guardrail instead of landing:

```python
from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, output_guardrail
import dos
from dos import oracle

cfg = dos.default_config("/path/to/repo")

@output_guardrail
async def backed_by_git(ctx: RunContextWrapper, agent: Agent, output) -> GuardrailFunctionOutput:
    v = oracle.is_shipped(ctx.context.plan, ctx.context.phase, cfg=cfg)
    return GuardrailFunctionOutput(
        output_info={"verdict": "SHIPPED" if v.shipped else "NOT_SHIPPED",
                     "via": v.source},
        tripwire_triggered=not v.shipped,   # "done" with no artifact → trip
    )

worker = Agent(name="worker",
               instructions="Ship the phase, then report.",
               output_guardrails=[backed_by_git])
# Runner.run(...) now raises OutputGuardrailTripwireTriggered on an unbacked
# "done" — catch it and re-dispatch instead of consuming the claim.
```

The same module-level `verify_shipped` function from Recipe 2 also drops in as a
`@function_tool` if you want the agent able to *check itself* before answering.

The guardrail, executed directly (openai-agents 0.17.4, 2026-06-10):

```
guardrail on unbacked 'done' -> tripwire: True  {'verdict': 'NOT_SHIPPED', 'via': 'none'}
guardrail on backed 'done'   -> tripwire: False {'verdict': 'SHIPPED', 'via': 'grep-subject'}
```

## Recipe 5 — Claude Code / Claude Agent SDK: already first-class

Claude Code is DOS's most-worn integration — don't write an adapter, use the
shipped surfaces:

```bash
dos init --hooks claude-code   # the verdict wired into the host's own hook config
```

- **Hooks (enforcement):** a refused tool call is denied *before it runs*; a false
  "done" at Stop is refused. See [QUICKSTART](../../docs/QUICKSTART.md) and
  [docs/221](../../docs/221_the-cross-vendor-hook-installer.md).
- **MCP (advisory):** add `{ "command": "dos-mcp" }` to the host config and the
  agent gets `dos_verify` / `dos_arbitrate` as native tools — zero code. The same
  server works for any MCP host (Claude Desktop, Cursor, Cline, an Agent-SDK app).
- **The plugin:** [claude-plugin/](../../claude-plugin/README.md) bundles both plus
  the skills.

For the Claude **Agent SDK** specifically: point its hook config at the same
`dos hook` CLI the installer wires (the hook dialect is data — `--dialect
claude-code` is the default), or attach `dos-mcp` as an MCP server in
`ClaudeAgentOptions`. Cursor, Codex CLI, and Gemini CLI wire the same way with
their own dialect: `dos init --hooks <runtime>`.

## Swarm runtimes (Hermes / OpenClaw) — the deep worked example

For a persistent autonomous-swarm runtime, the integration is a two-function
adapter over the CLI (no `import dos` at all) plus the lease bracket around
shared-state writes. That one is built out as a full **offline, A/B-measured
example** with non-forgeable scoreboards: [`../hermes_integration/`](../hermes_integration/).

---

## Which seam, which syscall — the map

| Framework | The believe-the-agent point | The DOS bind | Verdict source |
|---|---|---|---|
| LangGraph | a conditional edge routing on the worker's output | a `referee` node + route on its verdict field | `oracle.is_shipped` |
| CrewAI | `kickoff()` returns the agents' narration | a `verify_shipped` tool + a post-kickoff gate | `oracle.is_shipped` |
| AutoGen | `TextMentionTermination("TERMINATE")` — saying it ends it | a `TerminationCondition` only git satisfies | `oracle.is_shipped` |
| OpenAI Agents SDK | the final output lands unexamined | an `output_guardrail` tripwire | `oracle.is_shipped` |
| Claude Code / Agent SDK | tool calls + Stop | shipped: `dos init --hooks`, `dos-mcp`, plugin | hooks + MCP |
| any of them, fanning out | N workers, one repo, no admission check | `admit(...)` before each dispatch | `arbiter.arbitrate` |

Three disciplines carry over from the kernel no matter the framework:

- **Route on the verdict, never the report.** Keep the agent's prose out of the
  branch condition entirely (Recipe 1's `verdict` vs `report` split).
- **A tool the agent may call is advisory.** It helps an honest agent self-check;
  it does not gate a dishonest one. The gate is the call *you* make at the seam
  the agent doesn't control (Recipe 2's second layer, Recipe 3, Recipe 4).
- **Pair every refusal-to-believe with a budget.** `verify` says NOT_SHIPPED
  forever on a run that's truly stuck — compose with attempt caps / message caps
  so honest failure still terminates (Recipes 1 and 3).

## Provenance — what ran, what didn't

| Recipe | Status on 2026-06-10 |
|---|---|
| 0 (universal) | **ran** — output above is verbatim (`dos-kernel` v0.21.0) |
| 1 (LangGraph) | **ran** — langgraph 1.2.4, full graph invoked, output verbatim |
| 2 (CrewAI) | **ran** — crewai 1.14.6, the tool executed; the post-kickoff gate is Recipe 0's tested call |
| 3 (AutoGen) | **ran** — autogen-agentchat 0.7.5, the condition called with scripted messages, both verdicts + the `\|` composition |
| 4 (OpenAI Agents) | **ran** — openai-agents 0.17.4, the guardrail invoked both ways |
| 5 (Claude Code) | shipped product surface — see the plugin's own verified-install witness |

What no recipe ran here: a live LLM driving the worker. The workers are scripted
*because the seam is the demo* — swap in your real agents; the referee doesn't
care who's lying to it.
