---
description: 同步所有研究報告與量化模型文件至 Notion Research Hub (One-Way Mirror)
---

# Notion Research Sync Protocol

本 Workflow 負責將本地 `research/` 目錄下的最新分析報告、量化模型規範同步至 Notion 用戶端。

## 1. 執行同步 (Sync Execution)
腳本將執行全量比對 (Smart Mirroring)，僅上傳有變更的檔案。

// turbo-all
1. 執行同步腳本
   - Command: `.bin\python\python.exe ops/sync_full_research.py`
