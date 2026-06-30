---
description: Đẩy kết quả test automation (Playwright/JUnit/Allure) lên Xray Test Management.
skills:
  - jira_integration
---

# Workflow: Import Test Results to Xray

> **BẮT BUỘC (MANDATORY SKILL):** Bạn PHẢI nạp và đọc kỹ nội dung của skill **`jira_integration`** (tại `.agent/skills/jira_integration/SKILL.md`) để biết cách sử dụng scripts trước khi bắt đầu.

Workflow này giúp đẩy kết quả test automation lên Xray (Cloud hoặc Server/Data Center) để tracking trên Jira.

## Các bước thực hiện:

1. **Kiểm tra prerequisites:**
   - Đọc skill `jira_integration` để nắm cấu trúc scripts.
   - Kiểm tra file `.env` đã cấu hình Xray credentials:
     - **Xray Cloud**: `XRAY_CLIENT_ID`, `XRAY_CLIENT_SECRET`
     - **Xray Server**: `JIRA_PAT` hoặc `JIRA_EMAIL` + `JIRA_API_TOKEN`
   - Kiểm tra `XRAY_PLATFORM` (cloud/server) trong `.env`.
   - Nếu chưa cài dependencies: `cd scripts/integrations && npm install`

2. **Verify Xray authentication:**
   ```bash
   node scripts/integrations/jira/xray_auth.js --verify
   ```
   - Nếu thất bại: kiểm tra credentials trong `.env`

3. **Xác định report cần import:**
   - Hỏi user loại report:
     - **Playwright JSON**: `--format playwright --file <path-to-results.json>`
     - **JUnit XML**: `--format junit --file <path-to-junit.xml>`
     - **Xray JSON** (đã convert sẵn): `--format xray --file <path-to-xray.json>`
   - Xác nhận **Project Key** (từ `.env` hoặc `--project`)

4. **Thực thi import:**
   ```bash
   # Playwright report
   node scripts/integrations/jira/xray_importer.js --format playwright --file ./test-results.json --project PROJ

   # JUnit XML
   node scripts/integrations/jira/xray_importer.js --format junit --file ./junit-results.xml --project PROJ

   # Xray JSON
   node scripts/integrations/jira/xray_importer.js --format xray --file ./xray-payload.json
   ```

5. **Xử lý kết quả:**
   - Kiểm tra output: Test Execution Key được tạo trên Jira.
   - Nếu thành công: thông báo user key của Test Execution mới.
   - Nếu thất bại: đọc log → phân tích nguyên nhân → fix → chạy lại.

6. **Lưu ý quan trọng:**
   - **Test Key Convention**: Test title nên chứa Jira key để Xray mapping tự động:
     ```typescript
     test('[PROJ-123] Login should work', async ({ page }) => { ... });
     ```
   - **Xray Cloud** cần authenticate riêng (Client ID + Secret), khác với Jira auth.
   - **Rate limit**: Tránh import quá nhiều lần liên tiếp.
