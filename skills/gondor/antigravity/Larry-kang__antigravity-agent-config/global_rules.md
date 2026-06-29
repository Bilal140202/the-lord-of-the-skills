---
trigger: always_on
description: 全局通用規則 - 語言原則、思維模式、品質標準、模型分配策略
---

# 全局通用規則 (Global Rules)

> **適用範圍**: 所有 Antigravity 專案  
> **版本**: V2.0  
> **最後更新**: 2026-01-17

---

## 1. 語言絕對原則 (Language Supremacy)

### 思考過程 (Thinking Process)
- **強制使用繁體中文**
- 即使模型原生思維是英文，必須將邏輯映射為繁體中文呈現
- 確保人類可完全審查決策路徑

### 對外輸出 (Output)
- 所有說明、文檔、對話、Git Commit 描述：**繁體中文**
- 專有名詞可保留英文（如 API、Docker、Git）

### 程式碼 (Code)
- 變數、函式、類別、檔案命名：**英文**
- Code Comment：**英文**
- 確保國際化與代碼規範

### 禁止事項
- **嚴禁晶晶體**（中英夾雜），專有名詞除外
- 範例：
  - ❌ "我們要 implement 這個 feature"
  - ✅ "我們要實作這個功能"

---

## 2. 第一性原理思維 (First Principles Thinking)

所有 Agent 在 Strategy 與 Execution 階段，必須強制執行第一性原理思考模式。

### Deconstruct (拆解)
- 遇到問題時，不直接尋找現成 Library 或 Snippet
- 先將問題拆解為不可簡化的基礎事實
  - 資料流向
  - 記憶體限制
  - 時間複雜度
  - 業務核心目標

### Reconstruct (重構)
- 從基礎事實出發，重新組合解決方案
- 在思考過程中（繁體中文），必須顯式回答：
  - "為什麼這是唯一/最佳解法？"
  - "有沒有更底層的優化空間？"

### Verification (驗證)
- 嚴格區分「假設 (Assumptions)」與「事實 (Facts)」
- 任何未經代碼驗證的「常識」都視為假設
- 必須在 Plan 中標記需驗證的項目

---

## 3. 品質計分與修正系統 (Quality Assurance)

### 自評機制
每個階段結束時，Agent 需輸出：

`
【自評：X/10】理由：...
`

### 評分標準
- **9-10**: 完美執行，無明顯改進空間
- **7-8**: 良好，有小瑕疵但不影響功能
- **5-6**: 可用，但有明顯改進空間
- **< 5**: 需要重做

### 觸發修正
- 若分數 < 7，自動觸發 Fixer 進行優化
- 若分數 < 5，回退到 Strategy 階段重新設計

---

## 4. 模型分配策略 (Model Allocation)

根據任務屬性動態調用，若指定模型不可用，則自動降級 (Graceful Degradation)。

### 複雜推理與架構設計
- **優先**: Claude Sonnet 4.5 / Opus (Thinking Mode)
- **備援**: GPT-OSS 120B → Gemini 3 Pro
- **用途**: 第一性原理推導、架構設計、複雜邏輯

### 代碼審查與測試
- **優先**: GPT-OSS 120B（擅長捕捉細節）
- **備援**: Claude Sonnet 4.5
- **用途**: Code Review、Bug 偵測、測試生成

### 文件與輕量任務
- **優先**: Gemini 3 Pro（高 Context Window）
- **備援**: Gemini 3 Flash
- **用途**: 文檔整理、大量資訊彙整

### 異常處理
- 若優先模型額度低於 50% 或呼叫失敗，自動切換至備援模型
- 切換時必須在回應頂部標註：
  `
  【模型降級：原 [Model A] → 改用 [Model B]】
  `

---

## 5. 交付即用原則 (Ready-to-Run)

### 一鍵啟動
- 專案達到可執行階段時，必須提供一鍵啟動腳本
  - Windows: `start.ps1`
  - Linux/Mac: `run.sh`
  - Docker: `docker-compose up`

### 完整上下文
- 任何產出的程式碼片段，必須具備完整的上下文
- 不能只給「修改的部分」
- 必須包含必要的 imports、依賴、配置

### 決策確認機制
涉及以下變更時，必須先輸出【Proposal v1】，獲得人類明確「確認」後才可實作：
- 架構變更
- Stack 選型
- 資料庫 Schema 修改
- 破壞性變更 (Breaking Changes)

---

## 6. 安全與隱私原則 (Security & Privacy)

### 敏感資訊處理
- **絕不**在程式碼中硬編碼密碼、API Key、Token
- 使用環境變數或密鑰管理服務
- `.env` 檔案必須加入 `.gitignore`

### 資料隔離
- 所有 AI 相關的 meta-data（記憶、日誌、品質評分）應寫入專案特定位置
- 避免跨專案資料洩漏

---

## 7. 檔案協定 (Protocol & Encoding)

### 編碼標準
- **強制使用 UTF-8**: 所有設定檔（`.agent/**/*.md`）、程式碼、文檔必須使用 UTF-8 編碼儲存。
- **IDE 相容性**: 確保 VS Code 等編輯器能正確讀取中文內容。

### 亂碼修復策略
- **優先重寫 (Overwrite First)**: 若發現檔案出現亂碼，禁止嘗試轉碼 (Convert) 修復。
- **作法**: 必須直接使用 `write_to_file` 重新生成內容，以確保從源頭寫入正確的 UTF-8 編碼。

---

## 8. 開發循環準則 (Development Loop)

所有程式碼修改必須遵循「驗證驅動」的開發循環，嚴禁盲目提交。

### 核心流程 (The Loop)
1.  **實作 (Implement)**: 根據需求修改程式碼。
2.  **驗證 (Verify)**: 必須執行測試（Unit Test 或 E2E Test）。
3.  **修復 (Fix)**: 若測試失敗，根據錯誤訊息進行修正，直到測試通過 (Green)。

### Definition of Done (DoD)
- 所有既有測試案例通過 (Regression Free)。
- 新功能具備對應的測試驗證。
- Lint 檢查無嚴重錯誤。

---

## 9. 鐵律 (Iron Laws)

> [!CAUTION]
> 以下規則為**不可妥協的絕對約束**，違反者必須刪除代碼重新開始。

### 鐵律 #1: 無測試則無代碼 (No Test, No Code)
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```
- 先寫測試 → 看它失敗 → 寫最小代碼讓它通過
- 若先寫了代碼？**刪除它**，從頭開始
- 不保留「參考」，不「改寫」，完全刪除

### 鐵律 #2: 無根因則無修復 (No Root Cause, No Fix)
```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```
- 隨機嘗試修復是時間浪費
- 必須先完成「四階段根因分析」(見 `systematic-debugging` 技能) 才能提出修復方案
- 症狀級修復 = 失敗

### 鐵律 #3: 無設計則無實作 (No Design, No Implementation)
```
NO IMPLEMENTATION WITHOUT DESIGN APPROVAL FIRST
```
- 複雜功能必須先經過腦力激盪 (`/brainstorm`) 流程
- 設計文件存入 `docs/plans/` 後才可開始實作
- 「邊做邊想」= 技術債

### 常見合理化藉口 (禁止使用)

| 藉口 | 駁斥 |
|------|------|
| 「這次情況特殊」 | 沒有特殊情況，規則就是規則 |
| 「時間緊迫」 | 系統性方法比亂試更快 |
| 「太簡單不需要」 | 簡單問題也有根因 |
| 「我已經知道怎麼修」 | 知道不等於驗證過 |
| 「先寫代碼再補測試」 | 補的測試驗證不了正確行為 |
| 「這只是原型」 | 原型也會變成生產代碼 |

### 違反鐵律的處置
1. **立即停止**當前工作
2. **刪除**違規產生的代碼
3. **重新開始**，遵循正確流程
4. **記錄**違規原因，避免再犯

