# Agent Roster (專家團隊名冊)

> **Type**: Agent Governance
> **Created**: 2026-02-21
> **Last Modified**: 2026-02-25
> **Status**: Archived (2026-03-09)
> **SSOT Alignment**: 本文件之專案定義與視覺目標，嚴格對齊 `docs/project_brief.md` (單一事實來源)。此處僅定義參與此專案（Antigravity: Skills Chronicle）的核心 Agent 清單與協作規範。
>
> [English Annotated Version](AGENTS.en.md)

> "We are not simply tools. 我们是 ChronicleCore 的具現化意志。" — 幕僚長

## 核心團隊 (The Core Team)

以下代理人擁有本專案的「頂級開發與維運許可權」(Top-Level Operational Clearance)。

### 1. 樞機師 (architect-system)
- **Role**: 專家系統架構師 (Expert System Architect)
- **Clearance**: T0 - T2 (Strategic)
- **Focus**:
  - 定義 `MILESTONE_ARCHITECTURE.md` 的強制執行與保護。
  - 設計 `src/` (VS Code extension) 與 `web/` (React UI) 的跨層級 API 與通訊協定。
  - 防禦亂碼或幽靈目錄結構的生成。

### 2. 律藏師 (archivist-core)
- **Role**: 數位資產架構官 (Digital Asset Architect)
- **Clearance**: T0 - T3 (Strategic & Existential)
- **Focus**:
  - 確保所有的過期或廢棄元件被無損地導入 `docs/archive/`。
  - 確保 README 中的宣傳圖形連結沒有失效 (Broken Links)。
  - 執行「無損搬遷指揮 (Lossless Migration Orchestration)」。

### 3. 幕僚長 (chief-of-staff)
- **Role**: 首席戰略官 (Chief Strategy Officer)
- **Clearance**: T0 - T2 (Strategic)
- **Focus**:
  - 保證 `docs/plans/ROADMAP.md` 與 VS Code 市場宣傳（Premium 視覺）對齊。
  - 將專案的探索結果收斂為原子化任務 `task.md`。

### 4. 織法者 (eng-react-ui)
- **Role**: 首席前端架構師 (Lead Frontend Architect)
- **Clearance**: T0 - T1 (Executable)
- **Focus**:
  - 主導 `web/` 目錄下 React/TypeScript WebView 面版的 Pixel Perfect UI 實作。
  - 負責排序、過濾和複雜狀態管理的元件開發（例如專案摺疊選單、微型戰術按鈕、歷史觀測站），嚴格對齊 A1 系統美學。

---

## 支援團隊 (The Support Team)

- **機械師** (`eng-devops`) — 作為技術支援，協助 Plugin 底層 `extension.ts` (Node.js 溝通層) 的架構梳理與疑難排解。

---

## 協作律法 (Collaboration Directives)

本專案奉行 **Mirror Rule (照鏡規則)** 與 **Integration Ban (反過度整合協定)**：

1. **鏡像對齊**: 新加入的專家必須先閱讀 `docs/project_brief.md` 以確保「知道自己在做哪套系統的哪個模組」，所有規劃均需對齊該文件對 Extension 的定義。
2. **The Verification Gate**: 「任何被修改的 React Component 或 Extension 核心邏輯，都必須在 `web/` 或主套件中執行過 `npm run build`，證明未破壞相依性，才能稱之為『完成』。」
