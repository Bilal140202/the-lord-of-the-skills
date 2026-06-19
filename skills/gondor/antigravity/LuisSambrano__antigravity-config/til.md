---
description: Append a Today I Learned entry to the knowledge base repository.
---

# /til

Creates and pushes a structured learning entry.

## Steps

1. Parse the concept or learning from the user command.
2. Expand into a structured entry: what, why, code example, references.
3. Infer category from the topic (e.g., javascript, react, databases, architecture, devops).
4. Generate a kebab-case filename.
5. Navigate to ~/playground/repos/LuisSambrano/today-i-learned.
6. Write the file to the inferred category directory.
7. Execute: git pull origin main && git add . && git commit -m "docs(til): add [topic]" && git push origin main
8. Report the file title, category, and path.

## Entry format

# [Title]
Date: YYYY-MM-DD
Category: [name]

## What I Learned
[Technical explanation]

## Example
[Code example]

## Why It Matters
[Impact on architecture, performance, or workflow]

## References
[Links to documentation]
