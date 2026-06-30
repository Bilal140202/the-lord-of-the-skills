---
description: Autonomous research on a topic followed by structured GitHub Issue creation.
---

# /issue

Researches a topic and creates a structured GitHub Issue.

## Steps

1. Parse the topic from the user command.
2. Search the web for official documentation, specifications, tradeoffs, and relevant context.
3. Structure findings:
   - Context / Problem
   - Objective
   - Findings
   - Conclusion / Recommended action
4. Create the GitHub Issue:
   gh issue create --title "[RESEARCH] topic" --body "content" --label "research"
5. Return the issue URL.

## Usage examples

/issue Research migrating from REST to GraphQL
/issue Investigate Supabase realtime capabilities
/issue Document Next.js server action limitations
