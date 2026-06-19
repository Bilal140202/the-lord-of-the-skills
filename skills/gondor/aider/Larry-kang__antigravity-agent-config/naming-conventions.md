---
name: naming-conventions
description: 本專案的全局命名與代碼行為規範。
filters:
  - pattern: "*"
---

# 命名與技術規範 (Naming & Technical Conventions)

本規範適用於所有 Agent 在本專案中的行為，旨在確保代碼的一致性、安全性與效能。

## 1. 命名規範 (Naming Standards)

- **檔案命名 (File Naming)**: 
  - 所有新增檔案必須使用 **全小寫** 並以 **連字符 (`-`)** 分隔。
  - 範例: `ticker-analysis-v1.md`, `python-ops.py`。
- **變數與函式 (Variables & Functions)**: 
  - 遵循該語言的官方慣例（例如：Python 使用 `snake_case`，C# 使用 `PascalCase`）。
- **類別命名 (Class Naming)**: 
  - 統一使用 `PascalCase`。

## 2. 代碼行為規範 (Coding Standards)

- **UTF-8 強制協定**: 
  - 讀寫任何檔案必須顯式指定 `encoding='utf-8'`。
  - 對於 C# 與 PowerShell，優先考慮無 BOM 的 UTF-8。
- **異步優先**: 
  - 在 C# 與 JavaScript 中，除非有特殊理由，否則應優先使用異步操作。
- **錯誤處理 (Error Handling)**: 
  - 嚴禁使用空白的 `catch` 區塊。
  - 所有的錯誤訊息必須包含足夠的上下文以便診斷。

## 3. Git 操作規範 (Git Protocol)

- **分支管理**: 
  - 禁止隨意在 `main` 分支進行實驗性變更。
  - 使用功能分支 (`feat/`, `fix/`, `doc/`) 進行作業。
- **提交訊息**: 
  - 使用繁體中文撰寫提交描述。
  - 遵循語義化提交 (Semantic Commits) 格式。

## 4. 語言協議 (Language Protocol)

- **繁體中文指令**: 
  - 所有的 Markdown 文件內容、報告、日誌以及程式碼中的註解，必須 100% 使用繁體中文。
  - 程式碼關鍵字與專有名詞除外。
