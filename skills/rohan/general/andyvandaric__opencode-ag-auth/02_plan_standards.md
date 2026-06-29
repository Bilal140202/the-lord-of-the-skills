## 📋 Implementation Plan Quality Standards

> [!IMPORTANT]
> **Target: 97%+ Confidence Score** before moving to Ready.
> Plans missing required sections will be rejected by user.

### Adaptive Plan Requirements

**Different tasks require different levels of detail:**

| Task Type | Required Sections | Test Requirements |
|-----------|-------------------|-------------------|
| **Feature (feat)** | Goal, Current State, Proposed Changes, Types, Verification | Unit tests + Manual checklist |
| **Bug Fix (bug)** | Bug Description, Root Cause, Fix, Regression Test | Test proving bug is fixed |
| **Phase/Epic** | All sections + Success Criteria Matrix | Comprehensive test suite |
| **Refactor** | Before/After, Migration Steps | Existing tests must pass |
| **Config/Trivial** | Can skip plan → Fast-track to Ready | Build verification only |

### Plan Template by Complexity

#### 🟢 Simple (bug fix, single-file change)
```markdown
# [Title]
> **Status**: 📝 PLANNING

## Bug/Issue
[What's broken]

## Root Cause
[Why it's broken]

## Fix
#### [MODIFY] `path/to/file.ext`
[Description of change]

## Verification
- [ ] Build passes
- [ ] Test: [specific test command]
```

#### 🟡 Medium (feature, multi-file)
```markdown
# [Title]
> **Status**: 📝 PLANNING
> **Confidence**: ~95%

## Goal
[What we're building and why]

## Current Architecture
[What already works - avoid duplicate effort]

## Proposed Changes

### Step 1: Backend
#### [NEW/MODIFY] `path/to/file.rs`
[code snippet]

### Step 2: Frontend
#### [NEW/MODIFY] `path/to/component.tsx`
[code snippet]

## Types
[typescript interface]

## Verification
- [ ] `cargo test --lib`
- [ ] Manual: [steps]
```

#### 🔴 Complex (phase, multi-component, architectural)
```markdown
# [Title]
> **Status**: 📝 PLANNING
> **Confidence**: ~97.5%
> **Parent**: [link to parent plan]

## Goal
[Comprehensive description]

## Current Architecture
| Component | Status | Location |
|-----------|--------|----------|
| ... | ✅/❌ | path |

## Proposed Changes

### Step 1: [Component A]
#### [NEW] `path/file.rs`
[rust code]

### Step 2: [Component B]
...

## Types
### Rust Types
[rust structs]

### TypeScript Types
[typescript interfaces]

## Integration Flow
| Action | Frontend | Backend |
|--------|----------|---------|
| ... | ... | ... |

## Verification Plan

### Success Criteria Matrix
| ID | Test Case | Expected | Type |
|----|-----------|----------|------|
| T1 | ... | ... | Unit |
| T2 | ... | ... | Integration |

### Automated Tests
#### [NEW] `tests/test_xxx.rs`
[test code]

### Manual Verification Checklist
| Step | Action | Expected | ✓ |
|------|--------|----------|---|
| M1 | ... | ... | ☐ |

## Completion Criteria
- [ ] `cargo test` → 0 failed
- [ ] Manual tests → All ✓
- [ ] `pnpm typecheck` → No errors
```

### Confidence Score Calculation

**Score per category (adjust weights by task type):**

| Category | Weight | Scoring |
|----------|--------|---------|
| Backend completeness | 30% | All functions defined with signatures |
| Frontend completeness | 30% | Components, types, state defined |
| Integration clarity | 25% | Clear flow between FE ↔ BE |
| Tests & Verification | 15% | Test scenarios with assertions |

**Confidence thresholds:**
- `< 90%`: Incomplete, needs more detail
- `90-96%`: Review with user, may need iteration
- `97%+`: Ready for approval ✅

### AI Planning Checklist

Before moving plan to Planned status, verify:

- [ ] **Goal is clear**: One sentence explaining the outcome
- [ ] **Current state documented**: What already works (avoid reimplementing)
- [ ] **All file changes listed**: `[NEW]`, `[MODIFY]`, `[DELETE]` tags
- [ ] **Code snippets included**: Signatures, structs, interfaces
- [ ] **Types defined**: Both Rust and TypeScript if cross-boundary
- [ ] **Integration flow**: Table showing FE → BE mapping
- [ ] **Tests specified**: At minimum, unit test stubs with assertions
- [ ] **Manual verification**: Checklist for UI/UX testing
- [ ] **Confidence score calculated**: Must be 97%+
