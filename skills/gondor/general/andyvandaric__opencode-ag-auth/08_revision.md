## 🔄 Revision Workflow

### When Starting from Backlog
> [!CAUTION]
> If task is in **Backlog**: DO NOT implement!

1. Ask user if they want to proceed
2. If complex: Create Implementation Plan → move to **Planned**
3. If simple: User approves directly → move to **Ready**
4. Get explicit approval → move to **Doing** to implement

### Minor Revisions (Same Task)
| Current Stage | User Says "change X" | Action |
|--------------|---------------------|--------|
| Ready | Update plan, stay in Ready |
| Doing | Fix inline, no status change |
| Testing | → Doing, fix, → Testing again |
| Done | Create NEW bug/chore task |

### Major Revisions (Scope Change)
1. Mark current task with note: "Superseded by [new-id]"
2. Create new task with updated scope
3. Fresh workflow: Backlog → Planned → Ready → Doing

### 🔄 Research → Implementation (Clone Workflow)
When research is complete and ready for implementation:

```bash
# Clone research task as implementation feat
flowcrate clone <research-id> -t feat --title "Implement: <title>" -s ready

# Example:
flowcrate clone research-4d0f -t feat --title "Implement AI Integration Polish" -s ready
```

**What gets cloned:**
- ✅ Title (can override with `--title`)
- ✅ Description
- ✅ Plan Link (key feature!)
- ✅ Priority

**What does NOT get cloned:**
- ❌ Time entries (research time stays with research)
- ❌ Walkthrough, CommitID, Summary

**Benefit:** Research task stays in Done with timer history, new feat task ready for implementation with same plan.

---

## Task Gate Rules

> [!CAUTION]
> **APPROVAL GATES** - AI must NEVER bypass!

| Status | AI Can Implement? | Requires |
|--------|------------------|----------|
| Backlog | ❌ NO | Create plan first |
| Planned | ❌ NO | **Confidence Score > 97%** + User Approval |
| Ready | ✅ YES | Just start |
| Doing | ✅ YES (already working) | - |
| Testing | ❌ NO (wait for user) | User confirmation |

### 🚀 Trivial Task Fast-Track Exception
**Rule**: Planning documentation helps complex tasks, but slows down trivial ones.
**Exception**: You may skip `Planned` stage and go directly to `Ready` IF AND ONLY IF:
1. Change is extremely simple (e.g. typos, single-line CSS, simple function rename)
2. You are **100% CONFIDENT** that it will work on the first try
3. No complex logic or architectural changes involved

If ANY doubt exists → Create Plan → Planned → Check 97% Confidence → Ready

### 🐛 Bug Fix / Debug Request Protocol

> [!CAUTION]
> **MANDATORY: Create Bug Card BEFORE Fixing!**
> When user reports a bug or requests debugging, AI MUST create a task card first.

**Trigger Phrases (Multilingual):**

| Language | Trigger Phrases |
|----------|-----------------|
| **English** | "fix this", "bug", "not working", "broken", "check wiring", "debug", "investigate", "issue with" |
| **Indonesian** | "tolong fix", "nggak bisa", "rusak", "cek wiring", "ada bug", "kenapa ini", "error", "perbaiki" |

**Protocol:**
1. ❌ **DO NOT** start fixing immediately
2. ✅ **FIRST** create bug card:
   ```bash
   flowcrate create "Fix: [brief description]" -t bug -p 1 \
     -d "[What's broken. Root cause if known. Steps to reproduce.]" \
     --json | Out-String
   ```
3. ✅ Move to Doing: `flowcrate move <id> doing`
4. ✅ Fix the bug
5. ✅ Move to Done (or Testing if needs verification)

**Exception (Skip Card Creation):**
- Typo fixes (single character/word)
- Obvious one-liner that takes < 1 minute
- User explicitly says "just fix it quick, no card needed"

**Violation = Workflow Breach:**  
Fixing bugs without tracking = lost history, no time tracking, no audit trail.

---

## 🛫 Pre-Flight Check Before Any Code Work

> [!CAUTION]
> **MANDATORY: Before writing ANY code, AI MUST verify:**
> 1. ✅ A task card EXISTS for this work
> 2. ✅ Task is in **Doing** status (run `flowcrate list --status doing --json`)
> 3. ✅ Timer is running (check `isTimerRunning: true` in output)
>
> **If any check fails:**
> - Create card if missing
> - Move to Doing: `flowcrate move <id> doing --json`
> - Verify timer started before proceeding
