---
description: Phân tích requirement document (Jira ticket, .doc, user story) — sinh tài liệu phân tích chi tiết, KHÔNG sinh test cases.
skills:
  - requirements_analyzer
---

> **BẮT BUỘC (MANDATORY SKILL):** Bạn PHẢI nạp và đọc kỹ nội dung của skill **`requirements_analyzer`** (tại `.agent/skills/requirements_analyzer/SKILL.md`) để hiểu cách phân tích yêu cầu chuẩn trước khi bắt đầu.

# Workflow: Phân Tích Requirement Document

Workflow này phân tích requirement documents (Jira tickets, .doc files, user stories, design mockups) và sinh ra một tài liệu phân tích chi tiết. **KHÔNG sinh test cases** — chỉ tập trung vào hiểu, phân rã, và phát hiện rủi ro/mơ hồ trong yêu cầu.

## Khi nào sử dụng

- User cung cấp Jira ticket (.doc) hoặc requirement document và yêu cầu "phân tích"
- User muốn hiểu rõ scope, acceptance criteria, và dependencies trước khi viết test
- User cần danh sách các điểm mơ hồ (ambiguities) để clarify với PO/BA
- User nói: "phân tích requirement", "review yêu cầu", "analyze this ticket"

## Đầu vào (Input)

Agent cần thu thập từ user:

| # | Input | Bắt buộc | Mô tả |
|---|---|---|---|
| 1 | **Requirement document** | ✅ | File .doc, .md, URL Jira, hoặc text mô tả yêu cầu |
| 2 | **Mockup/Screenshot** | ⭕ Khuyến khích | Hình ảnh UI design, wireframe, hoặc screenshot hiện tại |
| 3 | **Related tickets** | ⭕ Tùy chọn | Các ticket phụ thuộc hoặc liên quan (dependencies) |
| 4 | **Context bổ sung** | ⭕ Tùy chọn | Thông tin về hệ thống hiện tại, business domain |

> [!NOTE]
> Nếu user chỉ cung cấp file .doc mà không có mockup, agent vẫn phải phân tích đầy đủ dựa trên nội dung document. Nếu có mockup/screenshot, agent phân tích UI chi tiết hơn.

## Các bước thực hiện

### Bước 1: Thu thập và đọc hiểu (Information Gathering)

1. **Đọc requirement document** được user cung cấp (file .doc, .md, hoặc URL)
   - Nếu file .doc format HTML (export từ Jira): parse HTML để trích xuất nội dung
   - Xác định: Ticket ID, Type, Priority, Status, Reporter, Assignee, Fix Version, Sprint, Labels
2. **Đọc mockup/screenshot** nếu có — phân tích UI layout, components, fields
3. **Kiểm tra related tickets** nếu có trong cùng thư mục hoặc được user cung cấp
   - Đọc và tóm tắt dependencies
4. **Xác nhận** đã nắm được bối cảnh → tiếp tục phân tích

### Bước 2: Trích xuất thông tin cốt lõi (Core Analysis)

1. **Tổng quan Ticket** — Bảng metadata (ID, Type, Priority, Status, Sprint, Assignee...)
2. **User Story** — Trích xuất format "As a... I want... So that..."
3. **Phạm vi áp dụng (Scope)** — Xác định rõ các module/page/component bị ảnh hưởng
4. **Acceptance Criteria** — Phân rã từng AC thành các nhóm logic, bao gồm:
   - Mô tả chi tiết từng AC
   - Bảng so sánh (nếu có cột mới, field mới, rule mới)
   - Phân biệt rõ **mặc định vs tùy chọn** (nếu applicable)

### Bước 3: Phân tích UI từ Mockup (nếu có)

Nếu user cung cấp mockup/screenshot:

1. **Mô tả layout** — Breadcrumb, header, sidebar, main content, footer
2. **Liệt kê components** — Tables, forms, modals, buttons, dropdowns, tabs
3. **Chi tiết fields** — Tên field, loại (input/dropdown/date picker), label, placeholder
4. **So sánh** mockup với document — phát hiện inconsistency
5. **Chụp quan sát** vào carousel trong artifact (nếu hình có sẵn)

### Bước 4: Phân tích Dependencies (Phụ thuộc)

1. Xác định các ticket/feature liên quan (referenced trong AC hoặc comments)
2. Đọc và tóm tắt nội dung ticket phụ thuộc
3. Nếu có mockup riêng cho dependency → phân tích UI chi tiết (fields, modals, interactions)
4. Tổng hợp **Business Rules** từ tất cả requirements + mockups
5. Đánh dấu rõ quy tắc nào từ ticket chính vs ticket phụ thuộc

### Bước 5: Phát hiện Ambiguities & Risks (Trọng tâm)

> [!IMPORTANT]
> Đây là phần **giá trị cao nhất** của workflow — phát hiện những gì requirement KHÔNG nói rõ.

**5.1. Điểm mơ hồ (Ambiguities):**

Với mỗi ambiguity, ghi rõ:
- **Mã:** AMB-XX (đánh số tuần tự)
- **Câu hỏi:** Mô tả rõ ràng điều gì chưa rõ
- **Nguy cơ:** Impact nếu không được giải quyết
- **Mức độ:** 🔴 High / 🟡 Medium / 🟢 Low

Các hướng phát hiện ambiguity:
- Từ khóa mơ hồ: "where applicable", "as needed", "similar to", "etc."
- Validation rules thiếu: min/max, format, required/optional
- Hành vi edge case: lỗi mạng, concurrent access, trống data
- Inconsistency giữa document và mockup (tên cột, format, layout)
- Threshold/config chưa xác định (ví dụ: bao nhiêu ngày = "approaching deadline"?)
- Conflict giữa requirements cũ và mới

**5.2. Rủi ro kiểm thử (Testing Risks):**

Với mỗi risk, ghi rõ:
- **Mã:** RISK-XX
- **Tên rủi ro**
- **Mô tả**
- **Mitigation** (cách giảm thiểu)

### Bước 6: Tổng hợp và trình bày (Synthesis & Delivery)

1. **Ma trận trạng thái** (nếu có state transitions) — bảng mapping trạng thái → hành vi
2. **Checklist AC** — Tóm tắt tất cả AC dạng checkbox, nhóm theo chức năng
3. **Khuyến nghị kiểm thử** — Gợi ý top 10 điều cần quan tâm nhất khi test
4. **Xuất Artifact** — Lưu toàn bộ phân tích vào file `.md`

## Cấu trúc Output (Template Artifact)

Agent PHẢI xuất artifact theo cấu trúc sau:

```markdown
# 📋 Phân Tích Requirement: [TICKET-ID]
## [Ticket Title]

## 1. Tổng Quan Ticket
(Bảng metadata)

## 2. User Story
(As a... I want... So that...)

## 3. Phạm Vi Áp Dụng (Scope)
(Bảng liệt kê modules/pages bị ảnh hưởng)

## 4. Acceptance Criteria — Phân Tích Chi Tiết
### 4.1. [Nhóm AC 1]
### 4.2. [Nhóm AC 2]
### 4.N. [Nhóm AC N]

## 5. Phụ Thuộc (Dependencies)
### 5.1. [Ticket phụ thuộc]
#### 5.1.1. [Chi tiết UI nếu có mockup]
#### 5.1.N. Business Rules tổng hợp

## 6. Phân Tích Mockup/Screenshot
### 6.1. [Mockup 1]
### 6.N. [Mockup N]

## 7. Các Điểm Mơ Hồ & Rủi Ro
### 7.1. Điểm Mơ Hồ (Ambiguities)
(Bảng: #, Câu hỏi, Nguy cơ, Mức độ)
### 7.2. Rủi Ro Kiểm Thử
(Bảng: #, Rủi ro, Mô tả, Mitigation)

## 8. Ma Trận Trạng Thái (nếu applicable)
(Bảng state → behavior)

## 9. Tóm Tắt Acceptance Criteria (Checklist)
(Checkbox nhóm theo chức năng)

## 10. Khuyến Nghị Cho Kiểm Thử
(Danh sách gợi ý, KHÔNG phải test cases)
```

## Quy tắc quan trọng

- ❌ **KHÔNG sinh test cases** — workflow này chỉ phân tích, không tạo TC
- ❌ **KHÔNG tự đoán** business logic nếu document không nói rõ → đưa vào Ambiguities
- ❌ **KHÔNG bỏ qua comments** trong Jira ticket — comments thường chứa thông tin quan trọng bổ sung
- ✅ **PHẢI đọc related tickets** nếu được reference trong AC
- ✅ **PHẢI phân tích mockup** chi tiết nếu được cung cấp (fields, layout, interactions)
- ✅ **PHẢI ghi rõ inconsistency** giữa document và mockup
- ✅ **PHẢI viết bằng Tiếng Việt**, format Markdown, xuất Artifact
- ✅ **PHẢI copy hình ảnh** vào thư mục artifacts nếu cần embed trong artifact

## Mối quan hệ với workflows khác

| Sau khi phân tích xong | Workflow tiếp theo |
|---|---|
| Cần sinh test cases nhanh | `/generate_testcases_from_requirements` |
| Cần sinh test cases bài bản (RBT 6 bước) | `/generate_manual_testcases_rbt` |
| Cần sinh automation scripts | `/generate_automation_from_testcases` |
| Cần phân tích cross-module | `/generate_cross_module_test_plan` |
