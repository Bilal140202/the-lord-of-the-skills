---
description: Lấy Requirements / User Stories từ Jira ticket và lưu thành file markdown hoặc JSON.
skills:
  - jira_integration
---

# Workflow: Fetch Jira Requirements

> **BẮT BUỘC (MANDATORY SKILL):** Bạn PHẢI nạp và đọc kỹ nội dung của skill **`jira_integration`** (tại `.agent/skills/jira_integration/SKILL.md`) để biết cách sử dụng scripts trước khi bắt đầu.

Workflow này giúp lấy requirements, user stories, hoặc issues từ Jira và chuyển thành tài liệu phục vụ test automation.

## Các bước thực hiện:

1. **Kiểm tra prerequisites:**
   - Đọc skill `jira_integration` để nắm cấu trúc scripts.
   - Kiểm tra file `.env` đã tồn tại và được cấu hình đúng.
   - Kiểm tra dependencies đã được cài đặt (`scripts/integrations/node_modules/`).
   - Nếu chưa cài, chạy: `cd scripts/integrations && npm install`

2. **Xác định thông tin cần lấy:**
   - Hỏi user cung cấp thông tin:
     - **Issue key** cụ thể (VD: `PROJ-123`) → dùng `--issue`
     - **Project key + Issue type** (VD: `PROJ`, `Story`) → dùng `--project --type`
     - **JQL query** tùy chỉnh → dùng `--jql`
     - **Epic key** (lấy children) → dùng `--epic`
   - Xác định format output: `json` (default) hoặc `md` (markdown requirement)

3. **Thực thi script:**
   - Chạy lệnh phù hợp:
   ```bash
   # Lấy 1 issue cụ thể
   node scripts/integrations/jira/jira_fetcher.js --issue <ISSUE_KEY>

   # Lấy issues theo project
   node scripts/integrations/jira/jira_fetcher.js --project <PROJECT_KEY> --type <TYPE> --max <N>

   # Tìm theo JQL
   node scripts/integrations/jira/jira_fetcher.js --jql "<JQL_QUERY>"

   # Xuất Markdown
   node scripts/integrations/jira/jira_fetcher.js --issue <KEY> --format md --output ./requirements/jira
   ```

4. **Xử lý kết quả:**
   - Kiểm tra output file được tạo trong `requirements/jira/` (hoặc `--output` chỉ định).
   - Nếu format `json`: Đọc và hiển thị tóm tắt issues cho user.
   - Nếu format `md`: Hiển thị nội dung markdown requirement cho user review.
   - Nếu gặp lỗi: Đọc log, phân tích nguyên nhân theo bảng Troubleshooting trong skill.

5. **Xử lý lỗi thường gặp:**
   - **HTTP 401**: Token sai → hướng dẫn user kiểm tra `JIRA_API_TOKEN` hoặc `JIRA_PAT`
   - **HTTP 404**: Issue không tồn tại hoặc `JIRA_BASE_URL` sai
   - **File .env not found**: Hướng dẫn user copy `.env.example` → `.env`
   - **Module not found**: Chạy `npm install` trong `scripts/integrations/`

6. **Delivery:**
   - Trình bày kết quả bằng Tiếng Việt.
   - Nếu user yêu cầu chuyển thành requirement document, sử dụng skill `requirements_analyzer` để format lại.
   - Lưu file output vào thư mục phù hợp (`requirements/jira/`).
