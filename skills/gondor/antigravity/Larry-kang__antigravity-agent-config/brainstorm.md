---
description: 設計先行 - 蘇格拉底式需求釐清與設計精煉流程
---

# /brainstorm 工作流

在開始實作前，透過蘇格拉底式對話釐清需求，產出設計文件。

## 前置條件
- 有模糊的功能需求或想法
- 需要探索多種方案

## 流程

### Step 1: 讀取 brainstorming 技能
```
參考 .agent/skills/brainstorming/SKILL.md
```

### Step 2: 理解上下文
- 檢查專案現狀（檔案、文檔、近期提交）
- 確認相關功能的既有實作

### Step 3: 蘇格拉底式對話
- 一次一問，釐清需求
- 多選題優先
- 記錄所有決策

### Step 4: 提出方案
- 提出 2-3 種方案
- 說明各方案的優缺點
- 給出建議並說明理由

### Step 5: 分段呈現設計
- 每段 200-300 字
- 確認每段後再繼續
- 涵蓋：架構、資料流、錯誤處理、測試

### Step 6: 產出設計文件
// turbo
```powershell
$date = Get-Date -Format "yyyy-MM-dd"
$topic = "[topic-name]"
$path = "docs/plans/$date-$topic-design.md"
New-Item -ItemType File -Path $path -Force
```

### Step 7: 提交設計文件
```bash
git add docs/plans/*.md
git commit -m "docs: add design for [topic]"
```

## 後續步驟
設計核准後：
1. 使用 `/execute-plan` 執行實作
2. 或使用 `writing-plans` 技能產出詳細計畫

## 輸出物
- `docs/plans/YYYY-MM-DD-<topic>-design.md`
