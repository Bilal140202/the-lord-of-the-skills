---
description: Phân tích tính năng đi qua nhiều modules nối tiếp, xây dựng Module Map + Dimension Catalog, và sinh ma trận kết hợp (Pairwise/Business-critical/Full Cartesian). Hỗ trợ 2 modes — DOCUMENT (từ tài liệu) và BROWSER (inspect DOM thực tế).
skills:
  - qa_automation_engineer
  - requirements_analyzer
---

# /generate_cross_module_test_plan — Phân Tích Cross-Module & Sinh Ma Trận Kết Hợp

> **Dùng khi:** Tính năng cần test đi qua **nhiều modules nối tiếp nhau**, mỗi module có nhiều lựa chọn (dimensions), và bộ kết hợp các lựa chọn quyết định output cuối cùng.

> **BẮT BUỘC (MANDATORY):** Trước khi bắt đầu, PHẢI nạp và đọc kỹ:
> - **Skill:** `.agent/skills/qa_automation_engineer/SKILL.md` — Workflow routing + automation rules
> - **Skill:** `.agent/skills/requirements_analyzer/SKILL.md` — Phân tích requirements

---

## Khi nào dùng workflow này?

| Tình huống | Dùng? |
|------------|-------|
| Tính năng đi qua **1 module/form** | ❌ Dùng `/generate_manual_testcases_rbt` |
| Tính năng đi qua **nhiều modules**, mỗi module **độc lập** | ⚠️ Dùng `/generate_application_test_plan` |
| Tính năng đi qua **nhiều modules NỐI TIẾP**, output phụ thuộc **bộ kết hợp điều kiện** | ✅ **Đúng workflow này** |
| Cần **ma trận kết hợp** (Pairwise / Decision Table đa chiều) | ✅ **Đúng workflow này** |

---

## 2 Modes

| Mode | Khi nào dùng | Input chính |
|------|-------------|-------------|
| **DOCUMENT** (mặc định) | User cung cấp tài liệu/spec mô tả modules + business rules | File `.md`, `.doc`, Jira ticket, hoặc mô tả text |
| **BROWSER** | User cung cấp URL và muốn agent inspect DOM thực tế | URL ứng dụng + credentials (nếu cần) |

> Agent tự chọn mode:
> - User cung cấp file/text mô tả → **DOCUMENT**
> - User cung cấp URL hoặc nói "inspect", "mở app", "xem trên browser" → **BROWSER**
> - User cung cấp cả hai → Ưu tiên **BROWSER**, dùng document để cross-reference
> - Nếu không rõ → hỏi user

---

## Input cần từ User

| Input | Bắt buộc | Mô tả |
|-------|----------|-------|
| **Tên tính năng / luồng** | ✅ | VD: "Biên bản thanh toán cho đối tác" |
| **Tài liệu yêu cầu** (DOCUMENT mode) | ✅ | File `.md`, Jira ticket, user story, hoặc text mô tả |
| **URL ứng dụng** (BROWSER mode) | ✅ | Để agent inspect DOM thực tế |
| **Danh sách modules tham gia** | ⚠️ Nên có | Nếu không → agent tự extract từ document/browser |
| **Danh sách dimensions** | ⚠️ Nên có | VD: loại đối tác, loại thuế... Nếu không → agent tự extract |
| **Business rules / công thức** | ❌ Optional | Nếu có → agent map vào ma trận |
| **Credentials** (BROWSER mode) | ❌ | Nếu app cần đăng nhập |
| **Chiến lược ma trận** | ❌ | `pairwise` (mặc định), `business-critical`, hoặc `full-cartesian` |

---

## Các bước thực hiện

### Bước 1: Module Recon — Khám phá từng Module

#### Mode DOCUMENT:

1. **Đọc tài liệu** user cung cấp (file local → `view_file`, URL → `read_url_content`, inline → parse trực tiếp)
2. **Extract danh sách modules** từ tài liệu:
   - Tìm các phần (sections) mô tả từng bước/module trong luồng
   - Xác định thứ tự modules (module nào trước, module nào sau)
   - Xác định fields/controls được đề cập cho mỗi module
3. **Nếu tài liệu không rõ** → hỏi user bổ sung thông tin cụ thể

#### Mode BROWSER:

1. **Nhận danh sách modules** từ user hoặc tự khám phá qua navigation
2. **Với mỗi module** trong chuỗi:
   ```
   browser_navigate → URL module
   browser_resize → 1920 × 1080
   browser_wait_for → page load
   browser_snapshot → thu thập DOM
   ```
3. **Thu thập cho mỗi module:**
   - Tên module (từ tiêu đề trang / breadcrumb)
   - Fields / Controls (input, select, radio...)
   - Giá trị có thể chọn (mở dropdown → đọc options)
   - Validation rules (required, format, min/max)

#### Output Bước 1 — Module Inventory (cả 2 modes):

```markdown
| # | Module | URL / Path | Inputs chính | Key Dimensions | Output | → Next Module |
|---|--------|-----------|-------------|---------------|--------|---------------|
| 1 | Quản lý Đối tác | /partners | Tên, MST, Loại | **Loại đối tác** (3 values) | Partner ID | → Thanh toán |
| 2 | Tạo Thanh toán | /payments/new | Số tiền, Loại | **Loại TT** (2 values) | Payment ID | → Thuế |
| ...| ... | ... | ... | ... | ... | ... |
```

---

### Bước 2: Data Flow & Dimension Extraction

> Gộp Data Flow Mapping + Dimension Extraction vào 1 bước để giảm context switching.

1. **Xác định Data Flow** giữa các modules:
   - Module A **output** gì?
   - Output đó trở thành **input/điều kiện** module B như thế nào?

2. **Ghi Dependencies Matrix:**

   ```markdown
   | Module đích | Phụ thuộc vào | Trường phụ thuộc | Loại phụ thuộc |
   |-------------|--------------|-----------------|----------------|
   | Thanh toán | Đối tác | Partner.type | Lọc options thanh toán |
   | Thuế | Đối tác + Thanh toán | Partner.type, Payment.currency | Quyết định loại thuế |
   ```

3. **Extract Dimensions** — các biến số quyết định output:

   ```markdown
   | # | Dimension (Chiều) | Module nguồn | Giá trị có thể | Số values |
   |---|------------------|-------------|----------------|-----------|
   | D1 | Loại đối tác | Đối tác | Tổ chức, Cá nhân, Hộ KD | 3 |
   | D2 | Loại thanh toán | Thanh toán | VND, USD | 2 |
   | D3 | Loại thuế | Thuế | PIT, VAT, Nhà thầu, Miễn thuế | 4 |
   ```

4. **Tính tổng tổ hợp tiềm năng:**
   ```
   Full Cartesian: D1 × D2 × D3 × ... = tổng bộ kết hợp
   ```

5. **Xác định constraints** (bộ kết hợp không hợp lệ):
   ```markdown
   | Constraint | Mô tả | Bộ bị loại |
   |-----------|-------|-----------|
   | C1 | Cá nhân + USD → không có Nhà thầu | 1 bộ |
   ```

6. **Trình bày cho user** kết quả phân tích:
   - Module Inventory
   - Dependencies Matrix
   - Dimension Catalog
   - Constraints
   - **Tiếp tục tự động** sang Bước 3 (KHÔNG dừng checkpoint — chỉ dừng nếu user chủ động nói sai)

---

### Bước 3: Sinh Ma Trận Kết Hợp (CORE OUTPUT ⭐)

Agent hỗ trợ **3 chiến lược** — user chọn hoặc agent đề xuất:

#### 3A. Pairwise Testing (Mặc định — KHUYẾN NGHỊ)

> Đảm bảo mọi **cặp 2 giá trị** từ 2 dimensions bất kỳ đều được test ít nhất 1 lần.
> Giảm đáng kể số bộ kết hợp mà vẫn cover 100% pairs.

**Cách thực hiện — PHẢI dùng script, KHÔNG tính thủ công:**

1. Agent **sinh script Python** sử dụng thư viện `allpairspy`:

   ```python
   # pairwise_generator.py
   from allpairspy import AllPairs
   
   dimensions = {
       "D1_partner_type": ["Tổ chức", "Cá nhân", "Hộ KD"],
       "D2_payment_type": ["VND", "USD"],
       "D3_tax_type": ["PIT", "VAT", "Nhà thầu", "Miễn thuế"],
       # ... thêm dimensions
   }
   
   # Constraints (bộ không hợp lệ)
   def is_valid(row):
       # Ví dụ: Cá nhân + USD → không có Nhà thầu
       if len(row) >= 3:
           if row[0] == "Cá nhân" and row[1] == "USD" and row[2] == "Nhà thầu":
               return False
       return True
   
   values = list(dimensions.values())
   keys = list(dimensions.keys())
   
   print(f"| # | {' | '.join(keys)} |")
   print(f"|{'---|' * (len(keys) + 1)}")
   for i, combo in enumerate(AllPairs(values, filter_func=is_valid)):
       row = ' | '.join(str(v) for v in combo)
       print(f"| {i+1} | {row} |")
   ```

2. Agent **chạy script** → đọc output → format thành bảng Markdown
3. Nếu `allpairspy` chưa cài → `pip install allpairspy` trước khi chạy

> **NGHIÊM CẤM** agent tự tính pairwise thủ công — LLM không đảm bảo đúng toán học.

#### 3B. Business-Critical Only

> Chỉ chọn các bộ kết hợp **quan trọng nhất** theo business risk.

**Tiêu chí chọn:**
- Bộ kết hợp phổ biến nhất trong thực tế (theo user confirm)
- Bộ liên quan đến tiền, thuế, quyết định tài chính → High Risk
- Bộ kết hợp biên (edge cases giữa các loại)

**Số lượng:** Thường 8-15 bộ. Agent đề xuất → user xác nhận.

#### 3C. Full Cartesian (Đầy đủ)

> Test TẤT CẢ bộ kết hợp hợp lệ. Dùng khi tổng bộ ≤ 50 hoặc user yêu cầu.

#### Output Bước 3 — Bảng Ma Trận:

```markdown
## Ma Trận Kết Hợp (Pairwise — N bộ)

| # | D1: Đối tác | D2: Thanh toán | D3: Thuế | D4: Công nợ | Risk |
|---|------------|---------------|---------|------------|------|
| 1 | Tổ chức | VND | VAT 10% | Thường | High |
| 2 | Tổ chức | USD | PIT 10% | Tạm ứng | High |
| 3 | Cá nhân | VND | PIT 10% | Thường | High |
| ... | ... | ... | ... | ... | ... |
```

> **Ghi chú về Expected Template / Formula:**
> - Nếu user cung cấp business rules → thêm cột "Expected Output" vào bảng
> - Nếu KHÔNG có → **KHÔNG thêm cột này**, để cho workflow tiếp theo xử lý
> - KHÔNG điền `[Cần user xác nhận]` — nếu không biết thì bỏ trống, đừng tạo noise

---

### Bước 4: Đóng Gói Output & Sinh Data (CHECKPOINT ⏸️)

> Đây là **checkpoint DUY NHẤT** — agent dừng ở đây chờ user xác nhận.

1. **Sinh artifact chính:**

   **File: `cross_module_test_plan_<feature>.md`**
   - Module Inventory (Bước 1)
   - Dependencies Matrix (Bước 2)
   - Dimension Catalog + Constraints (Bước 2)
   - **Ma Trận Kết Hợp** (Bước 3) — ĐÂY LÀ OUTPUT CHÍNH
   - Risk Assessment cho mỗi bộ kết hợp

2. **(Optional) Sinh test data cùng lúc** nếu user yêu cầu `--with-data`:

   Với mỗi bộ kết hợp trong ma trận, sinh 1 bộ data:
   ```json
   {
     "combination_id": "COMBO_01",
     "dimensions": { "D1": "Tổ chức", "D2": "VND", "D3": "VAT 10%" },
     "supporting_data": {
       "partner_name": "auto_c01_tc_<timestamp>",
       "tax_id": "0123456789",
       "amount": 100000000
     }
   }
   ```
   
   **Data Rules:**
   - Dimension values PHẢI đúng 100% từ ma trận — KHÔNG random
   - Supporting fields → random + unique + traceable (prefix `auto_combo{XX}`)
   - Không chứa real PII

3. **⏸️ DỪNG LẠI — Trình bày cho user:**
   - Ma trận kết hợp hoàn chỉnh
   - Hỏi: "Có bộ kết hợp nào thiếu? Cần bổ sung gì?"
   - **Chờ user xác nhận**

---

## Bước tiếp theo sau workflow này

| Mục tiêu | Workflow tiếp theo |
|----------|-------------------|
| Sinh **test cases chi tiết** cho từng bộ kết hợp | `/generate_manual_testcases_rbt` — input = ma trận |
| Tạo **test data thật trên hệ thống** qua browser pipeline | `/generate_combinatorial_test_data` — mode PIPELINE |
| Sinh **automation scripts** | `/generate_automation_from_testcases` — input = test cases |

---

## Ví dụ thực tế

### Ví dụ 1: E-Commerce Order (DOCUMENT mode)

**User nói:** "Phân tích luồng đặt hàng: Chọn sản phẩm → Chọn vận chuyển → Thanh toán → Xác nhận"

**Agent thực hiện:**
1. Extract 4 modules từ mô tả
2. Dimensions: Loại SP (3), Vận chuyển (3), Thanh toán (4) = 36 bộ full
3. Chạy script pairwise → giảm xuống ~12 bộ
4. Output: Ma trận 12 bộ + Module Map

### Ví dụ 2: Insurance Contract (BROWSER mode)

**User nói:** "Inspect app bảo hiểm tại https://example.com, luồng tạo hợp đồng"

**Agent thực hiện:**
1. Navigate qua 3 modules, snapshot mỗi module
2. Extract dimensions từ DOM: Loại BH (3), Gói (4), Kỳ hạn (3), PTTT (2) = 72 bộ full
3. Chạy script pairwise → giảm xuống ~15 bộ
4. Output: Ma trận 15 bộ + Data Flow

---

## NGHIÊM CẤM

| ❌ Không được làm | ✅ Thay thế đúng |
|-------------------|-----------------| 
| Tự tính pairwise thủ công (greedy/IPOG) | Sinh script Python + `allpairspy` → chạy script |
| Đoán giá trị dimensions không có nguồn | DOCUMENT: extract từ tài liệu, BROWSER: inspect DOM |
| Tự điền Expected Template/Formula khi không biết | Bỏ trống hoặc hỏi user — KHÔNG viết `[Cần xác nhận]` |
| Sinh Full Cartesian mặc định khi dimensions lớn | Dùng Pairwise — giảm 80-90% bộ kết hợp |
| Bỏ qua constraints (bộ kết hợp không hợp lệ) | Phải xác định và loại bỏ invalid combinations |
| Load quá nhiều skills (>2) vào context | Chỉ load 2 skills bắt buộc, thêm skill khác khi cần |

---

## Checklist cuối

- [ ] Đã thu thập thông tin TỪNG module (qua tài liệu hoặc browser)
- [ ] Đã xây dựng Dependencies Matrix giữa các modules
- [ ] Đã extract đầy đủ dimensions + values + constraints
- [ ] Đã chọn chiến lược ma trận phù hợp
- [ ] **(Pairwise)** Đã sinh và chạy script — KHÔNG tính thủ công
- [ ] Ma trận chỉ chứa bộ kết hợp hợp lệ (đã loại constraints)
- [ ] User đã xác nhận ma trận tại Bước 4
- [ ] Artifact output đã lưu đúng vị trí project
