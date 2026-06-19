# Quy Tắc Dành Riêng Cho Appium (Mobile Automation)

> Áp dụng khi tự động hóa ứng dụng mobile với Java và Appium.

## 1. Thứ Tự Ưu Tiên Locator

Sử dụng chiến lược locator native theo từng nền tảng (iOS / Android) thay vì web equivalent:

1. `accessibility id` — Cross-platform, ổn định nhất
2. `resource-id` (Android) — Thuộc tính native Android
3. `id` — ID chung
4. `iOS predicate string` (iOS) — Nhanh, chuyên biệt iOS
5. `iOS class chain` (iOS) — Truy vấn cấu trúc iOS
6. `xpath` — Lựa chọn cuối cùng (chậm nhất)

Ví dụ đúng:
```java
// Accessibility id — Cross-platform, luôn ưu tiên
driver.findElement(AppiumBy.accessibilityId("login_button"));

// Android — resource-id
driver.findElement(AppiumBy.id("com.application.xyz:id/login_button"));

// iOS — Predicate String (nhanh)
driver.findElement(AppiumBy.iOSNsPredicateString("label == 'Login'"));

// iOS — Class Chain
driver.findElement(AppiumBy.iOSClassChain(
    "**/XCUIElementTypeButton[`label == 'Login'`]"
));
```

## 2. NGHIÊM CẤM

- XPath tuyệt đối dựa trên vị trí — bất kỳ thay đổi layout nhỏ nào cũng gây fail:
  ```java
  // NGHIÊM CẤM:
  driver.findElement(By.xpath(
      "//android.widget.FrameLayout[1]/android.widget.LinearLayout[2]/android.widget.Button[1]"
  ));
  ```
- Truy vấn element nằm ngoài màn hình (off-screen) mà không scroll trước
- Tương tác với element bị disabled mà không kiểm tra trạng thái
- Hardcode thời gian chờ animation

## 3. Chiến Lược Chờ Đợi (Wait Strategy)

**NGHIÊM CẤM:**
- `Thread.sleep()` — Trong mọi trường hợp

**SỬ DỤNG:**
- Explicit Waits với `WebDriverWait`:
  ```java
  WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));

  // Chờ element hiển thị
  wait.until(ExpectedConditions.visibilityOfElementLocated(
      AppiumBy.accessibilityId("welcome_text")
  ));

  // Chờ element click được
  wait.until(ExpectedConditions.elementToBeClickable(
      AppiumBy.accessibilityId("submit_button")
  ));
  ```

- Xử lý scroll đến element:
  ```java
  // Android — UiScrollable
  driver.findElement(AppiumBy.androidUIAutomator(
      "new UiScrollable(new UiSelector().scrollable(true))" +
      ".scrollIntoView(new UiSelector().text(\"Submit\"))"
  ));
  ```

## 4. Cấu Trúc Test (TestNG)

```java
public class LoginMobileTest extends BaseTest {

    @BeforeMethod
    public void setUp() {
        // Khởi tạo driver, capabilities...
    }

    @Test(groups = {"mobile", "regression"})
    public void testLoginSuccess() {
        // Arrange
        LoginScreen loginScreen = new LoginScreen(driver);
        String email = DataGenerator.generateEmail("loginMobile");

        // Act
        loginScreen.login(email, "ValidPass@123");

        // Assert
        HomeScreen homeScreen = new HomeScreen(driver);
        Assert.assertTrue(homeScreen.isWelcomeDisplayed(),
            "Màn hình Home phải hiển thị sau khi đăng nhập");
    }
}
```

Lưu ý:
- Mobile dùng **Screen Objects** (tương đương Page Objects) — hậu tố `Screen`
- Ví dụ: `LoginScreen.java`, `HomeScreen.java`, `SettingsScreen.java`

## 5. Đặc Thù Mobile Testing

- **Xoay màn hình:** Test cả portrait và landscape nếu app hỗ trợ:
  ```java
  driver.rotate(ScreenOrientation.LANDSCAPE);
  ```
- **Background/Foreground:** Test app khi chuyển ra nền rồi quay lại:
  ```java
  driver.runAppInBackground(Duration.ofSeconds(5));
  ```
- **Push Notification:** Verify notification bằng Appium notification listener
- **Permission Dialog:** Xử lý dialog xin quyền (camera, location...):
  ```java
  // Android — Auto-grant permissions trong capabilities
  capabilities.setCapability("autoGrantPermissions", true);
  ```
