# Chiến Lược Chọn Locator (Áp Dụng Mọi Framework)

> Độ ổn định và khả năng đọc hiểu của locator quyết định sức khỏe của một automation framework.
> Nguyên tắc cốt lõi: KHÔNG BAO GIỜ chọn element dựa trên cấu trúc DOM gắn với styling. Hãy xây dựng locator dựa trên thuộc tính có ngữ nghĩa.

## 1. Bản Đồ Ưu Tiên (Master Priority Map)

Thứ tự ưu tiên từ cao đến thấp:

1. Thuộc tính Accessibility / Aria (semantic, hỗ trợ screen reader)
2. Thuộc tính test chuyên dụng (`data-testid`, `data-test`, `data-qa`)
3. Thuộc tính định danh chính (`id`, `resource-id`, `name`)
4. Hàm semantic riêng framework (Playwright: `getByRole`, `getByLabel`...)
5. CSS Selector
6. XPath (lựa chọn cuối cùng)

## 2. Quy Tắc Ổn Định (Stability Rules)

Mọi locator phải đảm bảo:
- Chỉ match **đúng 1 element** duy nhất trên trang (unique in scope).
- Sống sót qua thay đổi giao diện — không bị ảnh hưởng khi DOM thay đổi layout (thêm/bớt div wrapper, đổi flexbox).

**NGHIÊM CẤM sử dụng:**
- CSS class name động / hash tạm thời (ví dụ: `css-1n2xyz-btn`)
- Chuỗi `nth-child`, `nth-of-type` khi có lựa chọn tốt hơn
- ID tự sinh bởi framework (auto-generated IDs)
- XPath tuyệt đối dựa trên vị trí (ví dụ: `//div[3]/div[2]/form/button`)

## 3. Quy Trình Xác Minh Locator

Trước khi đưa locator vào code, phải kiểm tra:

1. Locator có match **đúng 1 element** trong DOM không?
2. Element match có phải là thành phần người dùng tương tác được không? (không phải shadow DOM overlay)
3. Reload / navigate lại trang — locator có còn đúng không?
4. Thử trên nhiều trạng thái trang (loading, loaded, có data, không data) — locator có ổn định không?

## 4. Locator Theo Framework

Chi tiết locator cho từng framework xem tại:
- Playwright: `.agent/rules/playwright_rules.md` (Section 3)
- Selenium: `.agent/rules/selenium_rules.md` (Section 1)
- Appium: `.agent/rules/appium_rules.md` (Section 1)
