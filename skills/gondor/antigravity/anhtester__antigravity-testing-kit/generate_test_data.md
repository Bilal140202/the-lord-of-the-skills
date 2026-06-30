---
description: Sinh test data có cấu trúc, unique, traceable cho test cases. Hỗ trợ UI forms, API payloads, data-driven tests.
skills:
  - test_data_generator
  - qa_automation_engineer
---

# /generate_test_data — Sinh Test Data Có Cấu Trúc

> User cung cấp feature/module hoặc test cases cần sinh data.
> AI phân tích fields, constraints, sinh bộ data đầy đủ (positive, negative, boundary, edge cases) với format sẵn sàng sử dụng.

> **BẮT BUỘC (MANDATORY):** Trước khi bắt đầu, PHẢI nạp và đọc kỹ:
> - **Skill:** `.agent/skills/test_data_generator/SKILL.md` — Quy tắc sinh data
> - **Rule:** `.agent/rules/automation_rules.md` — Section Test Data

---

## Input cần từ User

| Input | Bắt buộc | Mô tả |
|-------|----------|-------|
| Feature / Module | ✅ | VD: "Form đăng ký", "API Create User", "Trang Login" |
| Fields cần data | ⚠️ Nên có | Danh sách fields + constraints. Nếu không có → AI tự phân tích từ DOM/Spec |
| URL trang / Swagger spec | ❌ | Nếu có → AI inspect DOM/Spec để lấy validation rules chính xác |
| Test cases | ❌ | Nếu đã có test cases → AI sinh data match từng TC |
| Output format | ❌ | `json` (mặc định), `csv`, `markdown table`, `code` (TypeScript/Java/Python) |
| Ngôn ngữ data | ❌ | Tiếng Việt / Tiếng Anh (mặc định: theo context) |

---

## Các bước thực hiện

### Bước 1: Phân tích Fields & Constraints

1. **Xác định nguồn thông tin:**

   | Nguồn | Cách lấy | Ưu tiên |
   |-------|----------|---------|
   | User cung cấp trực tiếp | Đọc từ input | ⭐ Cao nhất |
   | DOM thực tế (UI form) | `browser_navigate` → `browser_snapshot` → phân tích input fields | ⭐ Cao |
   | Swagger/OpenAPI spec | `read_url_content` → parse schema + constraints | ⭐ Cao |
   | Test cases đã có | Đọc test steps → trích xuất fields | Trung bình |
   | Đoán từ tên module | Dựa trên kinh nghiệm domain | ⭐ Thấp nhất |

2. **Với mỗi field, xác định:**

   | Attribute | Ví dụ |
   |-----------|-------|
   | **Tên field** | email, password, name, phone |
   | **Kiểu dữ liệu** | string, number, boolean, date, file, enum |
   | **Required?** | Bắt buộc hay tùy chọn |
   | **Validation rules** | min/maxLength, pattern/regex, format (email, phone), unique |
   | **Giá trị mặc định** | Nếu có |
   | **Enum values** | VD: status = ["AVAILABLE", "UNAVAILABLE"] |
   | **Quan hệ phụ thuộc** | VD: `password_confirm` phải khớp `password` |

3. **Trình bày bảng Fields cho User xác nhận (CHECKPOINT ⏸️):**

   ```markdown
   | # | Field | Type | Required | Constraints | Notes |
   |---|-------|------|----------|-------------|-------|
   | 1 | email | string | ✅ | format: email, unique | Dùng để login |
   | 2 | password | string | ✅ | minLength: 6 | |
   | 3 | name | string | ✅ | maxLength: 100 | |
   | 4 | phone | string | ❌ | pattern: /^0[0-9]{9}$/ | 10 chữ số, bắt đầu bằng 0 |
   ```

   > Chờ User xác nhận hoặc bổ sung constraints trước khi sang Bước 2.

---

### Bước 2: Sinh Test Data theo 4 Categories

Với mỗi field đã xác định, sinh data theo bảng sau:

#### 2A. Positive Data (Happy Path)

- Giá trị hợp lệ, đúng format, trong constraints
- Tất cả required fields được điền
- Dữ liệu phải **unique + traceable**

**Format unique data:**
```
<prefix>_<testName>_<timestamp>
```
Ví dụ:
```
email:    auto_register_1712049200@test.com
username: user_login_1712049200
code:     TC_BOOK_1712049200
```

#### 2B. Negative Data

| Loại | Mô tả | Ví dụ |
|------|--------|-------|
| **Missing required** | Bỏ trống field bắt buộc | `email: ""` |
| **Invalid format** | Sai format | `email: "not-an-email"` |
| **Invalid type** | Sai kiểu dữ liệu | `price: "abc"` (expect number) |
| **Duplicate** | Giá trị đã tồn tại | `email: "existing@test.com"` |
| **Invalid characters** | Ký tự không được phép | `name: "<script>alert(1)</script>"` |
| **Wrong relationship** | Vi phạm quan hệ fields | `password_confirm ≠ password` |

#### 2C. Boundary Values

| Loại | Mô tả | Ví dụ (field có minLength=6, maxLength=20) |
|------|--------|-------|
| **Min** | Đúng bằng min | `"abcdef"` (6 chars) |
| **Min - 1** | Dưới min | `"abcde"` (5 chars) |
| **Max** | Đúng bằng max | `"a" * 20` (20 chars) |
| **Max + 1** | Vượt max | `"a" * 21` (21 chars) |
| **Empty** | Chuỗi rỗng | `""` |
| **Zero** | Số 0 (cho number fields) | `0` |
| **Negative** | Số âm (cho number fields) | `-1` |

#### 2D. Edge Cases

| Loại | Mô tả | Ví dụ |
|------|--------|-------|
| **Unicode** | Ký tự đặc biệt Unicode | `"Nguyễn Văn 🎉"` |
| **Very long** | Chuỗi cực dài | `"a" * 10000` |
| **Whitespace** | Khoảng trắng đầu/cuối | `"  email@test.com  "` |
| **SQL injection** | Pattern SQL injection | `"'; DROP TABLE users; --"` |
| **HTML tags** | HTML trong text field | `"<b>bold</b><img src=x onerror=alert(1)>"` |
| **Null/undefined** | Giá trị null | `null` |
| **Special numbers** | Số đặc biệt | `0.1 + 0.2`, `Number.MAX_SAFE_INTEGER`, `NaN` |
| **Date edge** | Ngày đặc biệt | `"2024-02-29"` (năm nhuận), `"2024-12-31"`, `"1970-01-01"` |

---

### Bước 3: Đóng gói Output

Trả kết quả theo format User yêu cầu (mặc định: JSON):

#### Format JSON (mặc định)

```json
{
  "module": "User Registration",
  "totalDataSets": 15,
  "fields": ["email", "password", "name", "phone"],
  "positive": [
    {
      "id": "POS_01",
      "description": "Đăng ký thành công với tất cả fields hợp lệ",
      "data": {
        "email": "auto_register_1712049200@test.com",
        "password": "Test@12345",
        "name": "Auto User Register",
        "phone": "0912345001"
      },
      "expectedResult": "Tạo tài khoản thành công, status 201"
    }
  ],
  "negative": [
    {
      "id": "NEG_01",
      "description": "Email trống",
      "data": { "email": "", "password": "Test@12345", "name": "Test User" },
      "expectedResult": "Lỗi validation: Email is required",
      "targetField": "email",
      "negativeType": "missing_required"
    },
    {
      "id": "NEG_02",
      "description": "Email sai format",
      "data": { "email": "not-email", "password": "Test@12345", "name": "Test User" },
      "expectedResult": "Lỗi validation: Invalid email format",
      "targetField": "email",
      "negativeType": "invalid_format"
    }
  ],
  "boundary": [
    {
      "id": "BND_01",
      "description": "Password đúng min length (6 chars)",
      "data": { "email": "auto_bnd01_1712049200@test.com", "password": "Abc@12", "name": "Test User" },
      "expectedResult": "Thành công",
      "targetField": "password",
      "boundaryType": "min"
    }
  ],
  "edgeCases": [
    {
      "id": "EDGE_01",
      "description": "Name chứa Unicode tiếng Việt + emoji",
      "data": { "email": "auto_edge01_1712049200@test.com", "password": "Test@12345", "name": "Nguyễn Văn 🎉" },
      "expectedResult": "Thành công — hệ thống chấp nhận Unicode",
      "targetField": "name",
      "edgeType": "unicode"
    }
  ]
}
```

#### Format Markdown Table

```markdown
| ID | Category | Description | email | password | name | Expected Result |
|----|----------|-------------|-------|----------|------|-----------------|
| POS_01 | Positive | Đăng ký thành công | auto_reg@test.com | Test@12345 | Auto User | 201 Created |
| NEG_01 | Negative | Email trống | (empty) | Test@12345 | Test User | 422: Email is required |
| BND_01 | Boundary | Password min length | auto_bnd@test.com | Abc@12 | Test User | 201 Created |
```

#### Format Code (TypeScript example)

```typescript
// test-data/registration.data.ts
export const registrationData = {
  positive: {
    email: `auto_register_${Date.now()}@test.com`,
    password: 'Test@12345',
    name: 'Auto User Register',
    phone: '0912345001',
  },
  negative: {
    emptyEmail: { email: '', password: 'Test@12345', name: 'Test' },
    invalidEmail: { email: 'not-email', password: 'Test@12345', name: 'Test' },
    shortPassword: { email: `auto_neg_${Date.now()}@test.com`, password: '123', name: 'Test' },
  },
  boundary: {
    minPassword: { email: `auto_bnd_${Date.now()}@test.com`, password: 'Abc@12', name: 'Test' },
    maxName: { email: `auto_bnd_${Date.now()}@test.com`, password: 'Test@12345', name: 'A'.repeat(100) },
  },
};
```

---

## Data Rules (BẮT BUỘC)

| # | Rule | Mô tả |
|---|------|-------|
| 1 | **Unique** | Không trùng lặp trong test suite — dùng timestamp/random |
| 2 | **Traceable** | Có thể truy ngược test nào sinh ra data — dùng prefix + test name |
| 3 | **No real PII** | KHÔNG dùng dữ liệu cá nhân thật (số CCCD, email thật, SĐT thật) |
| 4 | **Respect constraints** | Data phải tuân theo validation rules đã phân tích |
| 5 | **Include expectedResult** | Mỗi data set PHẢI có expected result để dùng cho assertion |
| 6 | **Deterministic khi cần** | Cùng seed → cùng data (cho reproducible tests) |

---

## NGHIÊM CẤM

| ❌ Không được làm | ✅ Thay thế đúng |
|-------------------|-----------------| 
| Dùng placeholder (`email hợp lệ`, `mã số hợp lệ`) | Giá trị cụ thể: `auto_tc01@test.com`, `KH-2026-0012` |
| Hardcode data trùng lặp giữa các test | Random data với prefix + timestamp |
| Dùng dữ liệu cá nhân thật | Data giả lập: `auto_*@test.com` |
| Chỉ sinh positive data | Bắt buộc cả 4 categories: Positive + Negative + Boundary + Edge |
| Sinh data không có expected result | Mỗi data set PHẢI nêu rõ expected result |
| Đoán validation rules không kiểm tra | Inspect DOM/Spec hoặc hỏi User |
| Đọc `.env` để lấy credentials | Hỏi User hoặc dùng placeholder `[FROM_ENV]` |

---

## Checklist cuối

- [ ] Đã phân tích đầy đủ fields + constraints
- [ ] User đã xác nhận bảng fields trước khi sinh data
- [ ] Data có đủ 4 categories (Positive, Negative, Boundary, Edge Cases)
- [ ] Mỗi data set có expected result rõ ràng
- [ ] Data unique + traceable (prefix + timestamp/random)
- [ ] Không chứa real PII
- [ ] Format output đúng yêu cầu User (JSON/CSV/Markdown/Code)
- [ ] Boundary values đúng theo constraints (min, min-1, max, max+1)