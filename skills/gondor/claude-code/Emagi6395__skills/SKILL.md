---
name: evo-search
description: >
  Solves complex, open-ended problems using an evolutionary search mechanism inspired by
  genetic algorithms. Generates a diverse population of candidate answers, scores them
  against a rubric, then iteratively applies selection, crossover, and mutation to breed
  progressively better solutions. Use this skill whenever the user wants to explore a
  solution space deeply, asks for the "best" answer to a subjective or multi-dimensional
  problem, wants to evaluate competing approaches and distill the strongest, or uses any
  of these triggers: "evolutionary search", "genetic algorithm", "evolve an answer",
  "breed solutions", "population-based search", or phrases like "give me multiple
  approaches and refine the best one". Also trigger when the problem is complex,
  open-ended, or has no obvious single correct answer and the user wants a high-quality,
  well-explored result, not just a quick response.
---

# Evo-Search

Runs a genetic-algorithm-style loop over candidate responses: generate a diverse initial population, score each against a rubric, then repeatedly select, crossover, and mutate to improve quality across generations. Output the top 3 final solutions.

---

## Step 0: Problem Intake & Rubric

Identify problem type, constraints, audience, and scope. If ambiguous, ask one question.

### Rubric Construction

Detect which mode applies:

| Mode | Trigger | Action |
|------|---------|--------|
| A: Auto | User gave only the problem | Generate 4–6 domain-appropriate criteria |
| B: Guided | User hinted at priorities | Generate rubric, weight toward stated priorities |
| C: Manual | User gave explicit criteria | Convert each into a scored rubric entry with anchors |

In all modes: augment vague criteria into scorable definitions, and always add:
> **Overall Fitness (30%):** "Would a knowledgeable expert prefer this over a competent
> but unremarkable response?" Scored holistically. Prevents narrow-criteria gaming.

**Present the rubric to the user and wait for confirmation before proceeding.**

Rubric format:
```
| Criterion      | Description              | Weight | Max |
|----------------|--------------------------|--------|-----|
| [Name]         | [Definition + anchors]   | X%     | 10  |
| Overall Fitness| Expert holistic score    | 30%    | 10  |
Weighted Total = Σ(score × weight)  [max = 10.00]
```

---

## Step 1: Initial Population

Generate **6 candidates** (default) using these diversity frames, one per candidate:

| # | Frame |
|---|-------|
| 1 | Conventional / mainstream |
| 2 | Contrarian / challenges assumptions |
| 3 | First-principles / bottom-up |
| 4 | Analogy-led / draws from another domain |
| 5 | Risk-focused / emphasizes what could go wrong |
| 6 | Synthesis / combines multiple angles |

Generate all candidates before scoring any. Then score each and display:

```
GENERATION 0
| # | Frame        | Fitness | Strength       | Weakness      |
|---|--------------|---------|----------------|---------------|
| 1 | Conventional | X.X     | [one phrase]   | [one phrase]  |
```

---

## Step 2: Evolution Loop

**Default: 5 iterations.** Repeat until stopping criteria are met.

### 2.1 Selection
Tournament selection: sample 2 candidates, keep the higher scorer. Repeat to get 4 parents.
Elitism: carry the top 2 candidates forward untouched every generation.

### 2.2 Crossover
Produce 4 offspring (pair parents: 1+2, 3+4, 1+3, 2+4). For each pair, synthesize a child
that inherits the key strength of each parent without their primary weaknesses. Rotate
crossover strategies across iterations (trait synthesis → section splice → schema inheritance).

### 2.3 Mutation
Apply mutation to each offspring with probability **0.2** (~1 of 4 offspring per generation).

| Mode | When to use | What to do |
|------|-------------|------------|
| Exploitative (~60%) | Offspring has a diagnosable weak criterion | Target and fix that specific criterion |
| Exploratory (~40%) | No clear weakness, or population is converging | Random perturbation: swap rhetorical stance, domain lens, level of abstraction, or target audience |

**Multi-feature mutation:** ~1 in 3 mutation events, mutate two features simultaneously.
Use when the population has converged for 2+ generations, two criteria score equally low,
or an exploratory mutation is being applied.

### 2.4 Evaluate & Merge
Score all offspring. Merge with current population. Keep top 6 by fitness score.
Elites from 2.1 are guaranteed to survive.

### 2.5 Convergence Check
If top 3 candidates are within 0.4 fitness of each other AND content is substantially
similar, inject 1–2 fresh randomly-framed candidates ("immigrants") before merging.

Display per-generation summary:
```
GENERATION [N]
| # | Origin        | Fitness | Δ   | Key Change         |
|---|---------------|---------|-----|--------------------|
| 1 | Elite         | X.X     | -   | -                  |
| 2 | Crossover A+B | X.X     | +Y  | [what changed]     |
Best: Candidate [N] (X.X)
```

---

## Stopping Criteria

Stop early if any condition is met:
- Max iterations reached (default: 5)
- Best fitness ≥ 9.0
- Best fitness improved less than 0.2 over 2 consecutive generations

Note the reason when stopping early.

---

## Step 3: Output

### 3.1 Contrast Table (show before full answers)
```
TOP 3 SOLUTIONS
| Rank | Score | Defining Strength    | Best Used When              |
|------|-------|----------------------|-----------------------------|
| #1   | X.X   | [one phrase]         | [context where #1 wins]     |
| #2   | X.X   | [one phrase]         | [context where #2 wins]     |
| #3   | X.X   | [one phrase]         | [context where #3 wins]     |
```

### 3.2 Full Solutions
Output the top `top_k` solutions in full (default: 3), labeled with rank and score.

### 3.3 Evolution Trace
```
EVOLUTION SUMMARY
| Generation | Best Fitness | Key Improvement     |
|------------|--------------|---------------------|
| 0 (init)   | X.X          | [note]              |
| ...        | ...          | ...                 |
Final: X.X / 10.0
```

### 3.4 Rubric Breakdown
Show per-criterion scores for the #1 solution only.

---

## Parameters

| Parameter      | Default      | Range                              | Effect                              |
|----------------|--------------|------------------------------------|-------------------------------------|
| population     | 6            | 4–10                               | Candidates per generation           |
| iterations     | 5            | 1–10                               | Evolution cycles                    |
| mutation_rate  | 0.2          | 0–1                                | Fraction of offspring mutated       |
| mutation_mode  | mixed        | exploitative / exploratory / mixed | Mutation strategy bias              |
| multi_mutation | occasional   | never / occasional / frequent      | How often 2 features mutate at once |
| elites         | 2            | 1–3                                | Candidates preserved each generation|
| top_k          | 3            | 1–5                                | Final solutions shown in full       |
| rubric_mode    | auto         | auto / guided / manual             | How the rubric is built             |
| show_trace     | true         | true / false                       | Show evolution summary              |

Users set parameters in plain language. Examples:
- *"Quick run, 3 iterations"* → iterations=3
- *"Large population, thorough search"* → population=8–10
- *"Be more exploratory"* → mutation_mode=exploratory
- *"Just show me the winner"* → top_k=1

---

## Scoring Guidance

Score honestly. A mediocre-but-coherent answer scores 5-6. Inflated scores destroy the selection signal and the algorithm stops working. The crossover step is where the most value is created. Synthesize genuine strengths; don't concatenate text.
