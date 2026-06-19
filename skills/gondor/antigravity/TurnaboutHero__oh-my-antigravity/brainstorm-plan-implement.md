---
description: Brainstorm → Plan → Implement workflow
---

# Brainstorm → Plan → Implement Workflow

## Overview

Structured workflow for feature development from idea to implementation.

## Stages

### Stage 1: Brainstorm (Oracle + Strategist)

**Goal**: Generate ideas and evaluate approaches

**Activities**:
- Understand requirements
- Identify constraints
- Propose multiple solutions
- Evaluate trade-offs

**Output**: Recommendation document

**Example**:
```markdown
## Feature: Real-time Notifications

### Approaches Considered

1. **WebSockets**
   - Pros: True real-time, bidirectional
   - Cons: Requires persistent connection
   
2. **Server-Sent Events (SSE)**
   - Pros: Simpler, HTTP-based
   - Cons: One-way only
   
3. **Long Polling**
   - Pros: Works everywhere
   - Cons: Less efficient

### Recommendation: WebSockets
Rationale: Need bidirectional for chat feature
```

### Stage 2: Plan (Prometheus)

**Goal**: Create detailed implementation plan

**Activities**:
- Break down into tasks
- Identify dependencies
- Assign agents
- Estimate effort

**Output**: Execution plan

**Example**:
```markdown
## Implementation Plan: WebSocket Notifications

### Tasks

1. **Backend Setup** (CodeSmith)
   - Install ws library
   - Create WebSocket server
   - Implement connection handling
   - Effort: 3 hours

2. **Client Integration** (Pixel)
   - WebSocket client wrapper
   - Reconnection logic
   - UI notification component
   - Effort: 4 hours

3. **Authentication** (SecurityGuard)
   - Token-based auth
   - Connection verification
   - Effort: 2 hours

4. **Testing** (Tester + Playwright-Master)
   - Unit tests
   - Integration tests
   - E2E connection tests
   - Effort: 3 hours

### Dependencies
- Task 3 must complete before Task 1
- Tasks 1 & 2 can run parallel
- Task 4 after all others
```

### Stage 3: Implement (Multi-Agent)

**Goal**: Execute the plan

**Activities**:
- CodeSmith implements backend
- Pixel builds frontend
- SecurityGuard ensures security
- Tester validates
- Git Master commits atomically

**Output**: Working feature

**Execution**:
```
[Parallel Track 1: Backend]
  SecurityGuard → Design auth flow
  CodeSmith → Implement WebSocket server
  CodeSmith → Add auth middleware
  Tester → Write server tests

[Parallel Track 2: Frontend]
  Pixel → Create WebSocket wrapper
  Pixel → Build notification UI
  Tester → Write client tests
  Playwright-Master → E2E tests

[Integration]
  Tester → Integration tests
  Debugger → Fix connection issues
  
[Finalization]
  Scribe → Update documentation
  Git Master → Atomic commits
```

## Usage

```
/workflow brainstorm-plan-implement: add real-time notifications
```

Or with ultrawork:
```
ulw workflow brainstorm-plan-implement: refactor authentication
```

## Success Criteria

- [ ] All agents completed their tasks
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Code committed
- [ ] No TODOs remaining

---

*"Ideas are easy. Implementation is hard. Planning makes it easier."*
