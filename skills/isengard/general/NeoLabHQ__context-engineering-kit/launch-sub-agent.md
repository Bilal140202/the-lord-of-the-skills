# launch-sub-agent

This command launches a focused sub-agent to execute the provided task. Analyze the task to intelligently select the optimal model and agent configuration, then dispatch a sub-agent with Zero-shot Chain-of-Thought reasoning at the beginning and mandatory self-critique verification at the end. It implements the **Supervisor/Orchestrator pattern** from multi-agent architectures where you (the orchestrator) dispatch focused sub-agents with isolated context. The primary benefit is **context isolation** - each sub-agent operates in a clean context window focused on its specific task without accumulated context pollution.

## Usage

```bash
`/launch-sub-agent Design a caching strategy for our API that handles 10k requests/second`
```

Agent output:

```markdown
**Analysis:**
- Task type: Architecture / design
- Complexity: High (performance requirements, system design)
- Output size: Medium (design document)
- Domain match: software-architect

**Selection:** Opus + software-architect agent

**Dispatch:** Task tool with Opus model, software-architect prompt, CoT prefix, critique suffix
```

## Advanced Options

**Explicit Model Override**

When you know the appropriate model tier, override automatic selection:

```bash
/launch-sub-agent "Task description" --model opus|sonnet|haiku
```

**Explicit Agent Selection**

Force use of a specific specialized agent:

```bash
/launch-sub-agent "Task description" --agent developer|researcher|software-architect|tech-writer|business-analyst|code-explorer|tech-lead|security-auditor
```

**Output Location**

Specify where results should be written:

```bash
/launch-sub-agent "Task description" --output path/to/output.md
```

**Combined Options**

```bash
/launch-sub-agent "Implement the payment flow" --agent developer --model opus --output src/services/payment.ts
```

## Core design principles

- **Context isolation**: Sub-agents operate with fresh context, preventing confirmation bias and attention scarcity
- **Intelligent model selection**: Match model capability to task complexity for optimal quality/cost tradeoff
- **Specialized agent routing**: Domain experts handle domain-specific tasks
- **Zero-shot CoT**: Systematic reasoning at task start improves quality by 20-60%
- **Self-critique**: Verification loop catches 40-60% of issues before delivery

## When to use this command

- Tasks that benefit from fresh, focused context
- Tasks where model selection matters (quality vs. cost tradeoffs)
- Delegating work while maintaining quality gates
- Single, well-defined tasks with clear deliverables

## When NOT to use

- Simple tasks you can complete directly (overhead not justified)
- Tasks requiring conversation history or accumulated session context
- Exploratory work where scope is undefined

## Theoretical Foundation

**Zero-shot Chain-of-Thought** (Kojima et al., 2022)

- Adding "Let's think step by step" improves reasoning by 20-60%
- Explicit reasoning steps reduce errors and catch edge cases
- Reference: [Large Language Models are Zero-Shot Reasoners](https://arxiv.org/abs/2205.11916)

**Constitutional AI / Self-Critique** (Bai et al., 2022)

- Self-critique loops catch 40-60% of issues before delivery
- Verification questions force explicit quality checking
- Reference: [Constitutional AI](https://arxiv.org/abs/2212.08073)

**Multi-Agent Context Isolation** (Multi-agent architecture patterns)

- Fresh context prevents accumulated confusion and attention scarcity
- Focused tasks produce better results than context-polluted sessions
- Supervisor pattern enables quality gates between delegated work
