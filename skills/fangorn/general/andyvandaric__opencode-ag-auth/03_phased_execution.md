## 🔗 Phased Execution Workflow

> [!IMPORTANT]
> **For complex features, break into phases with linked cards.**
> Execute phases based on: Risk ↓, Confidence ↑, Urgency ↑

### Phase Chain Pattern

When implementing multi-phase features:

1. **Create parent card** (epic or main bug/feat)
2. **Create child cards** for each phase with phase number
3. **Link plans** with proper phase chain documentation
4. **Execute by priority**: lowest risk + highest confidence first

**Example Phase Chain:**
```
Phase 1: Foundation (✅ DONE)
    └── feat-abc1: Backup module, tests
            │
            ▼
Phase 2: Bulk Operation (⏳ PENDING)
    └── feat-def2: Full workspace push
            │
            ▼
Phase 3: Fix Existing (⏳ PENDING)
    └── bug-ghi3: Fix single push ownership
```

### Phase Plan Template

Each phase plan MUST include:

```markdown
# [Title]

> **Status**: 📝 PLANNING  
> **Task ID**: [id]  
> **Priority**: P1 🔴  
> **Phase**: X of Y  
> **Confidence Score**: XX%

---

## 🔗 Phase Chain
[ASCII diagram showing dependencies]

### Dependencies
- **Requires**: [Previous phases]
- **Enables**: [Next phases]

---

## 📊 Confidence Score Analysis

| Factor | Score | Notes |
|--------|-------|-------|
| Factor 1 | XX% | Reason |
| ...     | ...  | ...    |

**Overall: XX%** - [Justification]

### Risk Areas (Why not 100%)
1. Risk 1
2. Risk 2

---

## Test Scenarios (COMPREHENSIVE)

### Scenario 1: Happy Path
[bash commands and expected output]

### Scenario N: Edge Case
[bash commands and expected output]
```

### Execution Priority Matrix

> [!CAUTION]
> **When multiple phases are Ready, execute by this priority:**

| Priority | Criteria |
|----------|----------|
| 1️⃣ **Lowest Risk** | Higher confidence score wins |
| 2️⃣ **Highest Urgency** | P0 > P1 > P2 > P3 |
| 3️⃣ **Dependency Order** | Foundation phases first |
| 4️⃣ **Smallest Scope** | Fewer files changed wins |

**Decision Flow:**
```
Ready tasks available?
    │
    ├── Sort by: Confidence DESC, Priority ASC, Scope ASC
    │
    └── Execute highest ranked first
```

### Confidence Score Analysis (Required for Complex Tasks)

> [!IMPORTANT]
> **For tasks >5 files or multi-component, MUST include factor breakdown:**

```markdown
## 📊 Confidence Score Analysis

| Factor | Score | Notes |
|--------|-------|-------|
| **Existing Code Reference** | 95% | Similar pattern exists in XYZ |
| **Backup/Rollback** | 95% | Phase 1 backup module available |
| **Cross-DB Operations** | 85% | Two connections simultaneously |
| **Bulk Operations** | 80% | Need transaction handling |
| **Edge Case Coverage** | 80% | 8 scenarios documented |

**Overall: 88%** - High confidence due to existing patterns.

### Risk Areas
1. Transaction rollback if partial failure
2. File conflict handling
3. Large dataset performance
```
