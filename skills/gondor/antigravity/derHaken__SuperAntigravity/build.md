---
name: build
description: name: build
---
# Build

Build, compile, and package the project.

## Steps
1. Analyze project structure and build configuration
2. Validate environment and dependencies
3. Execute build with appropriate flags for target (dev/prod/test)
4. Parse any errors with diagnostic analysis
5. Report artifacts generated and build metrics

## Common Build Systems
- npm/bun: `npm run build` / `bun run build`
- Python: `python -m build` / `poetry build`
- Go: `go build ./...`
- Rust: `cargo build --release`
- Docker: `docker build -t name .`

## On Build Failure
Load systematic-debugging skill to diagnose root cause.
Do NOT retry the same failing command — diagnose first.
