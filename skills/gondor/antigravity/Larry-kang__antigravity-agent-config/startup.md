---
description: 一鍵啟動：Git 同步 -> 環境修復 -> 每日例行
---

# 啟動自動化工作流 (/startup)

此工作流為每日工作的標準入口，確保環境最新、代碼健康後，銜接至每日工作。

## 1. 核心啟動 (Core Startup)
執行以下指令以同步代碼並修復潛在的環境問題：

// turbo
```powershell
# 1. 同步 main 分支
git checkout main
git pull origin main

# 2. 執行環境修復
.bin\python\python.exe ops/repair_project.py

# 3. 執行報告檢查
.bin\python\python.exe ops/lint_reports.py
```

## 2. 銜接工作 (Next Steps)
環境就緒後，請選擇當日任務：

*   **每日市場掃描**: 執行 [/daily-routine](file:///.agent/workflows/daily-routine.md)
*   **標的深度研究**: 執行 [/ticker-deep-dive](file:///.agent/workflows/ticker-deep-dive.md)
*   **生成全球報告**: 執行 `.bin\python\python.exe ops/generate_reports.py`

---
> [!TIP]
> 建議依序執行：Git Sync -> Repair -> Daily Routine。

## 3. 文件審查 (Document Review)
執行任何工作後，請務必執行 [/document-review](file:///.agent/workflows/document-review.md) 以確保產出品質。
