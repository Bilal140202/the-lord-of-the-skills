# WORKFLOW: OPTIMIZE PERFORMANCE (FULL SOURCE)

**Version:** Gold v1.1 (Master Merge)
**Layer:** 8 — Execution Workflow
**Tier:** 2 — Loaded by task
**File:** workflows/workflow-optimize-performance-SOURCE.md
**Primary Mode:** Performance
**Secondary Modes:** Debugger, Builder, Architect, Database, DevOps/Infra
**Purpose:** The systematic sequence for identifying and resolving performance bottlenecks — always measurement-first, never premature optimization. Prevents wasted effort on the wrong bottleneck and ensures complexity is only introduced where the gain is proven and worth the cost.
**Loaded When:** System is slow, latency is unacceptable, performance targets are not met, or proactive performance review is needed before scaling.
**Inherits From:** execution-workflow.md (universal process)

---

## WHAT THIS WORKFLOW DOES

This workflow enforces the cardinal rule of performance engineering:

### MEASURE FIRST. OPTIMIZE SECOND.

Without this workflow, developers optimize code that is not the bottleneck, add caching before understanding why queries are slow, and introduce complexity for unmeasurable improvements.

---

## ACTIVATION

### Operational Status

| Use When (Conditions) | Do NOT Use When (Anti-Patterns) |
| :--- | :--- |
| "This is slow" / Performance is degrading | Something is broken, not slow (use `workflow-debug-issue.md`) |
| Response time is too high / Latency spike | Code is messy but fast (use `workflow-refactor-module.md`) |
| "Why is this taking so long?" / "Where is the bottleneck?" | Building new features (use `workflow-build-feature.md`) |
| Query is slow / Page load is slow | General code review (use `workflow-review-code.md`) |
| Bundle too large / Core Web Vitals are poor | Speculative "let's optimize everything" |
| Proactive performance review before scaling | Correctness bug that incidentally mentions speed |

---

## REQUIRED FILES

### Skills — Always Load

| Priority | Skill | Why |
| :--- | :--- | :--- |
| Primary | `skill-performance` | Bottleneck identification, profiling methodology |
| Secondary | `skill-database` | Query optimization, indexing, connection management |

### Skills — Load When Relevant

| Condition | Skill |
| :--- | :--- |
| Code-level optimization needed | `skill-coding` |
| Architectural change needed for performance | `skill-architecture` |
| Infrastructure scaling needed | `skill-devops-infra` |
| Frontend rendering performance | `skill-ui-ux` |

### Contexts — Always Load

- `stack-context.md`
- `architecture-context.md`
- `database-context.md`

### Contexts — Load When Relevant

| Condition | Context |
| :--- | :--- |
| Frontend performance | `DESIGN.md` |
| API latency | `api-conventions.md` |
| Infrastructure bottleneck | `infra-context.md` |
| SLA requirements | `business-priorities.md` |
| Testing performance regression | `testing-standards.md` |

---

## REQUIRED INPUTS

At minimum, Anti-Gravity should have or establish before proceeding:

| Input Requirement | Description |
| :--- | :--- |
| **Symptom/Target** | Described performance symptom, target, or concern |
| **Affected Scope** | The affected path, module, endpoint, or operation |
| **External Environment** | Scale, traffic, and load assumptions |
| **Infrastructure** | Infrastructure and deployment assumptions |

### If inputs are incomplete

Do NOT jump straight into tuning. Instead:

1. Define the performance symptom precisely
1. Identify the most useful measurement still needed
1. State assumptions explicitly
1. Ask clarification only when missing information materially changes where the bottleneck is likely to be

---

## EXECUTION SEQUENCE

---

### STEP 1 — DEFINE THE PERFORMANCE PROBLEM

**Mode:** Performance
**Goal:** Quantify the problem. "It's slow" is a symptom, not a performance problem.

**CRITICAL RULE:** If you cannot measure the current performance with a number, you cannot optimize it. Get the number first.

#### Actions

1. **Quantify the current state:**
   - What specific operation is slow?
   - How slow is it — measured, not perceived?
   - What is the current latency: p50, p95, p99?
   - What is the current throughput?
   - Under what conditions does it degrade: load, data volume, time of day, specific inputs?
   - Is the issue user-visible, system-visible, cost-visible, or all three?

1. **Define the target:**
   - What is acceptable latency for this operation?
   - Check `database-context.md` query performance baselines
   - Check `business-priorities.md` for SLA requirements
   - Be specific: "p95 response time for sprint board load must be under 500ms"

1. **Quantify the gap:**

| Metric | Value |
| :--- | :--- |
| **Current** | [measured value] |
| **Target** | [required value] |
| **Gap** | [difference] |

1. **Assess impact:**
   - How many users are affected?
   - How frequently does this operation occur?
   - What is the business impact?

#### Output (Step 1)

| Field | Value |
| :--- | :--- |
| **Operation** | [what is slow] |
| **Current Performance** | [measured p50 / p95 / p99] |
| **Target** | [specific metric and threshold] |
| **Gap** | [difference] |
| **Impact** | [users affected, frequency, business consequence] |
| **Dimension** | [latency / throughput / memory / CPU / rendering / query time / contention] |

#### Gate (Step 1)

If the performance objective is still vague, optimization will become wasteful or misdirected. A vague target cannot be verified.

---

### STEP 2 — PROFILE AND IDENTIFY THE BOTTLENECK

**Mode:** Performance
**Goal:** Find WHERE the time is actually spent — not where you think it is spent.

**THE CARDINAL RULE: Optimizing a non-bottleneck produces zero improvement. Do NOT proceed to optimization until the bottleneck is identified with evidence.**

#### Request Path Trace

```text
Client request
  → Network
  → Server receive
  → Auth
  → Validation
  → Business logic
  → Database query or queries
  → Response formatting
  → Network
  → Client render
```

#### Segment Measurement

| Segment | How to Measure | Tool |
| :--- | :--- | :--- |
| Network latency | Browser DevTools Network tab | Chrome DevTools |
| Server processing time | Server-side timing logs | Custom middleware timer |
| Database query time | Query execution time | `EXPLAIN ANALYZE`, query logging |
| External API call time | Response time logging | Timing wrapper |
| Client rendering | Core Web Vitals, component profiler | Vercel Analytics, React DevTools |
| Total time | End-to-end request timing | Browser DevTools, custom timing |

#### Bottleneck Identification (Step 2)

1. **Dominant Segment:** Identify where >50% of total time is spent.
1. **Evidence Check:** If time is distributed evenly, rethink the architecture.

#### Deep Drill — Database

- Run `EXPLAIN ANALYZE` on the slow query
- Check: sequential scan versus index scan
- Check: number of rows scanned versus rows returned
- Check: join algorithms — nested loop, hash, merge
- Check `database-context.md` indexing strategy
- Check for N+1 query patterns — multiple queries where one suffices

#### Deep Drill — Frontend

- Check Core Web Vitals: LCP, FID or INP, CLS
- Check bundle size — is too much JavaScript being shipped?
- Check rendering performance — unnecessary re-renders?
- Check image sizes and loading strategy
- Check third-party script impact

#### Output (Step 2)

| Field | Value |
| :--- | :--- |
| **Bottleneck** | [specific segment] |
| **Time Consumed** | [X]ms of total [Y]ms |
| **Evidence** | [profiling data, query plan, trace] |
| **Bottleneck Type** | [compute / I/O / lock-contention / allocation / network / query-plan / rendering] |

#### Gate (Step 2)

If the bottleneck is still a guess, go back and gather stronger measurement. Never proceed to optimization on intuition alone.

---

### STEP 3 — GENERATE OPTIMIZATION OPTIONS

**Mode:** Performance
**Goal:** Produce multiple serious improvement paths targeted at the identified bottleneck.

### Only optimize the bottleneck. Nothing else.

#### Database Optimization Options

| Optimization | When to Apply | Tradeoff |
| :--- | :--- | :--- |
| **Add/Improve Index** | Sequential scan on index-eligible column | Slightly slower writes |
| **Optimize Query** | Unnecessary joins, suboptimal plan | May require raw SQL |
| **Add Pagination** | Returning too many rows | Client must handle pagination |
| **Denormalize** | Repeated expensive joins | Data duplication, complexity |
| **Pre-compute** | Expensive aggregation on every request | Stale data window |
| **Conn Pooling** | Connection overhead dominating | Infrastructure change |
| **Read Replica** | Read queries saturating primary | Cost, replication lag |

#### Application Optimization Options

| Optimization | When to Apply | Tradeoff |
| :--- | :--- | :--- |
| **Eliminate N+1** | Multiple sequential queries for related data | Larger single query |
| **Async/Background** | Slow operation blocking the response | User sees delayed result |
| **Caching** | Same expensive computation repeated | Invalidation complexity |
| **Algo Improvement** | O(n²) or worse in hot path | Code complexity |
| **Parallel Process** | Independent operations sequential | Error handling complexity |
| **Reduce Work** | Computing things never used | Behavior change risk |
| **Batching** | Many small operations | Coordination complexity |

#### Frontend Optimization Options

| Optimization | When to Apply | Tradeoff |
| :--- | :--- | :--- |
| **Code Splitting** | Large bundle, slow initial load | Transition loading states |
| **Image Opt** | Large unoptimized images | Build pipeline complexity |
| **Memoization** | Expensive re-renders | Memory usage, stale risk |
| **Virtualization** | Rendering long lists (100+) | Scroll behavior complexity |
| **Optimistic Update** | User waiting for server | Rollback complexity |
| **Server Components** | Data fetching in client components | Less interactivity |
| **Payload Reduction** | Over-fetching data from API | API contract change |

#### Comparative Output (Step 3)

Generate at least two options.

| Option | Expected Improvement | Effort | Tradeoff | Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Option A** | [estimate] | [L/M/H] | [what is sacrificed] | [correctness/ops] |
| **Option B** | [estimate] | [L/M/H] | [what is sacrificed] | [correctness/ops] |
| **Baseline** | Do nothing | N/A | Current pain persists | Low |

---

### STEP 4 — COMPARE OPTIONS AND CHOOSE

**Mode:** Performance
**Goal:** Choose the optimization that actually improves the real system.

#### Selection Strategy (Step 4)

1. **Smallest Gain Principle:** Prefer the smallest option that meaningfully improves the bottleneck.
1. **"Fast Enough" Rule:** Stop once the target is met.
1. **Tradeoff Audit:** Does it weaken the system (memory, staleness, complexity) disproportionately?

#### Output (Step 4)

| Selection | Detail |
| :--- | :--- |
| **Recommended Option** | [choice] |
| **Why it Wins** | [reasoning tied to bottleneck] |
| **Main Tradeoff** | [explicit accepted cost] |
| **Rejected Options** | [reason for rejection] |

---

### STEP 5 — IMPLEMENT THE OPTIMIZATION

**Mode:** Builder
**Goal:** Apply the chosen optimization surgically, one change at a time.

#### Implementation Pipeline (Step 5)

1. **Record Baseline:** Document current performance measurement exactly.
1. **Single Variable:** Implement ONE optimization at a time. No batching.
1. **Readable Performance:** Encapsulate complexity behind clean interfaces.
1. **Comment why, not just what:** Explain the optimization's rationale.

#### Gate (Step 5)

If correctness or maintainability is being traded away without explicit acknowledgment, the result is unsafe. State all accepted tradeoffs before delivery.

---

### STEP 6 — VERIFY THE IMPROVEMENT

**Mode:** Performance
**Goal:** Prove the optimization worked with measurements, not assumptions.

#### Verification Comparison (Step 6)

Measure again using the SAME method as Step 1.

| Metric | Before | After | Improvement | Target Met? |
| :--- | :--- | :--- | :--- | :--- |
| **p50 Latency** | [X]ms | [Y]ms | [Z]% | ✅ / ❌ |
| **p95 Latency** | [X]ms | [Y]ms | [Z]% | ✅ / ❌ |
| **p99 Latency** | [X]ms | [Y]ms | [Z]% | ✅ / ❌ |

#### Regression Checklist (Step 6)

- [ ] All tests pass
- [ ] No new errors in monitoring
- [ ] Other operations not degraded
- [ ] Memory usage stable
- [ ] Correctness preserved

#### Decision (Step 6)

- **Target met:** Deliver.
- **Target NOT met:** Check if the bottleneck shifted. If yes, Step 2. If no, Step 3.

---

### STEP 7 — DELIVER

**Mode:** Communicator
**Goal:** Communicate findings with evidence, tradeoffs, and monitoring guidance.

#### Delivery Structure (Step 7)

- **Problem:** Quantified with baseline.
- **Bottleneck:** Identified with evidence.
- **Optimization:** Rationale for choice.
- **Comparative Results Table** (p95, p50).
- **Accepted Tradeoffs** (Complexity, Memory, etc.).
- **Monitoring Guidance:** What metric/threshold to watch.

---

## CHECKPOINTS AND QUALITY GATES

| Gate | Condition | Action |
| :--- | :--- | :--- |
| **Gate 1 — Vague Problem** | Cannot define real metric or pain | Get measurement first |
| **Gate 2 — Weak Profile** | Evidence cannot localize bottleneck | Strengthen profiling |
| **Gate 3 — Intuition Tuning** | Win not visible in measurements | Gather evidence |
| **Gate 4 — ROI Check** | Complexity outweighs gain | Re-check tradeoff |
| **Gate 5 — Stealth Tradeoff** | Correctness traded silently | Stop. State tradeoffs. |
| **Gate 6 — Target Met** | Further work has diminishing returns | Stop. Target achieved. |

---

## WORKFLOW ANTI-PATTERNS

| Anti-Pattern | Why It Is Harmful | Workflow Prevention |
| :--- | :--- | :--- |
| **Tune-First** | Effort wasted on non-bottlenecks | Measure First (Step 1) |
| **Benchmark Vanity** | System unimproved for real users | Real-workload validation |
| **Complexity Creep** | Maintenance burden > Gain | "Fast Enough" Rule |
| **Tradeoff Denial** | Staleness/Memory surprises later | Explicit Tradeoff Delivery |
| **Non-Bottleneck Tuning** | Zero improvement in overall speed | Path Trace (Step 2) |

---

## FAILURE MODES AND ESCALATION PATHS

| Failure Mode | Symptom | Escalation |
| :--- | :--- | :--- |
| **Design Problem** | Symptoms caused by architecture | Switch to `workflow-plan-architecture.md` |
| **Infra Bound** | Local code cannot fix environment | Load `skill-devops-infra` |
| **Refactor Needed** | Optimization is non-local/trivial | Coordinate with `workflow-refactor-module.md` |
| **Misleading Data** | Benchmark doesn't reflect workload | Strengthen profiling realism |

---

## FINAL RULE

Optimize the measured bottleneck on the path that actually matters — not the code that merely looks expensive.

---

## VERSION HISTORY

| Version | Date | Changes |
| :--- | :--- | :--- |
| Gold v1.1 | Initial | Systematic sequence for identifying and resolving performance bottlenecks |
