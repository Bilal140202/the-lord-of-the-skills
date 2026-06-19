---
description: Phân tích automation tests không ổn định (flaky), xác định root cause và tự động khắc phục. Hỗ trợ 2 mode — ANALYZE (chỉ báo cáo) và FIX (báo cáo + tự sửa code).
skills:
  - flaky_test_analyzer
  - smart_locator_agent
  - locator_healer_agent
---

# Workflow: Phân Tích & Khắc Phục Flaky Tests

> **BẮT BUỘC (MANDATORY SKILL):** Bạn PHẢI nạp và đọc kỹ nội dung của skill **`flaky_test_analyzer`** (tại `.agent/skills/flaky_test_analyzer/SKILL.md`) trước khi bắt đầu. Ngoài ra, tham khảo thêm skill **`smart_locator_agent`** và **`locator_healer_agent`** khi cần sửa/thay locator.

Workflow này giúp agent tự động phân tích các automation test không ổn định (lúc pass lúc fail), xác định root cause chính xác, và (tùy mode) tự động sửa code để stabilize test.

## ⚠️ Nguyên tắc thực thi

- **Tất cả output bằng Tiếng Việt**
- **KHÔNG đoán** nguyên nhân — phải phân tích log, code, và DOM thực tế
- **Phải chờ user xác nhận** danh sách fix tại Bước 3 trước khi sửa code (Mode FIX)
- Nếu user chưa cung cấp test file/error log → hỏi trước khi bắt đầu
- ⚠️ Sau khi user xác nhận fix → agent tự sửa + verify, KHÔNG hỏi lại trong quá trình fix

## 2 Chế độ (Mode)

| Mode | Khi nào sử dụng | Output |
|---|---|---|
| **ANALYZE** (mặc định) | User cần hiểu nguyên nhân flaky, chưa muốn sửa code | Báo cáo phân tích + Đề xuất fix |
| **FIX** | User muốn agent tự sửa code luôn | Như ANALYZE + Code đã sửa + Kết quả verify |

> Nếu user nói "sửa luôn", "fix giùm", "khắc phục test này", hoặc yêu cầu agent sửa code → tự động chuyển sang **Mode FIX**.

## Input cần thu thập

Agent cần ít nhất **1 trong các input** sau từ user:

| Input | Cách lấy | Độ ưu tiên |
|---|---|---|
| **Test file path** | User cung cấp hoặc agent tìm trong project | ⭐ Bắt buộc |
| **Error log / stack trace** | User paste hoặc agent chạy test để thu thập | ⭐ Bắt buộc |
| **CI/CD log** | User cung cấp URL hoặc file log | Tùy chọn |
| **Test report** (HTML/JSON) | Playwright report, Allure, TestNG report | Tùy chọn |
| **Lịch sử fail** | Số lần fail / tổng số lần chạy | Tùy chọn |

## Các bước thực hiện

### Bước 1: Thu thập thông tin & Tái hiện lỗi (Detect & Reproduce)

1. **Đọc test file** bằng `view_file`:
   - Xác định framework (Playwright / Selenium / Appium / Pytest / TestNG)
   - Ghi nhận cấu trúc: Page Objects, fixtures, helper functions
   - Đánh dấu các vùng code nghi ngờ (waits, locators, assertions, setup/teardown)

2. **Chạy test** để tái hiện lỗi (nếu chưa có error log):
   - Chạy test **3 lần liên tiếp** bằng `run_command`:
     ```bash
     # Playwright
     npx playwright test <test_file> --retries=0 --reporter=list

     # Pytest
     python -m pytest <test_file> -v --count=3

     # Maven/TestNG
     mvn test -Dtest=<TestClass> -Dsurefire.rerunFailingTestsCount=0
     ```
   - Ghi nhận pattern: Fail lần nào? Fail ở step nào? Error message giống hay khác nhau?

3. **Thu thập evidence:**
   - Error log / stack trace từ mỗi lần chạy
   - Screenshots (nếu test có capture on failure)
   - Console log / Network log (nếu liên quan đến API calls)

### Bước 2: Phân tích Root Cause (Inspect & Classify)

1. **Đọc error log** và phân loại theo bảng root cause:

| Category | Dấu hiệu nhận biết | Ví dụ Error |
|---|---|---|
| 🎯 **Locator không ổn định** | `ElementNotFound`, `No matching element`, selector chứa dynamic class/index | `Locator('.css-1a2b3c')` fail vì class thay đổi mỗi build |
| ⏱️ **Timing / Race condition** | `Timeout`, `Element not visible`, test pass khi chạy chậm (debug mode) | `expect(element).toBeVisible()` timeout vì animation chưa xong |
| 📊 **Test data conflict** | `Duplicate key`, `Already exists`, fail khi chạy parallel | 2 test cùng tạo user `test@email.com` |
| 🔄 **State dependency** | Pass khi chạy độc lập, fail khi chạy cùng suite | Test B phụ thuộc data mà Test A tạo ra |
| 🌐 **Environment / Network** | `ECONNREFUSED`, `503`, `CORS error`, fail trên CI nhưng pass local | API server chậm, CDN timeout |
| 🖼️ **UI Animation / Transition** | `Element is not clickable`, `intercept`, fail ngẫu nhiên khi click | Modal animation chưa hoàn thành, overlay che button |
| 📱 **Viewport / Responsive** | Element bị ẩn, scroll không tới, fail ở resolution khác | Button nằm ngoài viewport trên CI (headless 800x600) |
| 🧹 **Cleanup / Teardown** | Fail ở lần chạy thứ 2+, pass lần đầu | Test không cleanup data → lần sau bị conflict |

2. **Inspect code** chi tiết, kiểm tra từng anti-pattern:

   **Locator check:**
   - [ ] Có dùng dynamic class (`css-xxx`, `sc-xxx`, `MuiXxx-root`)? → ❌
   - [ ] Có dùng positional xpath (`//div[3]/button[2]`)? → ❌
   - [ ] Locator có unique không? (kiểm tra trên DOM thực tế nếu cần)

   **Wait strategy check:**
   - [ ] Có `waitForTimeout()` / `Thread.sleep()` / `time.sleep()`? → ❌
   - [ ] Có `waitForSelector()` khi `expect()` đã đủ? → ⚠️
   - [ ] Assertion có timeout phù hợp không?

   **Test data check:**
   - [ ] Data có hardcoded không? (`test@email.com`, `user123`)
   - [ ] Data có unique per run không? (timestamp / random)
   - [ ] Có cleanup data sau test không?

   **Test independence check:**
   - [ ] Test có phụ thuộc thứ tự chạy không?
   - [ ] Test có share state qua global variable không?
   - [ ] Setup/Teardown có đầy đủ không?

3. **Nếu cần inspect DOM thực tế** (locator issue):
   - Mở browser bằng MCP: `browser_navigate` → `browser_resize(1920, 1080)` → `browser_snapshot`
   - So sánh locator trong code vs DOM thực tế
   - Xác định locator thay thế ổn định hơn (dùng skill `smart_locator_agent`)

### Bước 3: Lập báo cáo & Đề xuất fix (Report — CHECKPOINT)

1. **Tạo artifact** `flaky_analysis.md` với cấu trúc:

   ```markdown
   # Báo Cáo Phân Tích Flaky Test

   ## Tổng quan
   - **Test file:** <path>
   - **Framework:** Playwright / Selenium / ...
   - **Tần suất fail:** X/Y lần chạy
   - **Mức độ nghiêm trọng:** 🔴 Critical / 🟡 Medium / 🟢 Low

   ## Root Cause Analysis

   | # | Vị trí (Line) | Category | Mô tả vấn đề | Mức độ |
   |---|---|---|---|---|
   | 1 | test.ts:45 | ⏱️ Timing | waitForTimeout(3000) thay vì smart wait | 🔴 |
   | 2 | page.ts:12 | 🎯 Locator | .css-1abc dynamic class | 🟡 |

   ## Đề xuất Fix

   | # | Vấn đề | Code hiện tại | Code đề xuất | Lý do |
   |---|---|---|---|---|
   | 1 | Hard sleep | `waitForTimeout(3000)` | `expect(el).toBeVisible()` | Smart wait tự retry |
   | 2 | Dynamic class | `.css-1abc` | `getByRole('button', {name: 'Submit'})` | Semantic, không phụ thuộc CSS |
   ```

2. **⏸️ DỪNG LẠI — Trình bày cho user review:**
   - Danh sách root causes đã xác định
   - Bảng đề xuất fix (code cũ → code mới)
   - Hỏi: "Bạn đồng ý với phân tích này không? Tôi tiến hành sửa code luôn hay chỉ cần báo cáo?"

3. Nếu user chọn **Mode ANALYZE** → **KẾT THÚC** tại đây
4. Nếu user đồng ý fix → chuyển sang Bước 4

### Bước 4: Tự động sửa code (Auto-Fix — Mode FIX)

> Chỉ thực hiện khi ở **Mode FIX** và user đã xác nhận

1. **Sửa code** theo thứ tự ưu tiên (fix nghiêm trọng nhất trước):

   **Fix Locator:**
   - Dùng skill `locator_healer_agent` để thay thế locator hỏng
   - Tuân thủ locator priority trong `.agent/rules/locator_strategy.md`
   - Verify locator mới trên DOM thực tế trước khi commit vào code

   **Fix Timing:**
   ```
   ❌ page.waitForTimeout(3000)
   ✅ await expect(page.getByRole('button')).toBeVisible()

   ❌ Thread.sleep(5000)
   ✅ wait.until(ExpectedConditions.visibilityOfElementLocated(...))
   ```

   **Fix Test Data:**
   ```
   ❌ const email = "test@email.com"
   ✅ const email = `auto_${Date.now()}@test.com`
   ```

   **Fix Test Independence:**
   - Thêm setup/teardown để tạo và cleanup data riêng
   - Loại bỏ dependency giữa các test cases
   - Đảm bảo mỗi test tự tạo precondition riêng

2. **Sử dụng** `replace_file_content` hoặc `multi_replace_file_content` để áp dụng thay đổi
3. **Ghi chú** mỗi thay đổi vào artifact `flaky_analysis.md`

### Bước 5: Verify & Đảm bảo ổn định (Verify Stability)

> Chỉ thực hiện khi ở **Mode FIX**

1. **Chạy test 3 lần liên tiếp** sau khi fix:
   ```bash
   # Playwright
   npx playwright test <test_file> --retries=0 --repeat-each=3

   # Pytest
   python -m pytest <test_file> -v --count=3

   # Maven
   mvn test -Dtest=<TestClass> (chạy 3 lần thủ công)
   ```

2. **Đánh giá kết quả:**

   | Kết quả | Hành động |
   |---|---|
   | ✅ **3/3 PASS** | Test đã ổn định → cập nhật artifact, báo cáo thành công |
   | ⚠️ **2/3 PASS** | Vẫn còn flaky → quay lại Bước 2 phân tích lần fail, fix tiếp (tối đa 3 vòng) |
   | ❌ **0-1/3 PASS** | Fix sai hướng → rollback, phân tích lại root cause |

3. **Stability Checklist** (phải đạt toàn bộ trước khi kết thúc):
   - [ ] Locator unique và ổn định qua nhiều lần reload
   - [ ] Không có hard sleep / fixed delay
   - [ ] Test data unique + traceable mỗi lần chạy
   - [ ] Test độc lập — không phụ thuộc thứ tự chạy
   - [ ] Test pass **3+ lần liên tiếp**
   - [ ] Không còn debug log / commented code

4. **Cập nhật artifact** `flaky_analysis.md`:
   - Thêm section "Kết quả sau fix" với bảng kết quả chạy
   - Đánh dấu trạng thái: ✅ STABILIZED / ⚠️ PARTIALLY FIXED / ❌ STILL FLAKY

## Xử lý các tình huống đặc biệt

| Tình huống | Cách xử lý |
|---|---|
| **Test chỉ fail trên CI** | So sánh env CI vs local (viewport, timezone, headless, resources). Kiểm tra viewport `1920x1080` có được set trên CI không |
| **Test fail khi chạy parallel** | Kiểm tra test data isolation, shared state, database locks. Đề xuất unique data per worker |
| **Test fail sau deploy mới** | Kiểm tra DOM changes, API response changes. Dùng `locator_healer_agent` để update locators |
| **Test fail ngẫu nhiên không pattern** | Thu thập thêm data (chạy 10+ lần), kiểm tra memory leak, resource exhaustion |
| **Multiple tests cùng flaky** | Tìm common factor (shared fixture, shared page object, shared config) |
| **Test fail do external API** | Đề xuất mock/stub external dependencies, retry logic cho API calls |

## Output

### Mode ANALYZE
- Artifact `flaky_analysis.md`:
  - Tổng quan test (file, framework, tần suất fail)
  - Root Cause Analysis (bảng phân loại)
  - Đề xuất fix chi tiết (code cũ → code mới)
  - Stability checklist

### Mode FIX
- Tất cả output của Mode ANALYZE, cộng thêm:
  - Code đã được sửa (các file đã thay đổi)
  - Kết quả verify (3 lần chạy PASS/FAIL)
  - Trạng thái cuối: STABILIZED / PARTIALLY FIXED / STILL FLAKY