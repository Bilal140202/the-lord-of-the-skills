# /spec

Capture the full specification for a feature or task before any code is written.

**Steps:**
1. Ask for a feature name if not provided as an argument
2. Ask the user to describe: goal, user stories, acceptance criteria, constraints, and what is explicitly out of scope
3. Create `docs/specs/` directory if it does not exist
4. Save the gathered information to `docs/specs/{name}.md` using the template below
5. Confirm the file was saved and prompt the user to run `/research`

**Output template (`docs/specs/{name}.md`):**
```markdown
# Spec: {name}

## Goal
{goal}

## User Stories
{user stories}

## Acceptance Criteria
{acceptance criteria}

## Constraints
{constraints}

## Out of Scope
{out of scope}
```
