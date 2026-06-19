## 📎 Linking Rules

> [!IMPORTANT]
> **ALL tasks requiring implementation MUST link their artifacts.**

### When to Link Plan
- Task involves code changes beyond trivial fixes
- Task requires design decisions or architectural changes
- Confidence score needed for approval (>97%)

### When to Link Walkthrough
- Implementation is complete
- Visual/UI changes were made
- Complex workflow was implemented
- Serves as proof-of-work documentation

### CLI Commands for Linking

> [!CAUTION]
> **MUST use relative path!** Filename-only breaks confidence score display in Kanban cards.

```bash
# Link plan to task (relative path REQUIRED)
flowcrate update <id> --plan ".flowcrate/plans/PLAN_FEAT_XXX_NAME.md"

# Link walkthrough to task (relative path REQUIRED)
flowcrate update <id> --walkthrough ".flowcrate/walkthroughs/WLKTH_FEAT_XXX_NAME.md"
```

### ❌ DO NOT
- Leave plans unlinked after creation
- Complete tasks without linking walkthrough (if one exists)
- Create orphan artifacts in brain folder instead of `.flowcrate/`

### ✅ DO
- Link plan immediately after creating it (auto-moves to Planned)
- Link walkthrough before moving to Done
- Use consistent naming: `PLAN_<TYPE>_<ID>_<NAME>.md` for plans, `WLKTH_<TYPE>_<ID>_<NAME>.md` for walkthroughs

> [!CAUTION]
> **CRITICAL: Ready Board Completion Rule**
> - BEFORE declaring ANY work session complete, ALWAYS run `flowcrate list --status ready`
> - ALL tasks in Ready board MUST be executed to completion
> - Ready = User approved and waiting = MUST DO
> - Do NOT notify user about completion if Ready board has tasks remaining
> - Execute ALL Ready tasks sequentially before session end
