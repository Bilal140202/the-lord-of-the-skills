# Prompt Templates — Hướng Dẫn Sử Dụng

Thư mục này chứa các **prompt mẫu** dùng nhanh cho từng tác vụ QA cụ thể.
Khác với `plan/` (quy trình 6 bước), các prompt ở đây là **1 lần dùng**, copy → paste → gửi.

---

## Danh Sách Prompt

| # | File | Mục đích | Workflow liên quan |
|---|------|----------|--------------------|
| 01 | [`prompt_01_generate_requirements.txt`](prompt_01_generate_requirements.txt) | Phân tích website sinh Requirements | `/generate_requirements_from_website` |
| 02 | [`prompt_02_generate_test_cases.txt`](prompt_02_generate_test_cases.txt) | Sinh test cases từ requirements | `/generate_testcases_from_requirements` |
| 03 | [`prompt_03_create_framework_playwright.txt`](prompt_03_create_framework_playwright.txt) | Dựng framework Playwright TS từ đầu | `/generate_automation_framework` |
| 03 | [`prompt_03_create_framework_selenium.txt`](prompt_03_create_framework_selenium.txt) | Dựng framework Selenium Java từ đầu | `/generate_automation_framework` |
| 04 | [`prompt_04_generate_script_playwright.txt`](prompt_04_generate_script_playwright.txt) | Viết test script Playwright TS | `/generate_automation_from_testcases` |
| 04 | [`prompt_04_generate_script_selenium.txt`](prompt_04_generate_script_selenium.txt) | Viết test script Selenium Java | `/generate_automation_from_testcases` |
| 05 | [`prompt_05_convert_manual_to_automation.txt`](prompt_05_convert_manual_to_automation.txt) | Chuyển manual TC sang automation | `/generate_automation_from_testcases` |
| 06 | [`prompt_06_review_automation_code.txt`](prompt_06_review_automation_code.txt) | Review code automation | — |
| 07 | [`prompt_07_generate_test_data.txt`](prompt_07_generate_test_data.txt) | Sinh test data có cấu trúc | `/generate_test_data` |
| 08 | [`prompt_08_analyze_flaky_tests.txt`](prompt_08_analyze_flaky_tests.txt) | Phân tích test không ổn định | `/analyze_flaky_tests` |
| 09 | [`prompt_09_generate_api_tests.txt`](prompt_09_generate_api_tests.txt) | Viết test API từ Swagger | `/generate_api_tests_from_swagger` |

## Cách sử dụng

1. Chọn prompt phù hợp với tác vụ
2. Mở file `.txt`
3. Thay thế các phần trong `[...]` bằng dữ liệu thực tế
4. Copy toàn bộ nội dung → paste vào Antigravity chat → gửi

## Khác biệt với plan/

| | `prompt_template/` | `plan/manual/` | `plan/automation/` |
|---|---|---|---|
| Kiểu | 1 prompt dùng 1 lần | 6 bước tuần tự | 6 bước tuần tự |
| Phù hợp | Tác vụ đơn lẻ, nhanh | Sinh TC thủ công chuyên sâu | Xây dựng automation hoàn chỉnh |
| Context | Mỗi prompt độc lập | Cùng 1 conversation | Cùng 1 conversation |
