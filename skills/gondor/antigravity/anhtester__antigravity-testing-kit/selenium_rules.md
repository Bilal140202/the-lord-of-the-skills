# Quy Tắc Dành Riêng Cho Selenium WebDriver

> Áp dụng khi tự động hóa browser với Java và Selenium WebDriver.

## 1. Thứ Tự Ưu Tiên Locator

Tuân thủ nghiêm ngặt thứ tự sau để đảm bảo tốc độ và độ ổn định:

1. `id` — Nhanh nhất, unique nhất
2. `data-testid` / `data-test` / `data-qa` — Thuộc tính chuyên cho test
3. `name` — Thuộc tính HTML chuẩn
4. `cssSelector` — Linh hoạt, nhanh
5. `xpath` — Lựa chọn cuối cùng

Ví dụ đúng:
```java
driver.findElement(By.id("login-btn"));
driver.findElement(By.cssSelector("button[data-testid='submit-btn']"));
driver.findElement(By.name("username"));
```

Ví dụ sai — XPath cấu trúc phụ thuộc vị trí:
```java
// NGHIÊM CẤM: XPath tuyệt đối dựa trên DOM structure
driver.findElement(By.xpath("//div[3]/div[2]/form/div[1]/button"));
```

## 2. Chiến Lược Chờ Đợi (Wait Strategy)

**NGHIÊM CẤM:**
- `Thread.sleep()` — Trong mọi trường hợp
- Bất kỳ cách nào cố định thời gian chờ

**SỬ DỤNG:**
- Java Explicit Waits với `WebDriverWait` + `ExpectedConditions`:

```java
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

// Chờ element hiển thị
WebElement element = wait.until(
    ExpectedConditions.visibilityOfElementLocated(By.id("profile"))
);

// Chờ element click được
wait.until(ExpectedConditions.elementToBeClickable(By.id("submit-btn")));

// Chờ text xuất hiện
wait.until(ExpectedConditions.textToBePresentInElementLocated(
    By.id("message"), "Thành công"
));

// Chờ URL chuyển hướng
wait.until(ExpectedConditions.urlContains("/dashboard"));
```

- Có thể tạo custom `FluentWait` nếu cần polling linh hoạt:
```java
Wait<WebDriver> fluentWait = new FluentWait<>(driver)
    .withTimeout(Duration.ofSeconds(15))
    .pollingEvery(Duration.ofMillis(500))
    .ignoring(NoSuchElementException.class);
```

## 3. Thiết Lập Browser

- **Viewport:** Đặt viewport desktop (`1920x1080`) khi debug:
  ```java
  driver.manage().window().setSize(new Dimension(1920, 1080));
  ```
- **Headed mode:** Bắt buộc khi debug (không set `--headless`)
- **Headless mode:** Chỉ dùng khi test đã PASS trên headed hoặc trong CI/CD

## 4. Cấu Trúc Test (TestNG)

```java
public class LoginTest extends BaseTest {

    @BeforeMethod
    public void setUp() {
        // Navigate, setup data...
    }

    @Test(groups = {"smoke", "regression"})
    public void testLoginWithValidCredentials() {
        // Arrange
        LoginPage loginPage = new LoginPage(driver);
        String email = DataGenerator.generateEmail("login");

        // Act
        loginPage.login(email, "ValidPass@123");

        // Assert
        DashboardPage dashboard = new DashboardPage(driver);
        Assert.assertTrue(dashboard.isDisplayed(),
            "Dashboard phải hiển thị sau khi đăng nhập thành công");
    }

    @AfterMethod
    public void tearDown() {
        // Cleanup...
    }
}
```

## 5. Assertions (Kiểm Tra Kết Quả)

- Sử dụng TestNG Assertions (`Assert.assertEquals`, `Assert.assertTrue`...)
- Luôn thêm **message mô tả** vào assertion:
  ```java
  Assert.assertEquals(actualTitle, "Dashboard", "Tiêu đề trang phải là Dashboard");
  Assert.assertTrue(element.isDisplayed(), "Element phải hiển thị trên trang");
  ```
- Mỗi test method phải có ít nhất **1 assertion** ở cuối
