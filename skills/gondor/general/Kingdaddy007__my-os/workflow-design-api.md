# WORKFLOW: DESIGN API (FULL SOURCE)

**Version:** Gold v1.1 (Master Merge)
**Layer:** 8 — Execution Workflow
**Tier:** 2 — Loaded by task
**File:** workflows/workflow-design-api-SOURCE.md
**Primary Mode:** Architect
**Secondary Modes:** Security, Builder, Reviewer, Research
**Purpose:** The systematic sequence for designing API endpoints and contracts — from understanding the consumer's needs through contract definition to implementation with proper error handling, security, and documentation. Ensures APIs are designed from the consumer's perspective, not the database schema's perspective.
**Loaded When:** Creating new API endpoints, redesigning existing APIs, defining contracts between services, evaluating API design decisions, or preparing an API design for implementation or review.
**Inherits From:** execution-workflow.md (universal process)

---

## WHAT THIS WORKFLOW DOES

This workflow enforces contract-first design, consistent conventions, backward compatibility, and proper error handling.

Without this workflow, APIs tend to leak internal implementation details, use inconsistent patterns, create breaking changes that frustrate consumers, and collapse all failure classes into one vague response that clients cannot act on.

---

## ACTIVATION

### Use When

- "Design this API"
- "Create an endpoint for [functionality]"
- "What should this endpoint look like?"
- "How should the request and response be shaped?"
- "How should we version this?"
- "What should the error format be?"
- "REST versus GraphQL?"
- "How should this data be exposed?"
- Adding new server-accessible functionality
- Defining contracts between frontend and backend
- Designing webhook payloads
- Evolving an existing contract

### Do NOT Use When

- Building UI that consumes existing API → use `workflow-build-feature.md` or `workflow-design-ui.md`
- Reviewing existing API code → use `workflow-review-code.md`
- Optimizing slow endpoints → use `workflow-optimize-performance.md`
- Broad architecture planning where API shape is secondary → use `workflow-plan-architecture.md`
- Implementing already-finalized endpoints only → use `workflow-build-feature.md` with API design as supporting skill

---

## REQUIRED FILES

### Skills — Always Load

| Priority | Skill | Why |
| :--- | :--- | :--- |
| Primary | `skill-api-design` | Contract design, versioning, error handling |
| Secondary | `skill-security` | Auth, input validation, data exposure |
| Secondary | `skill-architecture` | Boundary placement and system fit |

### Skills — Load When Relevant

| Condition | Skill |
| :--- | :--- |
| API involves new queries/schema | `skill-database` |
| API introduces new boundaries | `skill-architecture` (deep) |
| Consumer task is unclear | `skill-product-thinking` |
| Contract needs implementation | `skill-coding` |
| Reviewing existing API quality | `skill-review-audit` |

### Contexts — Always Load

- `api-conventions.md`
- `stack-context.md`
- `security-baselines.md`
- `coding-standards.md`
- `architecture-context.md`
- `domain-rules.md`

### Contexts — Load When Relevant

| Condition | Context |
| :--- | :--- |
| New queries or schema needed | `database-context.md` |
| Business logic in responses | `domain-rules.md` |
| New module boundaries | `architecture-context.md` (deep load) |
| Business impact of API | `business-priorities.md` |
| Project consumer details | `project-context.md` |

---

## REQUIRED INPUTS

At minimum, Anti-Gravity should have or establish before proceeding:

- a stated or inferable consumer goal
- who or what will call this API
- what system boundary the API belongs to
- what trust or auth boundaries matter
- whether this is a new API, extension, compatibility-sensitive modification, or protocol-selection problem

### If inputs are incomplete

Do NOT jump straight into endpoint naming. Instead:

1. Restate the likely consumer task
1. State assumptions explicitly
1. Ask clarification only when missing information would materially change contract shape or compatibility risk

---

## EXECUTION SEQUENCE

---

### STEP 1 — UNDERSTAND THE CONSUMER

**Mode:** Architect
**Goal:** Design from the consumer's needs, not from the database schema. The contract should serve the consumer's task.

**Gate:** If the consumer task is still vague, do not lock contract shape yet.

#### Consumer Audit (Step 1)

1. **Identify the consumer:**
   - Who or what will call this API? Our own frontend, third-party, another service?
   - Internal consumer, partner-facing, or public?
   - What data does the consumer need? What do they NOT need?

#### Operational Inventory (Step 1)

1. **Map Actions:**
   - What actions does the consumer need to perform? (CRUD or Custom)
   - What is the frequency of each operation?
   - Identify the contract type: resource-oriented, operation-oriented, event/webhook.

#### Implementation Decision (Step 1)

**Decide: Server Action or API Route?**

| Criterion | Server Action | API Route |
| :--- | :--- | :--- |
| Called from our UI | ✅ Preferred | Only if Action insufficient |
| External clients | ❌ Never | ✅ Required |
| Webhooks | ❌ Never | ✅ Required |
| Needs versioning | ❌ N/A | ✅ For external stability |
| File upload | ❌ Limited | ✅ Better multipart |
| Streaming | ❌ Limited | ✅ Supported |

#### Output (Step 1)

```text
Consumer: [who calls this and from where]
Task: [what they are trying to accomplish]
Desired outcome: [what changes for them]
Contract type: [resource / operation / event]
API type decision: [Server Action / API Route and reason]
```

---

### STEP 2 — DEFINE THE CONTRACT

**Mode:** Architect
**Goal:** Define the exact API contract before writing any implementation. The contract IS the specification.

### Contract-first. Always.

**Gate:** Review the contract with the consumer BEFORE implementing.

#### Path & Schema Definition (Step 2)

1. **Structure URLs:** Per `api-conventions.md` (Plural nouns, Path IDs, kebab-case).
1. **Define Request:** Required fields, type constraints, validation (Zod).

#### Response Standards (Step 2)

Define the response shape per `api-conventions.md`:

```json
// Single resource
{ "data": { ... } }

// Collection
{ "data": [...], "pagination": { "page": 1, "limit": 20, "total": 145 } }

// Mutation success
{ "data": { ... }, "message": "Success" }

// Error
{ "error": { "code": "...", "message": "...", "details": [...] } }
```

#### Mapping & Field Audit (Step 2)

1. **Explicit Fields:** List every field, type, and optional status. CamelCase in JSON.

#### Error Taxonomy (Step 2)

| Scenario | Status | Error Code |
| :--- | :--- | :--- |
| Invalid input | 400 | VALIDATION_ERROR |
| Unauthenticated | 401 | UNAUTHORIZED |
| Unauthorized | 403 | FORBIDDEN |
| Not found | 404 | NOT_FOUND |
| Logic violation | 422 | BUSINESS_RULE_VIOLATION |
| Rate limited | 429 | RATE_LIMITED |
| Server error | 500 | INTERNAL_ERROR |

#### Output (Step 2)

Complete API contract (URLs, Methods, Request/Response Schemas, Error Modes, Pagination).

---

### STEP 3 — GROUND THE CONTRACT IN CONTEXT

**Mode:** Architect
**Goal:** Place the API inside the current system and project reality.

#### Environmental Audit (Step 3)

1. **Context Sync:**
   - Load relevant context files
   - Identify where the contract sits in the architecture
   - Inspect existing conventions from `api-conventions.md`
   - Identify compatibility obligations (if evolving)
   - Identify security or data ownership sensitivities

#### Output (Step 3)

```text
Boundary location: [where in the architecture]
Relevant constraints: [list]
Compatibility obligations: [list]
Existing conventions to follow: [list]
Protocol assumptions: [decided / assumed / open]
```

---

### STEP 4 — DESIGN THE DATA FLOW

**Mode:** Architect
**Goal:** Map how data flows from the API endpoint to the database and back. Document side effects explicitly.

#### Pipeline Sequence (Step 4)

```text
Request received
  → Authenticate (auth() helper)
  → Validate input (Zod schema)
  → Authorize (role + resource ownership)
  → Execute logic
  → Query/Mutate DB
  → Format response (transform shape)
  → Return
```

#### MappingSide Effects (Step 4)

1. **Document Consequences:** Notifications, Background jobs, Cache updates, Audit logs, External calls.

#### Performance Check (Step 4)

1. **Audit Complexity:** Joins, N+1 risks, Indexing needs, Caching potential.

#### Output (Step 4)

```text
Processing pipeline: [confirm sequence]
Data transformation: [DB shape -> Response shape]
Side effects: [complete list]
Performance notes: [indexing, caching]
```

---

### STEP 5 — EVALUATE AUTH, SECURITY, AND RISKS

**Mode:** Security
**Goal:** Make auth and error behavior explicit. Identify hidden secondary risks.

#### Access Control (Step 5)

1. **Strict Auth:**
   - Authenticate before any data access
   - Authorization checked for role AND resource ownership
   - Roles match `security-baselines.md` matrix
   - No bypass paths

#### Safety Protocols (Step 5)

1. **Inbound Data:** Server-side Zod validation, file safety (type/size), SQLi prevention.
1. **Outbound Data:** No sensitive fields, no internal leak in 500 errors.

#### Evolution Strategy (Step 5)

1. **Manage Change:**
   - Prefer additive evolution (new optional fields)
   - Define what constitutes a "Breaking Change"
   - Versioning strategy (now vs deferred)

#### Output (Step 5)

```text
Auth requirements: [sequence and rules]
Sensitive field rules: [blacklist]
Non-functional risks: [performance, integrity, abuse]
Compatibility strategy: [additive / versioned]
```

---

### STEP 6 — IMPLEMENT

**Mode:** Builder
**Goal:** Build the endpoint following the defined contract exactly.

#### Validation First (Step 6)

1. **Create Schemas:**

   ```typescript
   // features/[feature]/schemas/[action]Schema.ts
   export const createResourceSchema = z.object({ ... });
   ```

#### Build Pipeline (Step 6)

1. **Follow Step 4 Pipeline:** Authenticate → Validate → Authorize → Execute → Return.

#### Error & Pagination (Step 6)

1. **Handle Cases:** Map every contract error to an explicit handler. Never return raw error objects.
1. **Apply Pagination:** Follow `api-conventions.md` list patterns.

#### Testing Protocol (Step 6)

1. **Verify Coverage:** Happy path, Validation failures, Auth/Authz failures, Not Found, Business rules, Pagination edge cases.

---

### STEP 7 — VERIFY

**Mode:** Reviewer
**Goal:** Confirm the implementation matches the contract exactly and meets security requirements.

#### Compliance Checklist (Step 7)

- [ ] URL follows convention
- [ ] HTTP Method is correct
- [ ] Response shape matches contract (data envelope, camelCase)
- [ ] Error status codes/shapes match Step 2
- [ ] Auth happens before Data access
- [ ] Authorization checks Ownership
- [ ] Transactions used for atomic writes
- [ ] No internal leaks in 500 errors

---

### STEP 8 — DELIVER

**Mode:** Communicator
**Goal:** Communicate the API design clearly for review and maintenance.

#### Delivery Structure (Step 8)

```markdown

## API Endpoint Summary

### Endpoint

[METHOD] [URL]

### Request/Response

[Schemas with examples]

### Auth & Permissions

[Roles and Ownership rules]

### Side Effects & Flow

[Pipeline and secondary consequences]

### Compatibility

[Additive rules and breaking risk areas]
```

---

## CHECKPOINTS AND QUALITY GATES

| Gate | Condition | Action |
| :--- | :--- | :--- |
| Gate 1 — Task vague | Consumer goal not mapped | Do not lock contract |
| Gate 2 — Implementation Leak | API mirrors DB schema/internals | Redesign around consumer task |
| Gate 3 — Auth/Failure vague | Protected paths not explicitly mapped | Contract incomplete |
| Gate 4 — Implementation First | Code exists before contract is reviewed | Stop. Document contract first. |

---

## WORKFLOW ANTI-PATTERNS

| Anti-Pattern | Why It Is Harmful | Workflow Prevention |
| :--- | :--- | :--- |
| Storage-First Design | Consumers inherit DB constraints | Start with Consumer Job (Step 1) |
| Weak Failure Story | Clients cannot distinguish logic errors | Define error codes explicitly (Step 2) |
| Casual Breaking | Trust in the interface collapses | Preserve additive evolution |
| Code as Specification | Inconsistencies spread unreviewed | Contract-first discipline |

---

## FINAL RULE

Design the contract for the consumer and for future change — not for the convenience of the current implementation. Contract-first. Always.

---

## VERSION HISTORY

| Version | Date | Changes |
| :--- | :--- | :--- |
| Gold v1.1 | Initial | Established the systematic sequence for API contract design and implementation |
