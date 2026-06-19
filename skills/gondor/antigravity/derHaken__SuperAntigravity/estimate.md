---
name: estimate
description: name: estimate
---
# Estimate

Development estimates for tasks, features, or projects.

## Estimation Process
1. Break the work into discrete components
2. For each component, estimate: design + implementation + testing + integration
3. Apply complexity multipliers for unknowns and dependencies
4. State confidence level and key assumptions

## Complexity Factors
- **Simple** (hours): Well-understood, existing patterns, clear scope
- **Medium** (days): Some unknowns, new patterns, multiple components
- **Complex** (weeks): Significant unknowns, architectural decisions, cross-cutting concerns

## Output Format
For each component:
- **Component name**
- **Estimate**: X hours/days
- **Confidence**: high / medium / low
- **Key assumptions**: what must be true for this estimate to hold
- **Risks**: what could make this take longer

**Total**: Sum + buffer for integration and unexpected issues

## Buffer Guidelines
- High confidence: 20% buffer
- Medium confidence: 50% buffer
- Low confidence: 100% buffer (or break down further before estimating)

## What Estimates Are NOT
Estimates are not commitments. They're informed guesses.
State your confidence. State your assumptions. Update when you learn more.
