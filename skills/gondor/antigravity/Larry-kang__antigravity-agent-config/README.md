# Global Skills (全域技能庫)

這個目錄存放跨專案通用的 Agent 技能，採用 Superpowers 框架的最佳實踐。

## 技能清單

### 核心工程紀律 (Core Engineering Discipline)
| 技能 | 用途 |
|------|------|
| `tdd` | 測試驅動開發 - RED-GREEN-REFACTOR 循環 |
| `systematic-debugging` | 四階段根因分析 |
| `verification-before-completion` | 完成前驗證機制 |

### 設計與規劃 (Design & Planning)
| 技能 | 用途 |
|------|------|
| `brainstorming` | 蘇格拉底式設計精煉 |
| `writing-plans` | 實作計畫撰寫 |
| `subagent-development` | 子代理驅動開發 + 二階段審查 |

### 審查與品質 (Review & Quality)
| 技能 | 用途 |
|------|------|
| `code-review` | 二階段代碼審查 (Spec + Quality) |
| `skill-factory` | 技能撰寫規範 + CSO 優化 |

### 專業領域 (Domain-Specific)
| 技能 | 用途 |
|------|------|
| `dotnet-engineering` | .NET 開發規範 |
| `gas-ops` | Google Apps Script 營運流程 |
| `python-ops` / `python-scripting` | Python 環境與腳本 |
| `git-ops` / `git-branching` | Git 版本控制 |
| `n8n-ops` | n8n 工作流管理 |
| `notion-sync` | Notion 同步操作 |
| `quantitative-research` / `research-workflow` | 量化研究流程 |

## 架構

```
skills/
  skill-name/
    SKILL.md              # 技能說明 (必要)
    scripts/              # 輔助腳本 (可選)
    references/           # 參考文件 (可選)
```

## CSO 規範 (Claude Search Optimization)

技能的 `description` 欄位必須符合 CSO 格式：
- 以「Use when...」開頭
- 描述觸發條件與症狀
- 不描述技能內容

詳見 `skill-factory/SKILL.md`。
