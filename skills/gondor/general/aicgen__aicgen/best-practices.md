# Best Practices

# Planning Best Practices

## Plan Before Implementation

**ALWAYS design and plan before writing code:**

1. **Understand Requirements**
   - Clarify the goal and scope
   - Identify constraints and dependencies
   - Ask questions about ambiguous requirements

2. **Break Down Into Phases**
   - Divide work into logical phases
   - Define deliverables for each phase
   - Prioritize phases by value and dependencies

3. **Design First**
   - Sketch architecture and data flow
   - Identify components and interfaces
   - Consider edge cases and error scenarios

4. **Get User Approval**
   - Present the plan to stakeholders
   - Explain trade-offs and alternatives
   - Wait for approval before implementation

## Never Make Assumptions

**CRITICAL: When in doubt, ASK:**

```typescript
// ❌ BAD: Assuming what user wants
async function processOrder(orderId: string) {
  // Assuming we should send email, but maybe not?
  await sendConfirmationEmail(orderId);
  // Assuming payment is already captured?
  await fulfillOrder(orderId);
}

// ✅ GOOD: Clarify requirements first
// Q: Should we send confirmation email at this stage?
// Q: Is payment already captured or should we capture it here?
// Q: What happens if fulfillment fails?
```

**Ask about:**
- Expected behavior in edge cases
- Error handling strategy
- Performance requirements
- Security considerations
- User experience preferences

## Plan in Phases

**Structure work into clear phases:**

### Phase 1: Foundation
- Set up project structure
- Configure tooling and dependencies
- Create basic types and interfaces

### Phase 2: Core Implementation
- Implement main business logic
- Add error handling
- Write unit tests

### Phase 3: Integration
- Connect components
- Add integration tests
- Handle edge cases

### Phase 4: Polish
- Performance optimization
- Documentation
- Final review

**Checkpoint after each phase:**
- Demo functionality
- Get feedback
- Adjust plan if needed

## Planning Template

```markdown
## Goal
[What are we building and why?]

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Questions for Clarification
1. [Question about requirement X]
2. [Question about edge case Y]
3. [Question about preferred approach for Z]

## Proposed Approach
[Describe the solution]

## Phases
1. **Phase 1**: [Description]
   - Task 1
   - Task 2

2. **Phase 2**: [Description]
   - Task 1
   - Task 2

## Risks & Mitigation
- **Risk**: [Description]
  **Mitigation**: [How to handle]

## Alternatives Considered
- **Option A**: [Pros/Cons]
- **Option B**: [Pros/Cons]
- **Chosen**: Option A because [reason]
```

## Communication Principles

1. **Ask Early**: Don't wait until you're stuck
2. **Be Specific**: "Should error X retry or fail immediately?"
3. **Propose Options**: "Would you prefer A or B?"
4. **Explain Trade-offs**: "Fast but risky vs. Slow but safe"
5. **Document Decisions**: Record what was decided and why

## Anti-Patterns

❌ **Don't:**
- Start coding without understanding requirements
- Assume you know what the user wants
- Skip the planning phase to "save time"
- Make architectural decisions without discussion
- Proceed with unclear requirements

✅ **Do:**
- Ask questions when requirements are vague
- Create a plan and get it approved
- Break work into reviewable phases
- Document decisions and reasoning
- Communicate early and often


---

# Documentation Organization

## Keep Root Clean

**RULE: Documentation must NOT clutter the project root.**

```
❌ BAD: Root folder mess
project/
├── README.md
├── ARCHITECTURE.md
├── API_DOCS.md
├── DEPLOYMENT.md
├── TROUBLESHOOTING.md
├── USER_GUIDE.md
├── DATABASE_SCHEMA.md
├── TESTING_GUIDE.md
└── ... (20 more .md files)

✅ GOOD: Organized structure
project/
├── README.md              (overview only)
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── deployment/
│   └── guides/
└── src/
```

## Documentation Structure

**Standard documentation folder:**

```
docs/
├── architecture/
│   ├── overview.md
│   ├── decisions/         # Architecture Decision Records
│   │   ├── 001-database-choice.md
│   │   └── 002-api-design.md
│   └── diagrams/
│
├── api/
│   ├── endpoints.md
│   ├── authentication.md
│   └── examples/
│
├── guides/
│   ├── getting-started.md
│   ├── development.md
│   ├── deployment.md
│   └── troubleshooting.md
│
├── features/              # Organize by feature
│   ├── user-auth/
│   │   ├── overview.md
│   │   ├── implementation.md
│   │   └── testing.md
│   ├── payments/
│   └── notifications/
│
└── planning/              # Active work planning
    ├── memory-lane.md     # Context preservation
    ├── current-phase.md   # Active work
    └── next-steps.md      # Backlog
```

## Memory Lane Document

**CRITICAL: Maintain context across sessions**

### Purpose
When AI context limit is reached, reload from memory lane to restore working context.

### Structure

```markdown
# Memory Lane - Project Context

## Last Updated
2024-12-10 15:30

## Current Objective
Implementing user authentication system with OAuth2 support

## Recent Progress
- ✅ Set up database schema (2024-12-08)
- ✅ Implemented user registration (2024-12-09)
- 🔄 Working on: OAuth2 integration (2024-12-10)
- ⏳ Next: Session management

## Key Decisions
1. **Database**: PostgreSQL chosen for ACID compliance
2. **Auth Strategy**: OAuth2 + JWT tokens
3. **Session Store**: Redis for performance

## Important Files
- `src/auth/oauth.ts` - OAuth2 implementation (IN PROGRESS)
- `src/models/user.ts` - User model and validation
- `docs/architecture/decisions/003-auth-system.md` - Full context

## Active Questions
1. Should we support refresh tokens? (Pending user decision)
2. Token expiry: 1h or 24h? (Pending user decision)

## Technical Context
- Using Passport.js for OAuth
- Google and GitHub providers configured
- Callback URLs: /auth/google/callback, /auth/github/callback

## Known Issues
- OAuth redirect not working in development (investigating)
- Need to add rate limiting to prevent abuse

## Next Session
1. Fix OAuth redirect issue
2. Implement refresh token rotation
3. Add comprehensive auth tests
```

### Update Frequency
- Update after each significant milestone
- Update before context limit is reached
- Update when switching between features

## Context Reload Strategy

**For AI Tools with Hooks:**

Create a hook to reload memory lane on startup:

```json
{
  "hooks": {
    "startup": {
      "command": "cat docs/planning/memory-lane.md"
    }
  }
}
```

**For AI Tools with Agents:**

Create a context restoration agent:

```markdown
# Context Restoration Agent

Task: Read and summarize current project state

Sources:
1. docs/planning/memory-lane.md
2. docs/architecture/decisions/ (recent ADRs)
3. git log --oneline -10 (recent commits)

Output: Concise summary of where we are and what's next
```

## Feature Documentation

**Organize by feature/scope, not by type:**

```
❌ BAD: Organized by document type
docs/
├── specifications/
│   ├── auth.md
│   ├── payments.md
│   └── notifications.md
├── implementations/
│   ├── auth.md
│   ├── payments.md
│   └── notifications.md
└── tests/
    ├── auth.md
    └── payments.md

✅ GOOD: Organized by feature
docs/features/
├── auth/
│   ├── specification.md
│   ├── implementation.md
│   ├── api.md
│   └── testing.md
├── payments/
│   ├── specification.md
│   ├── implementation.md
│   └── providers.md
└── notifications/
    ├── specification.md
    └── channels.md
```

**Benefits:**
- All related docs in one place
- Easy to find feature-specific information
- Natural scope boundaries
- Easier to maintain

## Planning Documents

**Active planning should be in docs/planning/:**

```
docs/planning/
├── memory-lane.md         # Context preservation
├── current-sprint.md      # Active work
├── backlog.md             # Future work
└── spike-results/         # Research findings
    ├── database-options.md
    └── auth-libraries.md
```

## Documentation Principles

1. **Separate folder**: All docs in `docs/` directory
2. **Organize by scope**: Group by feature, not document type
3. **Keep root clean**: Only README.md in project root
4. **Maintain memory lane**: Update regularly for context preservation
5. **Link related docs**: Use relative links between related documents

## README Guidelines

**Root README should be concise:**

```markdown
# Project Name

Brief description

## Quick Start
[Link to docs/guides/getting-started.md]

## Documentation
- [Architecture](docs/architecture/overview.md)
- [API Docs](docs/api/endpoints.md)
- [Development Guide](docs/guides/development.md)

## Contributing
[Link to CONTRIBUTING.md or docs/guides/contributing.md]
```

**Keep it short, link to detailed docs.**

## Anti-Patterns

❌ **Don't:**
- Put 10+ markdown files in project root
- Mix documentation types in same folder
- Forget to update memory lane before context expires
- Create documentation without clear organization
- Duplicate information across multiple docs

✅ **Do:**
- Use `docs/` directory for all documentation
- Organize by feature/scope
- Maintain memory lane for context preservation
- Link related documents together
- Update docs as code evolves


---

# Code Review Practices

## Review Checklist

- [ ] Code follows project style guidelines
- [ ] No obvious bugs or logic errors
- [ ] Error handling is appropriate
- [ ] Tests cover new functionality
- [ ] No security vulnerabilities introduced
- [ ] Performance implications considered
- [ ] Documentation updated if needed

## Giving Feedback

**Good:**
```
Consider using `Array.find()` here instead of `filter()[0]` -
it's more readable and stops at the first match.
```

**Bad:**
```
This is wrong.
```

## PR Description Template

```markdown
## Summary
Brief description of changes

## Changes
- Added X feature
- Fixed Y bug
- Refactored Z

## Testing
- [ ] Unit tests added
- [ ] Manual testing performed

## Screenshots (if UI changes)
```

## Best Practices

- Review promptly (within 24 hours)
- Focus on logic and design, not style (use linters)
- Ask questions rather than make demands
- Praise good solutions
- Keep PRs small and focused
- Use "nitpick:" prefix for minor suggestions
- Approve with minor comments when appropriate


---

# Refactoring Patterns

## Common Code Smells

### Long Method
Split into smaller, focused functions.

```typescript
// Before
function processOrder(order: Order) {
  // 100 lines of code...
}

// After
function processOrder(order: Order) {
  validateOrder(order);
  calculateTotals(order);
  applyDiscounts(order);
  saveOrder(order);
}
```

### Duplicate Code
Extract common logic.

```typescript
// Before
function getAdminUsers() {
  return users.filter(u => u.role === 'admin' && u.active);
}
function getModeratorUsers() {
  return users.filter(u => u.role === 'moderator' && u.active);
}

// After
function getActiveUsersByRole(role: string) {
  return users.filter(u => u.role === role && u.active);
}
```

### Primitive Obsession
Use value objects.

```typescript
// Before
function sendEmail(email: string) { /* ... */ }

// After
class Email {
  constructor(private value: string) {
    if (!this.isValid(value)) throw new Error('Invalid email');
  }
}
function sendEmail(email: Email) { /* ... */ }
```

### Feature Envy
Move method to class it uses most.

```typescript
// Before - Order is accessing customer too much
class Order {
  getDiscount() {
    return this.customer.isPremium() ?
      this.customer.premiumDiscount :
      this.customer.regularDiscount;
  }
}

// After
class Customer {
  getDiscount(): number {
    return this.isPremium() ? this.premiumDiscount : this.regularDiscount;
  }
}
```

## Safe Refactoring Steps

1. Ensure tests pass before refactoring
2. Make one small change at a time
3. Run tests after each change
4. Commit frequently
5. Refactor in separate commits from feature work

## Best Practices

- Refactor when adding features, not separately
- Keep refactoring commits separate
- Use IDE refactoring tools when available
- Write tests before refactoring if missing


---

# Version Control Patterns

## Branching Strategies

### GitHub Flow
Simple: main + feature branches.

```
main ─────●─────●─────●─────●─────
           \         /
feature     ●───●───●
```

### Git Flow
For scheduled releases: main, develop, feature, release, hotfix.

```
main    ─────●─────────────●─────
              \           /
release        ●─────────●
                \       /
develop  ●───●───●───●───●───●───
          \     /
feature    ●───●
```

## Commit Messages

```
feat: add user authentication

- Implement JWT-based auth
- Add login/logout endpoints
- Include password hashing

Closes #123
```

**Prefixes:**
- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code change that doesn't fix bug or add feature
- `docs:` - Documentation only
- `test:` - Adding tests
- `chore:` - Maintenance tasks

## Best Practices

- Keep commits atomic and focused
- Write descriptive commit messages
- Pull/rebase before pushing
- Never force push to shared branches
- Use pull requests for code review
- Delete merged branches
- Tag releases with semantic versions
