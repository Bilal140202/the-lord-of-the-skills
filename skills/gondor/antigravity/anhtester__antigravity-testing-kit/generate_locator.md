---
description: Sinh locator ổn định cho UI element. Hỗ trợ Playwright, Selenium, Appium.
skills:
  - smart_locator_agent
  - ui_debug_agent
---

# /generate_locator — Sinh Locator Ổn Định Cho UI Automation

> User cung cấp element cần tìm locator (mô tả, screenshot, URL, hoặc HTML snippet).
> AI inspect DOM/UI hierarchy thực tế, sinh locator ổn định theo priority chuẩn, verify uniqueness, trả về kết quả.

> **BẮT BUỘC (MANDATORY):** Trước khi bắt đầu, PHẢI nạp và đọc kỹ:
> - **Skill:** `.agent/skills/smart_locator_agent/SKILL.md` — Quy trình sinh locator
> - **Skill:** `.agent/skills/ui_debug_agent/SKILL.md` — Quy trình inspect DOM
> - **Rule:** `.agent/rules/locator_strategy.md` — Bản đồ ưu tiên locator
> - **Rule:** `.agent/rules/<framework>_rules.md` — Quy tắc riêng framework đang dùng

---

## Input cần từ User

| Input | Bắt buộc | Mô tả |
|-------|----------|-------|
| Mô tả element | ✅ | VD: "nút Login", "dropdown chọn Country", "ô nhập Email" |
| URL trang chứa element | ✅ | Để AI navigate và inspect DOM thực tế |
| Framework | ✅ | `playwright`, `selenium`, hoặc `appium` |
| HTML snippet | ❌ | Nếu User đã có sẵn DOM context — AI dùng để phân tích nhanh |
| Page class đích | ❌ | File Page class mà locator sẽ được thêm vào |
| Login yêu cầu | ❌ | Nếu trang yêu cầu đăng nhập — User cho biết cách login |

> **Lưu ý về Login:** Nếu trang yêu cầu đăng nhập, User PHẢI chỉ rõ cách login (fixture, script, URL login...). AI KHÔNG ĐƯỢC tự đọc `.env` hay đoán credentials.

---

## Các bước thực hiện

### Phase 1: Phân tích yêu cầu

1. **Hiểu element cần tìm** — Xác định rõ:
   - **Loại element:** button, input, link, dropdown, dialog, table row, checkbox, radio...
   - **Context:** Nằm trong page chính, dialog/modal, sidebar, table, iframe?
   - **Thao tác:** click, fill, select, hover, verify text, verify visibility?

2. **Xác định framework và đọc rules tương ứng:**

   | Framework | Rule file |
   |-----------|-----------|
   | Playwright | `.agent/rules/playwright_rules.md` |
   | Selenium | `.agent/rules/selenium_rules.md` |
   | Appium | `.agent/rules/appium_rules.md` |

3. **Kiểm tra Page class hiện tại (nếu User chỉ định):**
   - Đọc file Page class → biết locator đã có sẵn
   - Tránh trùng lặp hoặc xung đột naming

---

### Phase 2: Inspect DOM / UI Hierarchy thực tế

> ⚠️ **NGUYÊN TẮC BẤT DI BẤT DỊCH: KHÔNG BAO GIỜ ĐOÁN LOCATOR. PHẢI INSPECT THỰC TẾ.**

#### 2A. Web (Playwright MCP)

4. **Navigate đến trang chứa element:**
   ```
   browser_navigate(url=<target_url>)
   ```

5. **Resize viewport (BẮT BUỘC):**
   ```
   browser_resize(width=1920, height=1080)
   ```

6. **Capture DOM:**
   ```
   browser_snapshot()
   ```

7. **Phân tích element trong snapshot:**
   - Tìm ref element trong DOM tree
   - Ghi lại **tất cả attributes có giá trị**: `role`, `aria-label`, `aria-labelledby`, `data-testid`, `data-test`, `data-qa`, `id`, `name`, `placeholder`, `type`, `href`, text content
   - Ghi lại **parent context** (dialog? table? sidebar? iframe?)

8. **Nếu element bị ẩn** (dropdown menu, modal, tooltip...):
   - Thực hiện action mở element: `browser_click(ref=<trigger>)`
   - Capture lại: `browser_snapshot()`

#### 2B. Mobile (Appium)

4. **Dùng Appium Inspector** hoặc `page_source` để lấy UI hierarchy
5. **Ghi lại attributes:** `accessibility-id`, `resource-id`, `content-desc`, `text`, `class`, `bounds`
6. **Nếu element nằm trong scroll view** → scroll đến element trước khi inspect

---

### Phase 3: Sinh locator theo Priority

9. **Áp dụng bản đồ ưu tiên (Master Priority Map):**

   | # | Loại | Khi nào dùng |
   |---|------|-------------|
   | 1 | Accessibility / Aria | Element có `role`, `aria-label` rõ ràng |
   | 2 | Test attribute | Element có `data-testid`, `data-test`, `data-qa` |
   | 3 | ID / name | Element có `id` hoặc `name` ổn định (không auto-generated) |
   | 4 | Framework semantic | Playwright: `getByRole`, `getByLabel`... |
   | 5 | CSS Selector | Dùng attribute cụ thể, tránh class động |
   | 6 | XPath | Lựa chọn cuối cùng — chỉ dùng XPath tương đối |

10. **Sinh locator theo framework:**

    **Playwright (TypeScript/JavaScript):**
    ```typescript
    // Priority 1: Role-based
    page.getByRole('button', { name: 'Submit' })

    // Priority 2: Test ID
    page.getByTestId('submit-btn')

    // Priority 3: Label / Placeholder
    page.getByLabel('Email')
    page.getByPlaceholder('Enter your password')

    // Priority 4: Text
    page.getByText('Submit')

    // Priority 5: CSS
    page.locator('#submit-button')
    page.locator('[data-testid="submit-btn"]')

    // Priority 6: XPath (cuối cùng)
    page.locator('//button[@type="submit"]')
    ```

    **Playwright (Python):**
    ```python
    # Priority 1: Role-based
    page.get_by_role("button", name="Submit")

    # Priority 2: Test ID
    page.get_by_test_id("submit-btn")

    # Priority 3: Label / Placeholder
    page.get_by_label("Email")
    page.get_by_placeholder("Enter your password")

    # Priority 4: Text
    page.get_by_text("Submit")

    # Priority 5: CSS
    page.locator("#submit-button")

    # Priority 6: XPath (cuối cùng)
    page.locator("//button[@type='submit']")
    ```

    **Selenium (Java):**
    ```java
    // Priority 1: ID
    driver.findElement(By.id("submit-button"));

    // Priority 2: Test attribute
    driver.findElement(By.cssSelector("[data-testid='submit-btn']"));

    // Priority 3: Name
    driver.findElement(By.name("submit"));

    // Priority 4: CSS Selector
    driver.findElement(By.cssSelector("button.btn-primary[type='submit']"));

    // Priority 5: XPath (cuối cùng)
    driver.findElement(By.xpath("//button[@type='submit']"));
    ```

    **Appium (Java):**
    ```java
    // Priority 1: Accessibility ID
    driver.findElement(AppiumBy.accessibilityId("login_button"));

    // Priority 2: Resource ID (Android)
    driver.findElement(AppiumBy.id("com.app:id/login_button"));

    // Priority 3: iOS Predicate
    driver.findElement(AppiumBy.iOSNsPredicateString("label == 'Login'"));

    // Priority 4: Class Chain (iOS)
    driver.findElement(AppiumBy.iOSClassChain("**/XCUIElementTypeButton[`label == 'Login'`]"));

    // Priority 5: XPath (cuối cùng)
    driver.findElement(AppiumBy.xpath("//android.widget.Button[@text='Login']"));
    ```

---

### Phase 4: Validate locator

11. **Verify uniqueness — PHẢI match đúng 1 element:**

    **Web (Playwright MCP):**
    ```
    browser_evaluate(function="() => document.querySelectorAll('<css_selector>').length")
    ```

    **Selenium:**
    ```java
    List<WebElement> matches = driver.findElements(By.<strategy>("<locator>"));
    assert matches.size() == 1;
    ```

    **Appium:**
    ```java
    List<WebElement> matches = driver.findElements(AppiumBy.<strategy>("<locator>"));
    assert matches.size() == 1;
    ```

12. **Verify visibility** — Element phải tương tác được:
    - Không bị overlay bởi element khác
    - Không ở trạng thái `hidden`, `display:none`, `visibility:hidden`
    - Không nằm ngoài viewport (cần scroll)

13. **Verify stability — Kiểm tra checklist:**
    - [ ] Không dùng dynamic CSS class (VD: `css-1n2xyz`, `sc-bdnxRM`)
    - [ ] Không dùng XPath tuyệt đối (VD: `//html/body/div[1]/div[2]/button`)
    - [ ] Không dùng auto-generated ID (VD: `ember123`, `react-select-2-input`)
    - [ ] Không dùng `nth-child` / `nth-of-type` khi có lựa chọn tốt hơn
    - [ ] Sống sót qua page reload
    - [ ] Ổn định trên nhiều trạng thái trang (loading, loaded, có data, không data)

---

### Phase 5: Trả kết quả

14. **Output Format — BẮT BUỘC cung cấp đầy đủ 3 phần:**

```markdown
## Locator Result: [Mô tả element]

**Framework:** [Playwright / Selenium / Appium]

### 🎯 Primary Locator (Recommended)
```<language>
// Locator code — copy-paste ready
```
- **Loại:** [Role-based / Test ID / CSS / ...]
- **Unique:** ✅ Match 1 element
- **Stability:** ✅ Không dùng dynamic class / absolute xpath

### 🔄 Fallback Locator
```<language>
// Locator thay thế khi primary hỏng
```
- **Loại:** [CSS / XPath / ...]
- **Khi nào dùng:** Khi primary locator bị break do DOM thay đổi

### 💡 Reasoning
- Giải thích tại sao chọn Primary locator này
- Tại sao loại bỏ các candidate khác
- Rủi ro tiềm ẩn (nếu có)

### 📋 Usage Example (nếu User yêu cầu)
```<language>
// Ví dụ sử dụng locator trong test code
```
```

15. **(Tùy chọn) Nếu User yêu cầu thêm vào Page class:**
    - Thêm locator đúng vị trí trong Page class
    - Đặt tên theo naming convention của project
    - Tạo method sử dụng locator nếu cần

---

## Common Patterns (Tham khảo)

### Scoping locator trong Dialog / Modal:
```typescript
// Playwright — scope vào dialog trước
const dialog = page.getByRole('dialog');
dialog.getByRole('button', { name: 'Confirm' }).click();
```
```java
// Selenium — scope vào dialog
WebElement dialog = driver.findElement(By.cssSelector("[role='dialog']"));
dialog.findElement(By.cssSelector("button[data-testid='confirm']")).click();
```

### Dynamic text matching:
```typescript
// Playwright — exact vs partial
page.getByText('Submit', { exact: true })     // exact match
page.getByText(/submit/i)                      // regex, case-insensitive
```
```python
# Playwright Python — normalize-space XPath
page.locator(f"//a[normalize-space()='{text}']")
```

### Table row action:
```typescript
// Playwright — filter row rồi interact
const row = page.getByRole('row').filter({ hasText: 'John Doe' });
row.getByRole('button', { name: 'Edit' }).click();
```
```java
// Selenium — XPath relative trong table
driver.findElement(By.xpath("//tr[contains(., 'John Doe')]//button[text()='Edit']"));
```

---

## NGHIÊM CẤM

| ❌ Không được làm | ✅ Thay thế đúng |
|-------------------|-----------------|
| Đoán locator không inspect DOM/UI | `browser_snapshot()` hoặc Appium Inspector trước |
| Dùng CSS class động (`css-1n2xyz`, `sc-xxx`) | Dùng role, aria, data-testid, text |
| Dùng XPath tuyệt đối (`//html/body/div[1]...`) | Dùng XPath tương đối với attribute |
| Dùng auto-generated ID (`ember123`, `:r1:`) | Dùng stable attribute hoặc text |
| Trả locator không verify uniqueness | Luôn verify match đúng 1 element |
| Chỉ trả 1 locator, không có fallback | Trả Primary + Fallback + Reasoning |
| Đọc `.env` để lấy credentials login | Hỏi User cách login hoặc dùng fixture có sẵn |

---

## Checklist cuối

- [ ] Đã inspect DOM/UI hierarchy thực tế (không đoán)
- [ ] Locator theo đúng priority: accessibility > test-id > id/name > semantic > css > xpath
- [ ] Primary locator match đúng 1 element duy nhất
- [ ] Có Fallback locator
- [ ] Có Reasoning giải thích lý do chọn
- [ ] Không dùng dynamic class, absolute xpath, auto-generated ID
- [ ] Locator ổn định qua page reload và nhiều trạng thái
- [ ] (Nếu thêm vào Page class) Đã verify code chạy không lỗi