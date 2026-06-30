---
globs: "**/*"
---
# Git and commits (always on)

Parallel agent sessions share `main` on this clone. See `CLAUDE.md` § Git commits
for the full tier table. Short form:

- **Default: Tier A lean commit** — `git commit --only <your-paths> -m "type(scope): subject"` then stop (no `changelog.d/`, version bump, or push in that turn).
- **When:** slice done or before idle — not every turn. Slash command: `/lean-commit`.
- **Tier B:** user-visible change → add a `changelog.d/` snippet (separate commit or next turn); never edit `CHANGELOG.md` by hand.
- **No** push unless the user said push/ship/Push all.
- **Release (Tier C):** version bump + `scripts/cut-release.sh` only when cutting a release.
