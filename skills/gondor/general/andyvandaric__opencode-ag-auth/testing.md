## 🧪 Testing Strategy & Best Practices

> **Universal testing guidelines** - AI should adapt examples to match the project's primary language.
> Examples below cover multiple languages. Apply patterns that fit your stack.

---

### Test Types & When to Use

| Type | Scope | Speed | When |
|------|-------|-------|------|
| **Unit** | Single function/module | Fast (ms) | Every feature/fix |
| **Integration** | Multiple modules together | Medium (s) | API endpoints, DB ops |
| **E2E** | Full user flow | Slow (min) | Critical paths only |

---

### Test Requirements by Change Type

| Change Type | Required Tests |
|-------------|---------------|
| Bug fix | Test proving bug is fixed |
| New feature | Unit + integration tests |
| Refactor | Existing tests must pass |
| API change | Contract tests for input/output |
| UI change | Snapshot or E2E test |
| Config/script | Verification test |

---

### Bash/Shell Testing

```bash
#!/usr/bin/env bash
set -euo pipefail
# test-script.sh — lightweight test harness

# Setup test environment
ROOT="$(pwd)/test-run"
mkdir -p "$ROOT"
CALLS="$ROOT/calls.log"
rm -rf "$ROOT" || true
mkdir -p "$ROOT"

# Create mocks for external commands
mock() {
  cat > "$ROOT/mocks/$1" <<'EOF'
#!/usr/bin/env bash
echo "MOCK:$0 $@" >> __CALLS__
EOF
  sed -i "s#__CALLS__#${CALLS}#g" "$ROOT/mocks/$1"
  chmod +x "$ROOT/mocks/$1"
}

# Put mocks at front of PATH
export PATH="$ROOT/mocks:$PATH"

# Test cases
echo "Test 1: dry-run mode"
./script.sh --dry-run > "$ROOT/dry-run.out" 2>&1 || true
grep -q "DRY-RUN" "$ROOT/dry-run.out" && echo "PASS" || echo "FAIL"

echo "Test 2: verify expected commands called"
./script.sh --apply > "$ROOT/apply.out" 2>&1 || true
grep -q "MOCK:.*expected-command" "$CALLS" && echo "PASS" || echo "FAIL"

echo "TESTS COMPLETE. Logs in $ROOT"
```

**Key patterns:**
- Use `set -euo pipefail` for strict mode
- Mock external commands by placing scripts in PATH
- Log mock invocations to verify behavior
- Use grep assertions for verification

---

### TypeScript/JavaScript Testing

```typescript
// Co-locate tests: utils.test.ts next to utils.ts
import { describe, test, expect, vi } from 'vitest';

// ✅ Descriptive test names
test('returns empty array when no items match query', () => {
  const result = search('nonexistent');
  expect(result).toEqual([]);
});

// ✅ Mock external dependencies
const mockDb = {
  query: vi.fn().mockResolvedValue([{ id: 1 }]),
};
const service = new TaskService(mockDb);
```

---

### Rust Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;
    
    #[test]
    fn test_specific_behavior() {
        // Arrange
        let input = create_test_input();
        
        // Act
        let result = function_under_test(input);
        
        // Assert
        assert_eq!(result, expected_output);
    }
    
    #[test]
    fn test_with_temp_files() {
        let temp = tempdir().unwrap();
        let file_path = temp.path().join("test.txt");
        // temp auto-cleans on drop
    }
}
```

---

### Python Testing

```python
import pytest
from unittest.mock import Mock, patch

def test_function_behavior():
    """Test describes expected behavior."""
    result = function_under_test("input")
    assert result == expected_output

@patch('module.external_service')
def test_with_mock(mock_service):
    """Mock external dependencies."""
    mock_service.return_value = {"status": "ok"}
    result = call_service()
    assert result["status"] == "ok"
```

---

### Mock & Stub Guidelines

| Mock | Don't Mock |
|------|-----------|
| External APIs | Pure functions |
| Database calls | Business logic |
| File system | Data transformations |
| Time/Date | Simple calculations |
| Network requests | Internal utilities |

---

### Coverage Guidelines

| Threshold | Level | Notes |
|-----------|-------|-------|
| **80%+** | Target | For new code |
| **60%+** | Minimum | For legacy code |
| **100%** | Critical paths | Auth, payments, data ops |

---

### Pre-Commit Checklist

Before every commit:
- [ ] All tests pass
- [ ] No skipped tests
- [ ] Coverage not decreased
- [ ] New code has tests

**Commands by language:**
```bash
# Bash
shellcheck *.sh && ./test-script.sh

# TypeScript
pnpm test --coverage

# Rust
cargo test --lib

# Python
pytest --cov
```

---

### Anti-Patterns to Avoid

| ❌ Don't | ✅ Do |
|---------|------|
| Test implementation details | Test behavior/output |
| Depend on test order | Each test is independent |
| Use real external services | Mock external dependencies |
| Write tests after deployment | Write tests with code |
| Skip tests to meet deadlines | Fix failing tests first |
