## 🔄 CLI-Rulesets Sync Rule

> [!CAUTION]
> **MANDATORY: When adding/modifying ANY CLI command:**
> 1. Update `templates/core/workflow/06_cli_reference.md` with command + all flags
> 2. Add usage example with `--json | Out-String`
> 3. Verify `flowcrate <cmd> --help` works (if not, create bug card)
> 4. Run `flowcrate rules sync` to propagate to local `.gemini/`
> 5. Update plan with CLI change documented

**Purpose**: Rulesets template = Single Source of Truth for:
- AI agent context (internal documentation)
- Human developer reference
- Future User Guide foundation

### Pre-Merge Checklist for CLI Changes

| Check | Action |
|-------|--------|
| ✅ Command documented | Add to `06_cli_reference.md` |
| ✅ All flags listed | Include short + long forms |
| ✅ Example provided | Show typical usage |
| ✅ Help text works | Verify with `--help` |
| ✅ Synced to local | Run `flowcrate rules sync` |

### Template Files to Update

| Change Type | Files to Update |
|-------------|-----------------|
| New command | `06_cli_reference.md` |
| New workflow stage | `01_stages.md` |
| Linking changes | `07_linking.md` |
| Release process | `09_release.md` |
| Git workflow | `11_git_branching.md` |

### Embedded Template Workflow (CRITICAL)

> [!IMPORTANT]
> **For changes to embedded templates** (`src-tauri/src/templates/`):
> 
> Rust's `include_str!()` macro embeds files **AT COMPILE TIME**. Incremental builds may NOT pick up template changes!

**Correct Workflow:**
1. ✅ Update template file in `src-tauri/src/templates/core/workflow/`
2. ✅ **`cargo clean --manifest-path=src-tauri/Cargo.toml`** (MANDATORY!)
3. ✅ `cargo build --manifest-path=src-tauri/Cargo.toml`
4. ✅ Install binary: 
   - `cp src-tauri/target/debug/flowcrate.exe ~/.cargo/bin/`
   - `cp src-tauri/target/debug/flowcrate.exe $LOCALAPPDATA/FlowCrate/`
5. ✅ Sync to current project: `flowcrate rules sync --force`
6. ✅ Sync to all linked projects:
   ```bash
   cd flowcrate-server && flowcrate rules sync --force
   cd ../flowcrate-landing && flowcrate rules sync --force
   cd ../server-hardening && flowcrate rules sync --force
   ```

**Why `cargo clean` is required:**
- `include_str!()` dependency tracking is imperfect
- Incremental compilation may use cached embedded content
- Only full rebuild guarantees fresh template embedding

**Verification:**
```bash
# Check if update applied
grep "your new content" .gemini/rules/workflow/06_cli_reference.md

# Should return matches if sync worked
```

### Version Tracking

When making breaking CLI changes:
1. Document in `CHANGELOG.md`
2. Update command examples in rulesets
3. Create migration notes if needed
