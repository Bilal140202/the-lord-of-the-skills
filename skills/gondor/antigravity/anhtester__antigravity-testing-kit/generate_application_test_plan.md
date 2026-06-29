---
description: Khám phá ứng dụng web, sinh test plan và test scenarios. Hỗ trợ 2 mode — PLAN (chỉ test plan) và FULL (test plan + automation skeleton).
skills:
  - qa_automation_engineer
  - requirements_analyzer
  - ui_debug_agent
---

# Workflow: Khám Phá Ứng Dụng & Sinh Test Plan

> **BẮT BUỘC (MANDATORY SKILL):** Bạn PHẢI nạp và đọc kỹ nội dung của skill **`qa_automation_engineer`** (tại `.agent/skills/qa_automation_engineer/SKILL.md`) trước khi bắt đầu. Ngoài ra, tham khảo thêm skill **`requirements_analyzer`** và **`ui_debug_agent`** để hỗ trợ phân tích UI.

Workflow này giúp agent tự động khám phá một ứng dụng web, phân tích cấu trúc, xác định các modules/user flows quan trọng, và sinh ra Test Plan hoàn chỉnh.

## ⚠️ Nguyên tắc thực thi

- **Tất cả output bằng Tiếng Việt**
- **KHÔNG đoán** cấu trúc app — phải inspect DOM thực tế qua MCP/browser tools
- **Phải chờ user xác nhận** scope tại Bước 2 trước khi sinh chi tiết
- Nếu user chưa cung cấp URL → hỏi trước khi bắt đầu

## 2 Chế độ (Mode)

| Mode | Khi nào sử dụng | Output |
|---|---|---|
| **PLAN** (mặc định) | User cần khám phá app, lập test plan, xác định scenarios | Modules, User Flows, Test Scenarios, Priority |
| **FULL** | User yêu cầu thêm automation skeleton hoặc nói "full automation suite" | Như PLAN + Manual Test Cases + Automation Skeleton (POM + Test classes) |

> Nếu user nói "generate full automation suite", "bootstrap automation", hoặc yêu cầu code → tự động chuyển sang **Mode FULL**.

## Các bước thực hiện

### Bước 1: Tiếp nhận & Khám phá ứng dụng (Recon)

1. Nhận URL ứng dụng từ user
2. Sử dụng **MCP browser tools** (Playwright MCP) để mở ứng dụng:
   - `browser_navigate` → URL
   - `browser_resize(1920, 1080)` → desktop viewport
   - `browser_snapshot` → thu thập cấu trúc DOM
3. Khám phá **navigation menus**, sidebar, header để xác định các modules chính
4. Lần lượt truy cập từng module chính, dùng `browser_snapshot` để ghi nhận:
   - Tên module / trang
   - Các thành phần UI chính (forms, tables, buttons, modals)
   - Các action có thể thực hiện (CRUD, search, filter, export...)
5. Nếu app yêu cầu đăng nhập → hỏi user cung cấp credentials hoặc dùng fixture sẵn có

### Bước 2: Phân tích & Xác nhận scope (Analysis — CHECKPOINT)

1. Tổng hợp kết quả khám phá thành danh sách:
   - **Modules đã phát hiện** (tên, mô tả ngắn, số lượng features)
   - **User Flows chính** (Happy Path cho mỗi module)
   - **Dependencies** giữa các modules (nếu có)
2. Đánh giá **Risk Level** sơ bộ cho mỗi module:
   - 🔴 **High Risk** — Module core, ảnh hưởng nhiều user, logic phức tạp
   - 🟡 **Medium Risk** — Module phụ trợ, sử dụng thường xuyên
   - 🟢 **Low Risk** — Module ít sử dụng, ít thay đổi
3. **⏸️ DỪNG LẠI — Trình bày cho user review:**
   - Danh sách modules + risk level
   - User flows đã xác định
   - Hỏi user: "Bạn muốn tập trung vào modules nào? Có flow nào cần bổ sung?"
4. **Chờ user xác nhận** scope trước khi sang Bước 3

### Bước 3: Sinh Test Scenarios & Priority

1. Với mỗi module/flow đã được user xác nhận, sinh test scenarios:
   - **Happy Path** — luồng chính thành công
   - **Negative Path** — nhập sai, thiếu dữ liệu, lỗi validation
   - **Edge Cases** — boundary values, concurrent access, empty states
2. Gán **Priority** cho mỗi scenario dựa trên Risk Level:
   - **P1 (Critical)** — Core flows, regression blockers, dữ liệu nhạy cảm
   - **P2 (High)** — Main features, tính năng sử dụng thường xuyên
   - **P3 (Medium)** — Secondary features, UI/UX checks
   - **P4 (Low)** — Nice-to-have, cosmetic checks

### Bước 4: Đóng gói Test Plan (Output — Mode PLAN)

1. Tạo **artifact** `test_plan.md` với cấu trúc:
   - **Tổng quan ứng dụng** — mục đích, tech stack (nếu xác định được), URL
   - **Danh sách Modules** — bảng gồm: Module, Mô tả, Risk Level, Số scenarios
   - **User Flows** — mô tả từng flow chính (steps)
   - **Test Scenarios** — bảng: `| ID | Module | Scenario | Priority | Loại (Happy/Negative/Edge) |`
   - **Automation Candidates** — đánh dấu scenarios nào nên tự động hóa và lý do
2. Nếu user chọn **Mode PLAN** → **KẾT THÚC** tại đây

### Bước 5: Sinh Manual Test Cases (Mode FULL)

> Chỉ thực hiện khi ở **Mode FULL**

1. Chuyển test scenarios (Bước 3) thành **manual test cases đầy đủ**:
   - TC ID, Module, Test Title, Pre-conditions, Test Steps, Expected Results, Test Data, Priority
2. Test Data phải **cụ thể** (không placeholder chung chung)
3. Xuất dưới dạng bảng Markdown trong artifact

### Bước 6: Sinh Automation Skeleton (Mode FULL)

> Chỉ thực hiện khi ở **Mode FULL**

1. Xác định **tech stack** automation (hỏi user nếu chưa rõ):
   - Mặc định: Playwright + TypeScript (hoặc Selenium + Java theo preference)
2. Sinh **Page Object classes** cho mỗi module:
   - Locator thu thập từ DOM thực tế (Bước 1), KHÔNG đoán
   - Methods tương tác rõ nghĩa
3. Sinh **Test class skeleton** cho top-priority scenarios (P1, P2)
4. Đảm bảo tuân thủ **POM pattern** và **locator strategy** theo rules

## Output

### Mode PLAN
- Artifact `test_plan.md` gồm: App overview, Modules, User Flows, Test Scenarios (có Priority), Automation Candidates

### Mode FULL
- Tất cả output của Mode PLAN, cộng thêm:
- Manual Test Cases (bảng Markdown)
- Page Object classes
- Test class skeletons
- Assertions validating expected behavior