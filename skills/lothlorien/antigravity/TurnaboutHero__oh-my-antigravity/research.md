---
description: Multi-agent research orchestration
---

# /research

## What It Does

Orchestrates parallel scientist agents for comprehensive research workflows.

## Commands

```bash
/research <goal>              # Standard research with checkpoints
/research AUTO: <goal>        # Fully autonomous until complete
/research status              # Check current session
/research resume              # Resume interrupted session
/research list                # List all sessions
/research report <session-id> # Generate report
```

## Research Protocol

### 1. Decomposition
Breaks goal into 3-7 independent research stages

### 2. Parallel Execution
Fires up to 5 scientist agents concurrently

### 3. Cross-Validation
Verifies consistency across findings

### 4. Synthesis
Generates comprehensive markdown report

## Model Routing

- **Data gathering** → scientist-low (Haiku)
- **Standard analysis** → scientist (Sonnet)
- **Complex reasoning** → scientist-high (Opus)

## Example

**User**: `/research AUTO: analyze user churn patterns`

**System**:
```
[Research Session: churn-2024]
[Decomposition]
  Stage 1: Load and clean user data
  Stage 2: Exploratory data analysis
  Stage 3: Cohort analysis
  Stage 4: Feature importance
  Stage 5: Predictive modeling
  Stage 6: Visualization
  Stage 7: Recommendations

[Parallel Execution - Wave 1]
  → scientist-low: Loading data... ✓
  → scientist-low: Data cleaning... ✓
  → scientist: EDA... ✓

[Parallel Execution - Wave 2]
  → scientist: Cohort analysis... ✓
  → scientist-high: Feature importance... ✓
  → scientist-high: Predictive modeling... ✓

[Parallel Execution - Wave 3]
  → scientist: Creating visualizations... ✓
  → scientist-high: Generating recommendations... ✓

[Cross-Validation]
  ✓ Churn rate consistent across stages (23.4%)
  ✓ Top 3 features validated
  ✓ Model accuracy confirmed (R²=0.84)

[Synthesis]
  → Generating report...
  ✓ Saved to .oma/research/churn-2024/report.md

[Complete] Research session churn-2024 finished!
  Report: .oma/research/churn-2024/report.md
  Figures: .oma/research/churn-2024/figures/
  Data: .oma/research/churn-2024/data/
```

## Session Management

Research state persists at:
```
.oma/research/{session-id}/
├── report.md
├── figures/
│   ├── churn_over_time.png
│   ├── feature_importance.png
│   └── cohort_heatmap.png
├── data/
│   └── processed_data.csv
└── session.json
```

Resume anytime:
```
/research resume churn-2024
```

## Report Format

```markdown
# User Churn Analysis Report

## Executive Summary
[High-level findings]

## Methodology
[Data sources, sample size, time period]

## Key Findings

### Finding 1: Churn Rate Trends
[STAT:CHURN_RATE] 23.4% (95% CI: 22.1%-24.7%)

![Churn over time](figures/churn_over_time.png)

### Finding 2: Top Predictors
[STAT:FEATURE_IMPORTANCE]
1. Days since last login: 0.42
2. Feature usage count: 0.31
3. Support ticket count: 0.18

![Feature importance](figures/feature_importance.png)

## Limitations
- Sample limited to Q4 2024
- Self-reported satisfaction scores

## Recommendations
1. Implement re-engagement campaign...
2. Improve onboarding for...
```

---

*"Research is formalized curiosity."*
