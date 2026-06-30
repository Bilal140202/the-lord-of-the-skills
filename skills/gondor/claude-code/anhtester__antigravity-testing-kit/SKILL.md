---
name: RBT Manual Testing
description: Skill sinh manual test cases với 2 modes — QUICK (sinh nhanh từ requirements) và FULL RBT (quy trình AI-RBT 6 bước có đánh giá rủi ro). Master skill cho mọi tác vụ manual test case.
---

# RBT Manual Testing

## Description

Đây là **Master Skill** cho mọi tác vụ sinh manual test cases. Skill cung cấp **2 chế độ hoạt động** (modes) để phù hợp với mọi quy mô yêu cầu:

| Mode | Khi nào dùng | Thời gian |
|------|-------------|-----------|
| **QUICK** | Module đơn giản, cần TC nhanh, requirements rõ ràng | 1 lượt (không chờ user) |
| **FULL RBT** | Module phức tạp, cần phân tích rủi ro, hệ thống lớn | 6 bước tuần tự (có checkpoint) |

**Nguyên tắc cốt lõi:**
- **Human Strategy:** Con người xác định chiến lược, mức độ rủi ro và tiêu chuẩn
- **AI Execution:** AI thực hiện phân tích, viết TCs và rà soát lỗ hổng
- **Human Verification:** Con người kiểm tra lại kết quả trước khi chốt

---

## When to Use

Sử dụng skill này khi:

- Sinh manual test cases từ requirements / user stories
- Phân tích requirements để phát hiện ambiguity
- Phân rã hệ thống thành modules / features
- Xây dựng traceability matrix
- Áp dụng Risk-Based Testing (đánh giá rủi ro cho test cases)
- Chuẩn hóa test cases sang bảng Markdown (Jira/Excel format)
- Sinh test cases nhanh từ requirements đơn giản

**KHÔNG** sử dụng skill này khi:

- Cần sinh automation code → dùng `qa_automation_engineer`
- Cần inspect DOM / sinh locator → dùng `ui_debug_agent` / `smart_locator_agent`
- Chỉ cần sinh test data → dùng `test_data_generator`

---

## Mode Routing — Cách chọn mode

Agent tự động chọn mode dựa trên **trigger keywords** và **ngữ cảnh**:

### → Mode QUICK

Kích hoạt khi:
- User dùng workflow `/generate_testcases_from_requirements`
- User nói: "sinh test cases nhanh", "tạo TC từ requirement này", "viết test cases cho form..."
- Requirements đã rõ ràng, scope nhỏ (1 module / 1 tính năng)
- User không yêu cầu phân tích rủi ro hay quy trình bài bản

### → Mode FULL RBT

Kích hoạt khi:
- User dùng workflow `/generate_manual_testcases_rbt`
- User nói: "quy trình 6 bước", "phân tích RBT", "sinh test cases đầy đủ", "sinh bộ TC bài bản"
- Scope lớn (nhiều modules, hệ thống phức tạp)
- User yêu cầu Traceability Matrix hoặc đánh giá Risk Level
- Requirements chưa rõ ràng, cần phân tích Ambiguity

### → Khi không rõ

Nếu không xác định được mode, agent **hỏi user**:
```
Bạn muốn sinh test cases theo chế độ nào?
1. QUICK — Sinh nhanh từ requirements (không qua bước phân tích)
2. FULL RBT — Quy trình 6 bước đầy đủ (phân tích → phân rã → RBT → sinh TC)
```

---

# Mode 1: QUICK — Sinh Test Cases Nhanh

## Mục đích

Sinh test cases **nhanh, đủ chất lượng** từ requirements/user stories đã rõ ràng, phù hợp cho module đơn giản hoặc khi cần kết quả ngay.

## Quy trình (1 lượt duy nhất)

**Agent phải:**

1. **Đọc và hiểu requirements** được cung cấp
2. **Xác định các luồng chính:**
   - Happy Path (luồng chính)
   - Negative Path (dữ liệu sai, thiếu)
   - Boundary Cases (giá trị biên)
3. **Áp dụng kỹ thuật thiết kế test case** tự động:
   - **Equivalence Partitioning (EP):** Chia input thành nhóm tương đương
   - **Boundary Value Analysis (BVA):** Test giá trị tại ranh giới
   - **Decision Table:** Liệt kê tổ hợp điều kiện (nếu có nhiều rules)
   - **State Transition:** Test chuyển đổi trạng thái (nếu có workflow)
4. **Validation chuyên biệt từng trường (Field-Level Validation):**
   - Liệt kê **tất cả input fields** trên form/UI
   - Sinh validation test cases **riêng cho TỪNG trường** theo đặc tính riêng của nó
   - Áp dụng checklist validation theo loại field (xem bảng Field-Level Validation bên dưới)
   - **KHÔNG** gộp validation nhiều trường vào 1 test case
5. **Sinh test cases** với đầy đủ fields:
   - TC ID (format: `[DỰ_ÁN]_[MODULE]_TC_[SỐ]`)
   - Module
   - Test Case Title / Test Scenario
   - Pre-conditions
   - Test Steps (đánh số)
   - Expected Results (đánh số tương ứng)
   - Test Data (**phải cụ thể**, không placeholder)
   - Priority (Critical / High / Medium / Low)
6. **Xuất ra bảng Markdown** chuẩn, sẵn sàng copy sang Excel/Jira

## Bảng Output

```
| TC ID | Module | Test Scenario | Pre-Condition | Test Steps | Test Data | Expected Result | Priority |
```

## Quy tắc Test Data (áp dụng cho cả 2 modes)

```
❌ Sai: "Nhập mã số hợp lệ"
✅ Đúng: "Nhập mã: KH-2026-0012"

❌ Sai: "Nhập email hợp lệ"
✅ Đúng: "Nhập email: test_khachhang_01@domain.com"

❌ Sai: "Nhập giá trị vượt giới hạn"
✅ Đúng: "Nhập 256 ký tự vào trường Name (max: 255)"
```

## Bảng Field-Level Validation (áp dụng cho cả 2 modes)

Khi form/UI có các input fields, agent **BẮT BUỘC** phải liệt kê từng trường và sinh validation TCs riêng theo loại:

| Loại Field | Validation cần test |
|---|---|
| **Text (Name, Address...)** | Required/Optional · Min length · Max length · Chỉ khoảng trắng (whitespace-only) · Ký tự đặc biệt (`<>&"'`) · XSS injection (`<script>alert(1)</script>`) · SQL injection (`' OR 1=1--`) · Unicode/Emoji · Leading/trailing spaces |
| **Email** | Format hợp lệ (`user@domain.com`) · Thiếu `@` · Thiếu domain · Domain không hợp lệ · Nhiều `@` · Ký tự đặc biệt trước `@` · Max length · Case sensitivity · Email đã tồn tại (nếu unique) |
| **Phone** | Chỉ chấp nhận số · Prefix hợp lệ (ví dụ: `+84`, `0`) · Min/Max length · Chữ cái xen lẫn · Dấu `-`, `.`, khoảng trắng · Mã vùng không hợp lệ |
| **Date / DateTime** | Format đúng (dd/MM/yyyy, ISO...) · Ngày không tồn tại (`31/02`, `30/02`) · Năm nhuận (`29/02/2024`) · Ngày quá khứ / tương lai (tùy business rule) · Giá trị min/max date · Timezone (nếu áp dụng) |
| **Number / Currency** | Min/Max value · Số âm · Số 0 · Số thập phân · Ký tự không phải số · Overflow (số cực lớn) · Leading zeros · Định dạng currency (dấu phẩy, dấu chấm) |
| **Dropdown / Select** | Giá trị mặc định · Tất cả options hợp lệ · Option bị disabled · Thay đổi selection · Required validation (chưa chọn) |
| **Checkbox / Radio** | Trạng thái mặc định · Check/Uncheck · Required validation · Nhóm radio (chỉ chọn 1) |
| **File Upload** | File type hợp lệ/không hợp lệ · Max size · File rỗng (0 KB) · Tên file có ký tự đặc biệt · Multiple files (nếu cho phép) · Kéo thả vs nút chọn |
| **Password** | Min/Max length · Yêu cầu ký tự đặc biệt · Yêu cầu chữ hoa/thường · Yêu cầu số · Copy-paste bị chặn? · Hiện/ẩn password · Confirm password khớp/không khớp |
| **Textarea** | Max length · Line breaks · HTML tags · Resize (nếu UI cho phép) · Character counter (nếu có) |

> **Nguyên tắc:** Mỗi trường có đặc tính riêng → validation riêng. Agent PHẢI phân tích từng field trước khi sinh TCs, không được dùng chung 1 bộ validation cho tất cả fields.

## Anti-Patterns (Mode QUICK)

- ❌ Sinh test data chung chung / placeholder
- ❌ Chỉ có Happy Path, thiếu Negative/Boundary
- ❌ Bỏ qua validation rules trong requirements
- ❌ Test Steps mơ hồ ("nhập dữ liệu" → phải ghi rõ nhập gì, ở đâu)
- ❌ Gộp validation nhiều trường vào 1 test case → mỗi trường phải có TC validation riêng
- ❌ Dùng chung 1 bộ validation cho tất cả fields (mỗi field type có checklist riêng)
- ❌ Bỏ qua security validation (XSS, SQL injection) cho text fields

---

# Mode 2: FULL RBT — Quy Trình AI-RBT 6 Bước

## Mục đích

Quy trình bài bản, tuần tự cho module phức tạp. Bao gồm phân tích Ambiguity, phân rã hệ thống, Traceability Matrix, đánh giá Risk Level, và sinh test cases chi tiết.

> ⚠️ **QUAN TRỌNG:** Quy trình này **BẮT BUỘC chạy tuần tự** từng bước. KHÔNG được gộp nhiều bước chạy 1 lần. Mỗi bước phải hoàn thành và được user xác nhận trước khi sang bước tiếp.

> [!NOTE]
> **2 luồng sử dụng riêng biệt:**
> - **Luồng Antigravity (slash command):** Agent thực hiện theo hướng dẫn tổng quát bên dưới. Agent KHÔNG cần đọc file prompt.txt.
> - **Luồng Copy-Paste (ChatGPT/Claude):** QA team copy nội dung prompt chi tiết từ `plans/manual/01-06/prompt.txt` vào chat AI, từng bước một.

### Bước 1: Context & Role-play (Khởi tạo ngữ cảnh)

**Mục đích:** Thiết lập vai trò Senior QA Engineer và nạp bối cảnh dự án.

**Agent phải:**
1. Yêu cầu user cung cấp:
   - Tên dự án / tính năng
   - Mô tả hệ thống hiện tại
   - Mục tiêu kiểm thử MVP
   - Tài liệu yêu cầu (Requirements, User Stories, Figma link, PDF...)
2. Đọc kỹ tài liệu và xác nhận đã hiểu bối cảnh
3. Tóm tắt scope kiểm thử
4. **Chờ user xác nhận** trước khi sang Bước 2

**Output:** Xác nhận hiểu bối cảnh + tóm tắt scope kiểm thử.

---

### Bước 2: Analysis & QnA (Phân tích yêu cầu)

**Mục đích:** Phân tích tài liệu để phát hiện điểm mờ, thiếu sót, mâu thuẫn.

**Agent phải:**
1. Xác định các luồng:
   - Happy Path (luồng chính)
   - Alternate Paths (luồng rẽ nhánh)
   - Exception Paths (luồng ngoại lệ)
2. Phát hiện Ambiguities:
   - Yêu cầu thiếu sót (không quy định độ dài textbox, timeout, hành vi mất kết nối...)
   - Yêu cầu mâu thuẫn
   - Yêu cầu chưa rõ ràng
3. Đặt câu hỏi Q&A có đánh số thứ tự (Q1, Q2...) cho user/PO/BA giải đáp, mỗi câu kèm ngữ cảnh và assumption nếu không được trả lời
4. **DỪNG LẠI — Chờ user trả lời** các câu hỏi trước khi tiếp tục

**Output:** Danh sách luồng + Ambiguities + Câu hỏi Q&A.

> [!IMPORTANT]
> **Đây là điểm nghẽn quan trọng nhất.** Nếu agent bỏ qua bước này và tự đoán logic, test cases sẽ sai nghiêm trọng. Agent PHẢI dừng lại và đợi user phản hồi.

---

### Bước 3: Decomposition (Phân rã hệ thống)

**Mục đích:** Chia tính năng phức tạp thành các Module / Sub-module nhỏ, dễ quản lý.

**Agent phải:**
1. Phân rã theo 1 trong 2 cách:
   - **Theo UI:** Header, Data Table, Form popup, Sidebar...
   - **Theo luồng:** Flow tạo mới, Flow chỉnh sửa, Flow xóa...
2. Mô tả ngắn gọn chức năng từng Module
3. Chỉ ra Dependencies giữa các Module

**Output:** Danh sách Modules/Sub-modules + Dependencies.

---

### Bước 4: Traceability (Đảm bảo độ bao phủ)

**Mục đích:** Thiết lập ma trận truy vết để đảm bảo 100% requirements được phủ test scenarios.

**Agent phải:**
1. Map mỗi Module/Rule với mã Yêu cầu (REQ-01, REQ-02...)
2. Cross-check xem có yêu cầu nào bị thiếu trong danh sách phân rã (Gap Analysis)
3. Liệt kê High-Level Test Scenarios cho từng Module, tập trung:
   - Security / phân quyền
   - UI Validation
   - Business Logic
   - Data Integrity
   - Error Handling
4. **Chờ user review** danh sách scenarios trước khi sinh test case chi tiết

**Output:** Traceability Matrix + High-Level Test Scenarios.

> [!WARNING]
> **Human Checkpoint:** User cần review danh sách scenarios để bổ sung các trường hợp đặc thù mà AI có thể bỏ sót. Đây là bước đánh giá rủi ro do con người thực hiện.

---

### Bước 5: RBT & TC Generation (Sinh Test Case chi tiết)

**Mục đích:** Sinh test cases chi tiết theo chiến lược Risk-Based Testing.

**Agent phải:**
1. Đánh giá Risk Level cho mỗi Module:
   - **High Risk:** Test kỹ, nhiều cases (nghiệp vụ quan trọng, liên quan tiền, bảo mật)
   - **Medium Risk:** Test vừa phải
   - **Low Risk:** Test cơ bản, happy path
2. Sinh test case với đầy đủ fields:
   - Module / Sub-module
   - Test Case Title
   - Pre-conditions
   - Test Steps (đánh số)
   - Expected Results (đánh số tương ứng)
   - Test Data (**phải cụ thể**, không dùng placeholder chung chung)
   - Priority
3. Bao phủ đa dạng:
   - Happy Path
   - Negative Path (giá trị biên, vượt ký tự)
   - Edge Cases (timeout, mất kết nối...)
4. **Validation chuyên biệt từng trường (Field-Level Validation):**
   - Liệt kê **tất cả input fields** trên form/UI đang test
   - Sinh validation TCs **riêng cho TỪNG trường** theo đặc tính riêng
   - Tham chiếu **Bảng Field-Level Validation** ở phần Mode QUICK để chọn validation phù hợp
   - **KHÔNG** gộp validation nhiều trường vào 1 TC
5. Áp dụng **kỹ thuật thiết kế test case** phù hợp:
   - **Equivalence Partitioning:** Chia input thành nhóm tương đương, test đại diện mỗi nhóm
   - **Boundary Value Analysis (BVA):** Test giá trị tại ranh giới (min, min+1, max-1, max)
   - **Decision Table:** Liệt kê tổ hợp điều kiện → kết quả (cho logic nhiều điều kiện)
   - **State Transition:** Test chuyển đổi trạng thái hợp lệ + không hợp lệ (cho workflow)
6. Nếu scenarios quá nhiều → sinh từng Module một, hỏi user để tiếp tục

**Output:** Danh sách Test Cases chi tiết có Risk Level.

---

### Bước 6: Template Mapping (Chuẩn hóa Format)

**Mục đích:** Đóng gói test cases thành bảng Markdown chuẩn, sẵn sàng copy sang Excel/Jira.

**Agent phải:**
1. Chuẩn hóa toàn bộ test cases vào bảng Markdown:

```
| TC ID | Module | Risk Level | Test Title | Pre-Condition | Test Steps | Expected Result | Priority | Test Data |
```

2. Quy tắc bảng:
   - TC ID theo format thống nhất (ví dụ: `CRM_CUST_TC_001`)
   - Test Steps và Expected Result đánh số, dùng `<br>` xuống dòng trong cell
   - **TUYỆT ĐỐI không được bỏ sót** bất kỳ test case nào đã sinh ở Bước 5
   - Nếu quá dài → chia thành Part 1, Part 2... và hỏi user để tiếp tục
3. Xuất output dưới dạng Artifact (`test_cases_<module>.md`)

**Output:** Bảng Test Cases Markdown hoàn chỉnh.

---

## Anti-Patterns (NGHIÊM CẤM — áp dụng cho cả 2 modes)

- ❌ Gộp nhiều bước chạy 1 lần trong FULL RBT (PHẢI tuần tự)
- ❌ Tự đoán business logic khi chưa hỏi user (Bước 2 - FULL RBT)
- ❌ Bỏ qua bước phân tích Ambiguity (FULL RBT)
- ❌ Sinh test data chung chung / placeholder
- ❌ Rút gọn hoặc bỏ sót test case khi mapping sang bảng
- ❌ Sinh tất cả test cases 1 lần cho hệ thống lớn (phải chia module)
- ❌ Chỉ có Happy Path, thiếu Negative/Boundary cases (QUICK)
- ❌ Test Steps mơ hồ, không ghi rõ dữ liệu nhập
- ❌ Gộp validation nhiều trường vào 1 test case → mỗi trường phải có TC validation riêng
- ❌ Dùng chung 1 bộ validation cho tất cả fields (Email ≠ Phone ≠ Date ≠ Text)
- ❌ Bỏ qua security validation (XSS, SQL injection) cho text/textarea fields
- ❌ Không liệt kê danh sách fields trước khi sinh validation TCs

---

## Prompt Templates

Các prompt template mẫu cho quy trình FULL RBT nằm tại:

```
plans/manual/
├── 01_context_and_roleplay/prompt.txt
├── 02_analysis_and_qna/prompt.txt
├── 03_decomposition/prompt.txt
├── 04_traceability/prompt.txt
├── 05_rbt_and_tc_generation/prompt.txt
└── 06_template_mapping/prompt.txt
```

Agent cần đọc prompt template tương ứng **trước khi** thực hiện mỗi bước (FULL RBT mode).

Mode QUICK không yêu cầu đọc prompt templates — agent áp dụng trực tiếp các kỹ thuật EP/BVA/Decision Table.

---

## Output Format

### Mode QUICK

| Output | Mô tả |
|--------|--------|
| Bảng TC Markdown | Test Cases đầy đủ, sẵn sàng copy sang Excel/Jira |

### Mode FULL RBT

| Bước | Output |
|------|--------|
| 1 | Xác nhận bối cảnh |
| 2 | Luồng + Ambiguities + Câu hỏi Q&A |
| 3 | Module Decomposition + Dependencies |
| 4 | Traceability Matrix + High-Level Scenarios |
| 5 | Test Cases chi tiết (Risk Level + Test Data) |
| 6 | Bảng Markdown chuẩn (Jira/Excel ready) |

Tất cả output phải bằng **Tiếng Việt**, format **Markdown**, sử dụng **Artifact** nếu nội dung dài.
