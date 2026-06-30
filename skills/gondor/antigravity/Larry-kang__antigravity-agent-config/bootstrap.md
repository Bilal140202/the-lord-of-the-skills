---
description: 一鍵初始化新專案環境與 .agent 規範 (Project Bootstrap SOP)
---

# Project Bootstrap Workflow

此工作流用於快速初始化新專案的 `.agent` 配置，確保所有新專案從第一天起就符合團隊規範。

## 執行步驟

1. **環境健全檢查 (Health Check)**:
   - 確保已安裝 Docker, .NET SDK, & Python。
2. **初始化目錄結構**:
   - 建立 `.agent/rules/`, `.agent/skills/`, `.agent/workflows/`。
3. **注入核心規範 (Core Rules)**:
   - 調用 `skill-factory` 產出基本的 `naming-conventions.md`。
4. **設置維運腳本**:
   - 建立 `start_project.ps1` 模板。
5. **首次 Git 提交**:
   - `git init`
   - `git add .`
   - `git commit -m "chore: initial bootstrap with Antigravity standards"`

## 調用方式
在聊天框輸入：`/bootstrap`
