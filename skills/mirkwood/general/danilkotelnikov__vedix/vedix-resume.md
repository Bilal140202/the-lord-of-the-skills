---
description: Resume a paused or failed Vedix job from its last successful phase.
argument-hint: "<job-id> [--from-phase <name>]"
---

Invoke the vedix skill in "resume" mode for the given job-id. The skill detects which artifacts exist on disk and resumes from the next phase. With `--from-phase`, force restart from that phase.
