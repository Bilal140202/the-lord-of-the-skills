# Playbook 00 — ship a non-coder verdict in 15 minutes

> **Goal:** a non-coder asked an agent to build a feature and was told "done."
> By the end of this playbook a developer has wired DOS so that person gets a
> **plain-English verdict** — "Probably yes" / "Not yet" — backed by what was
> actually built, not by what the agent *said*.

This is the smallest possible adoption move. No plan documents, no fleet, no
lanes — just the truth syscall with its non-coder renderer turned on. It works on
**any git repo**, because `verify` reads ground truth out of git history and
answers from that.

The scene: a product manager asked an agent to "add the `FOO1` feature." The
agent reported success. The PM can't read a diff and can't tell `via grep-subject`
from `via none`. A developer spends fifteen minutes making the kernel speak the
PM's language.

---

## Step 0 — install

```bash
pip install dos-kernel         # dist name is dos-kernel; `import dos` / `dos` cmd unchanged
# or, from a checkout:  pip install -e .
dos --help
```

> The bare PyPI name `dos` is an unrelated package — always install `dos-kernel`.

The kernel's only hard dependency is PyYAML. The plain-English renderer is
built in; nothing extra to install.

## Step 1 — point DOS at the repo

`cd` into the repo the agent worked in and scaffold the one policy file:

```bash
cd ~/code/the-product
dos init .
```

```text
wrote /home/you/code/the-product/dos.toml
derived 3 concurrent lane(s) (docs, src, tests) + an exclusive 'global'
DOS workspace initialised. Try:  dos doctor --workspace .
```

`dos init` reads your top-level directories and writes a `dos.toml` with a
sensible default lane taxonomy (here: `docs`, `src`, `tests` as concurrent
lanes, plus an exclusive `global`). For the non-coder verdict you don't have to
touch any of that — it's set up for the *fleet* features you may grow into later.
`verify` itself needs no plan, no lanes, nothing but git history.

## Step 2 — the developer-facing verdict (so you know what's underneath)

When the agent claims phase **`FOO1`** of the **`FOO`** workstream shipped, ask
the kernel. This is the normal, terse output a developer reads:

```bash
dos verify --workspace . FOO FOO1
```

```text
SHIPPED FOO FOO1 9b2d295 (via grep-subject)
```
```text
exit code: 0
```

`(via grep-subject)` means *"I found the `FOO1` token in a commit **subject** in
git history,"* and `9b2d295` is the commit that proves it. The verdict comes from
git ancestry, **not** from the agent saying "done." That's the whole point — but
it's still developer dialect. The PM can't read it.

## Step 3 — turn on the plain-English renderer

Add one flag: `--output plain`. Same verdict, rendered for someone who has never
opened a terminal before:

```bash
dos verify --workspace . --output plain FOO FOO1
```

```text
Probably yes: 'FOO1' looks like it was added, but the only sign is a note in the project history, not the built result itself. Worth opening it to confirm it's really there. (This checks that it's present, not that it works.)
```
```text
exit code: 0
```

Read that carefully — the verdict **hedges on purpose**, and the hedge is the
honesty discipline, not a bug. The only evidence here was a commit *subject* (the
`grep-subject` rung), which is the weakest rung the oracle has: a commit message
is a human-written note, not the built artifact. So the plain renderer says
"**Probably** yes ... the only sign is a note in the project history, not the
built result itself ... worth opening it to confirm." A stronger rung (a registry
entry, a verified build) would render a firmer "yes." The renderer **down-weights
weak evidence in plain words** — it never launders a thin signal into false
confidence. That is exactly the property you want a non-coder to feel.

## Step 4 — the honest "no"

Now ask about a phase the agent claimed but never actually committed — `FOO2`:

```bash
dos verify --workspace . --output plain FOO FOO2
```

```text
Not yet: 'FOO2' isn't in what was built. The agent may have said it was done, but it isn't in the project yet. Ask it to actually add 'FOO2', then check again.
```
```text
exit code: 1
```

This is the line that earns the fifteen minutes. The agent told the PM `FOO2` was
done; the kernel, reading git, says **"Not yet ... the agent may have said it was
done, but it isn't in the project yet."** The PM gets an actionable next step
("ask it to actually add `FOO2`, then check again") without ever reading code.

## Step 5 — the exit code a dev branches on

The English is for the human; the **exit code is for the script**. The same two
runs above carry the verdict in their exit status, so a developer can gate a
notification, a Slack message, or a CI step on it:

```bash
if dos verify --workspace . --output plain FOO FOO1; then
  echo "tell the PM: looks shipped"      # exit 0
else
  echo "tell the PM: not yet"            # exit 1
fi
```

`0` = shipped, `1` = not. **The exit code is the verdict** regardless of which
renderer you chose — `--output plain` changes only the words a human reads, never
the adjudication. So one command serves both audiences at once: the PM reads the
sentence, the pipeline reads the status.

## The three renderers — and a product's own wording

`--output` selects one of **three built-in renderers**, all rendering the *same*
verdict:

| `--output` | Audience | What it emits |
|---|---|---|
| `text` (default) | developer | terse: `SHIPPED FOO FOO1 9b2d295 (via grep-subject)` |
| `json` | a machine / another tool | the structured verdict object |
| `plain` | a non-coder | the full English sentence shown above |

If `plain`'s wording isn't quite your product's voice, you don't fork the kernel
— you register your **own** renderer as a `dos.renderers` entry point. The
skeleton under [`examples/dos_ext/`](../dos_ext/) ships a `friendly` renderer
exactly for this: `pip install` it and `--output friendly` becomes available
alongside the three built-ins, with your team's phrasing. (See
[`../dos_ext/`](../dos_ext/) and [HACKING.md](../../docs/HACKING.md) for the
entry-point map.)

## The one limit to say out loud

**`plain` tells the PM the feature is _present_, never that it is _correct_.**
Every renderer rides the same oracle, and the oracle's strongest claim is "this
phase is attributed as shipped in git history and is an ancestor of `HEAD`" — a
*presence* fact, not a *behaves-correctly* fact. The hedge in Step 3 even says so
in its own words: *"(This checks that it's present, not that it works.)"* Don't
let a "Probably yes" be heard as "the feature is correct." It means the work
landed; whether it does the right thing is still a question for a test, a review,
or a human opening it. Be honest about that with whoever reads the verdict — the
kernel is.

## What you have now

- A non-coder gets a plain-English ship verdict on demand — no terminal literacy
  required.
- The verdict is backed by git history, not by the agent's self-report.
- A developer branches on the same command's exit code (`0`=yes, `1`=no).
- The wording is swappable per product via a `dos.renderers` plugin.

## Where to go next

- **Onboard the repo properly** (stamp grammar, completeness check, lanes) →
  [`01_onboard-a-repo.md`](01_onboard-a-repo.md).
- **Add your own renderer wording** → [`../dos_ext/`](../dos_ext/) +
  [HACKING.md](../../docs/HACKING.md).
- **Put the verdict in CI** → [`cookbook-ci-integration.md`](cookbook-ci-integration.md).

---

### Recap — the commands

```bash
pip install dos-kernel                              # NOT `pip install dos` (that PyPI name is unrelated)
cd ~/code/the-product
dos init .                                          # scaffold dos.toml from the repo's dirs
dos verify --workspace . FOO FOO1                   # developer dialect:  SHIPPED ... (via grep-subject), exit 0
dos verify --workspace . --output plain FOO FOO1    # non-coder:  "Probably yes: ..."          exit 0
dos verify --workspace . --output plain FOO FOO2    # non-coder:  "Not yet: ..."               exit 1
```
