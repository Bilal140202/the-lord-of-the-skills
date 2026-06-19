---
name: gas-ops
description: Use when developing, operating, or deploying Google Apps Script projects with CI/CD automation.
metadata:
  version: "1.1.0"
---

# GAS Ops Skill

此技能規範 Google Apps Script (GAS) 開發的標準流程，結合 `clasp` 工具與 GitHub Actions 實現自動化部屬與版本控制。

## 環境依賴 (Dependencies)
- Node.js & npm (系統環境)
- @google/clasp (全域安裝: `npm install -g @google/clasp`)
- GitHub Actions (用於自動化部屬)

## 標準開發流程 (Workflow)

### 1. 本地開發與同步
在本地進行開發後，通過 Git 提交代碼。若需從 GAS 網頁工作區同步回本地：
```powershell
clasp pull
```

### 2. 自動化部屬 (GitHub Actions)
專案應配置 `.github/workflows/deploy.yml`，在推送到特定分支（如 `master` 或 `main`）時自動執行部屬。
- **機制**: GitHub Action 會安裝 `clasp` 並利用 `CLASPRC_JSON_BASE64` 秘密金鑰進行授權。
- **指令**: `clasp push --force`

### 3. 手動急修 (Manual Emergency Push)
僅在 CI/CD 失效且需緊急修復時使用：
```powershell
clasp push
```

## CI/CD 配置規範

### 認證金鑰處理
1. 執行 `clasp login` 獲取本地 `~/.clasprc.json`。
2. 將該檔案內容轉換為 Base64 字串：
   ```powershell
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("$HOME\.clasprc.json"))
   ```
3. 將結果存入 GitHub Repository Secrets，名稱為 `CLASPRC_JSON_BASE64`。

## 最佳實踐 (Best Practices)
1. **GitHub 為單一真相來源**: 始終信任 Git 上的代碼。避免在 GAS 網頁工作區直接修改代碼，除非是為了快速測試並隨即 `clasp pull` 回本地。
2. **自動化優先**: 儘量透過 `git push` 觸發 Action 進行部屬，確保部署紀錄與 Git Commit 關聯。
3. **強制更新**: 線上環境部屬建議使用 `clasp push --force` 以避免文件版本衝突。
