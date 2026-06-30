---
description: 文件產出審查與合規檢查 (Document Review & Compliance)
---

# 文件審查標準程序 (Document Review SOP)

本流程用於確保所有產出文件符合與用戶設定的「繁體中文」與「無亂碼」標準。

## 1. 編碼與內容審查 (Encoding & Content Audit)
1. **亂碼掃描**:
   - 檢查文件中是否出現 ``、`?` 或其他無法解析的字符。
   - 特別注意表格邊框與中文標點符號。
2. **完整性檢查**:
   - 確認 Markdown 表格格式正確 (沒有跑版)。
   - 確認所有超連結 (Links) 皆使用相對路徑且有效。

## 2. 語言合規 (Language Compliance)
依據 `language-mandate-core.md`：
1. **全繁體中文**: 說明文字、標題、分析內容必須為繁體中文。
2. **專有名詞**: 保留原文 (e.g., Bitcoin, Sharpe Ratio, NVDA)，不需強制翻譯。
3. **禁止語法**: 
   - 禁止出現簡體中文。
   - 禁止使用 "User" 或 "Client"，請統一使用 "您" 或 "用戶"。

## 3. 戰略一致性 (Strategic Alignment)
1. **各報告檢查**:
   - 確保結論 (Conclusion) 與目前的 Macro View 一致。
   - 確認風險提示 (Risk Warning) 足夠顯著。

## 4. 簽署與交付 (Sign-off)
1. **完成**: 若以上皆通過，即可進行 Git Commit 與交付。
2. **修正**: 若有問題，請立即修正該檔案，無需詢問用戶。
