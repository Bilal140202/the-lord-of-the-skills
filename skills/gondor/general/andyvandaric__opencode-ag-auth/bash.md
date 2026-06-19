## 🐚 Bash/Shell Scripting Rules

### Shebang Requirements
```bash
#!/usr/bin/env bash   # ✅ PREFERRED - portable
#!/bin/bash           # ✅ OK - direct path
#!/bin/sh             # ⚠️ POSIX only - more portable but limited
```

### Naming Conventions
| Context | Convention | Example |
|---------|------------|---------|
| Variables (local) | snake_case | `local_var`, `file_path` |
| Variables (exported) | SCREAMING_SNAKE | `DEPLOY_ENV`, `API_KEY` |
| Functions | snake_case | `process_file()`, `validate_input()` |
| Scripts | kebab-case or snake_case | `deploy-app.sh`, `install_deps.sh` |
| Constants | SCREAMING_SNAKE | `readonly MAX_RETRIES=3` |

### Best Practices
```bash
# ✅ ALWAYS use at top of scripts
set -euo pipefail    # Exit on error, undefined vars, pipe failures
# OR
set -e               # Exit on error (minimum)

# ✅ Quote variables to prevent word splitting
echo "$variable"     # ✅ GOOD
echo $variable       # ❌ BAD - word splitting issues

# ✅ Use [[ ]] for conditionals (bash-specific, safer)
if [[ -f "$file" ]]; then ... fi    # ✅ GOOD
if [ -f "$file" ]; then ... fi      # ⚠️ OK but less safe

# ✅ Use $() for command substitution
result=$(command)    # ✅ GOOD
result=`command`     # ❌ BAD - deprecated backticks
```

### Shellcheck
> **MANDATORY**: Run shellcheck before committing shell scripts.

```bash
# Install
apt install shellcheck   # Debian/Ubuntu
brew install shellcheck  # macOS

# Run
shellcheck script.sh

# Common errors to fix:
# SC2086: Double quote to prevent globbing and word splitting
# SC2034: Variable appears unused (may be exported)
# SC2155: Declare and assign separately to avoid masking return values
```

### Error Handling Pattern
```bash
#!/usr/bin/env bash
set -euo pipefail

# Trap for cleanup on exit
cleanup() {
    echo "Cleaning up..."
    rm -f "$temp_file"
}
trap cleanup EXIT

# Function with error handling
do_something() {
    local input="$1"
    if [[ -z "$input" ]]; then
        echo "Error: input is required" >&2
        return 1
    fi
    # ... do work
}

main() {
    local temp_file
    temp_file=$(mktemp)
    
    do_something "$1" || exit 1
}

main "$@"
```

### Common Patterns
```bash
# Check if command exists
command -v docker &>/dev/null || { echo "docker not found"; exit 1; }

# Default values
: "${VAR:=default_value}"

# Read file line by line
while IFS= read -r line; do
    echo "$line"
done < "$file"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help) show_help; exit 0 ;;
        -v|--verbose) VERBOSE=1; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done
```
