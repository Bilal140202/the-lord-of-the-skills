---
description: Thiết kế và scaffold automation framework hoàn chỉnh. Hỗ trợ Playwright, Selenium, Appium — Web, Mobile, API.
skills:
  - framework_architect
  - qa_automation_engineer
---

# Workflow: Thiết Kế Automation Framework

> **BẮT BUỘC (MANDATORY SKILL):** Bạn PHẢI nạp và đọc kỹ nội dung của skill **`framework_architect`** (tại `.agent/skills/framework_architect/SKILL.md`) trước khi bắt đầu. Ngoài ra, tham khảo thêm skill **`qa_automation_engineer`** để nắm các quy tắc automation chung.

Workflow này giúp agent thiết kế, scaffold và triển khai một automation framework hoàn chỉnh từ đầu, phù hợp với nhu cầu cụ thể của project.

## ⚠️ Nguyên tắc thực thi

- **Tất cả output bằng Tiếng Việt**
- **KHÔNG đoán** tech stack — phải hỏi user xác nhận trước khi scaffold
- **PHẢI tạo artifact `task.md`** để theo dõi tiến độ
- Mỗi file sinh ra phải **biên dịch/chạy được ngay** — không để placeholder `// TODO`
- Framework phải tuân thủ design principles trong skill `framework_architect`

## Stacks hỗ trợ

| Platform | Stack | Ngôn ngữ | Runner | Report |
|---|---|---|---|---|
| 🌐 Web | Playwright | TypeScript | Playwright Test | HTML Report, Allure |
| 🌐 Web | Playwright | Java | TestNG / JUnit5 | Allure |
| 🌐 Web | Playwright | Python | Pytest | pytest-html, Allure |
| 🌐 Web | Selenium | Java | TestNG | Allure, ExtentReports |
| 🌐 Web | Selenium | Python | Pytest | pytest-html, Allure |
| 📱 Mobile | Appium | Java | TestNG | Allure, ExtentReports |
| 📱 Mobile | Appium | Python | Pytest | Allure |
| 🔌 API | REST Assured | Java | TestNG | Allure |
| 🔌 API | Playwright API | TypeScript | Playwright Test | HTML Report |

## Các bước thực hiện

### Bước 1: Thu thập yêu cầu (Requirements Gathering — ⏸️ CHECKPOINT)

1. **Hỏi user** các thông tin cần thiết:

   | Câu hỏi | Mục đích | Mặc định nếu không trả lời |
   |---|---|---|
   | Ứng dụng cần test là gì? (Web / Mobile / API / Hybrid) | Chọn platform | Web |
   | Framework nào? (Playwright / Selenium / Appium) | Chọn tool | Playwright |
   | Ngôn ngữ? (TypeScript / Java / Python) | Chọn language | TypeScript (Playwright), Java (Selenium/Appium) |
   | Project name? | Đặt tên thư mục | `automation-framework` |
   | Có cần CI/CD pipeline không? | Sinh pipeline config | Có (GitHub Actions) |
   | Reporting tool? | Tích hợp report | Mặc định theo stack |
   | Có test API song song không? | Thêm API testing layer | Không |
   | Parallel execution? | Config parallel | Không |

2. **Xác nhận lại** với user trước khi scaffold:
   ```
   📋 Tóm tắt framework sẽ tạo:
   - Platform: Web
   - Framework: Playwright
   - Language: TypeScript
   - Runner: Playwright Test
   - Report: HTML Report + Allure
   - CI/CD: GitHub Actions
   - Project name: my-automation
   
   Bạn xác nhận để tôi bắt đầu scaffold không?
   ```

3. **Chờ user xác nhận** trước khi sang Bước 2

### Bước 2: Scaffold Project Structure (Foundation)

1. **Tạo artifact `task.md`** để theo dõi checklist:
   ```markdown
   # Framework Setup Progress
   - [x] Bước 1: Thu thập yêu cầu
   - [ ] Bước 2: Scaffold project structure
   - [ ] Bước 3: Sinh base classes
   - [ ] Bước 4: Sinh example tests
   - [ ] Bước 5: Cấu hình reporting & CI/CD
   - [ ] Bước 6: Verify & Deliver
   ```

2. **Tạo thư mục project** theo template trong skill `framework_architect`:
   - Tham khảo mục **Project Structure Templates** trong SKILL.md
   - Tạo toàn bộ thư mục + file cấu hình gốc

3. **Sinh file cấu hình build** (tuỳ stack):

   **Playwright + TypeScript:**
   - `package.json` — dependencies: `@playwright/test`, devDependencies phù hợp
   - `playwright.config.ts` — baseURL, viewport (1920x1080), timeout, retries, reporter
   - `tsconfig.json` — paths, strict mode
   - `.env.example` — template environment variables

   **Selenium + Java:**
   - `pom.xml` — dependencies: selenium-java, testng, webdrivermanager, allure-testng, log4j
   - `testng.xml` — suite configuration, listeners
   - `log4j2.xml` — logging configuration

   **Appium + Java:**
   - `pom.xml` — dependencies: appium-java-client, selenium-java, testng, allure
   - `testng.xml` — suite configuration
   - Capabilities config file (JSON/YAML) cho Android + iOS

   **Playwright + Python:**
   - `requirements.txt` — playwright, pytest, pytest-playwright, allure-pytest
   - `pyproject.toml` — pytest config, tool settings
   - `conftest.py` — root fixtures, browser setup

4. **Tạo file .gitignore** phù hợp (node_modules, target, __pycache__, .env, reports...)
5. **Tạo README.md** với hướng dẫn:
   - Prerequisites (Node.js, Java, Python version)
   - Installation steps
   - Cách chạy test
   - Project structure overview
   - Conventions (naming, coding standards)

### Bước 3: Sinh Core Classes (Base Layer)

1. **Configuration Management:**

   | Stack | File | Nội dung |
   |---|---|---|
   | Playwright TS | `src/utils/env.config.ts` | Đọc `.env`, export typed config object |
   | Selenium Java | `src/main/.../config/ConfigReader.java` | Đọc properties file, singleton pattern |
   | Appium Java | `src/main/.../config/AppConfig.java` | Đọc capabilities JSON, env variables |
   | Playwright Python | `src/utils/config.py` | Đọc `.env` bằng `python-dotenv` |

2. **Browser / Driver Management:**

   | Stack | File | Nội dung |
   |---|---|---|
   | Playwright TS | `playwright.config.ts` + fixtures | Browser config trong config, auth trong fixtures |
   | Selenium Java | `DriverFactory.java` | Factory pattern, WebDriverManager, thread-safe |
   | Appium Java | `AppiumDriverFactory.java` + `CapabilitiesManager.java` | Appium server URL, desired capabilities per device |
   | Playwright Python | `conftest.py` | Fixtures cho browser, context, page |

3. **Base Page / Screen class:**
   - Common methods: `navigate()`, `click()`, `type()`, `getText()`, `isVisible()`
   - Built-in smart waits (KHÔNG có hard sleep)
   - Screenshot on failure
   - Logging mỗi action

4. **Base Test class:**
   - Setup: khởi tạo browser/driver, navigate to baseURL
   - Teardown: đóng browser/driver, capture screenshot nếu fail
   - Test lifecycle hooks (beforeAll, afterAll, beforeEach, afterEach)

5. **Utilities:**
   - `TestDataGenerator` — sinh email, username, phone unique + traceable
   - `WaitHelper` — custom wait conditions (nếu cần ngoài built-in)
   - `ScreenshotUtil` — capture + attach to report
   - `Logger` — structured logging (Log4j / winston / Python logging)

### Bước 4: Sinh Example Tests (Validation Layer)

1. **Tạo ít nhất 1 example Page Object:**
   - `LoginPage` (hoặc `LoginScreen` cho mobile) với locators + methods thực tế
   - Locator dùng placeholder mô tả rõ cần thay thế:
     ```typescript
     // REPLACE: Update locator after inspecting actual DOM
     readonly usernameInput = this.page.getByLabel('Username');
     readonly passwordInput = this.page.getByLabel('Password');
     readonly loginButton = this.page.getByRole('button', { name: 'Login' });
     ```

2. **Tạo ít nhất 1 example Test:**
   - `LoginTest` — demo happy path (login thành công)
   - Có đầy đủ: Arrange → Act → Assert
   - Assertion có message rõ ràng
   - Test data dùng TestDataGenerator (nếu applicable)

3. **Tạo 1 example data-driven test** (nếu phù hợp):
   - Đọc data từ file JSON/YAML/CSV
   - Parameterized test với nhiều bộ data

### Bước 5: Cấu hình Reporting & CI/CD (Integration Layer)

1. **Reporting setup:**

   | Stack | Report | Cấu hình |
   |---|---|---|
   | Playwright TS | HTML + Allure | `reporter` trong playwright.config.ts |
   | Selenium Java | Allure | `allure-testng` dependency + `@Step`, `@Attachment` annotations |
   | Appium Java | Allure + ExtentReports | `allure-testng` + `ExtentManager` singleton |
   | Playwright Python | pytest-html + Allure | `conftest.py` hooks + pytest addopts |

   - Screenshot auto-attach on failure
   - Test step logging trong report

2. **CI/CD Pipeline** (nếu user yêu cầu):

   **GitHub Actions template:**
   ```yaml
   # Sinh file .github/workflows/<framework>.yml
   # Nội dung tùy stack: install deps → run tests → upload report
   ```

   - Install dependencies
   - Run tests (headless mode cho CI)
   - Upload test report as artifact
   - Parallel execution (nếu được yêu cầu)
   - Environment variables từ GitHub Secrets

3. **Docker support** (optional — chỉ nếu user yêu cầu):
   - Dockerfile cho test execution environment
   - docker-compose.yml nếu cần Selenium Grid / Appium server

### Bước 6: Verify & Deliver (Quality Gate)

1. **Kiểm tra framework build được:**
   ```bash
   # Playwright TS
   npm install && npx playwright install && npx playwright test --list

   # Selenium Java
   mvn clean compile

   # Appium Java
   mvn clean compile

   # Playwright Python
   pip install -r requirements.txt && playwright install
   ```

2. **Chạy example test** để verify framework hoạt động:
   - Nếu PASS → framework sẵn sàng
   - Nếu FAIL do thiếu app/URL → acceptable (ghi note trong README)
   - Nếu FAIL do lỗi code framework → sửa ngay

3. **Review checklist** trước khi bàn giao:
   - [ ] Project structure đúng template
   - [ ] Tất cả dependencies đã khai báo
   - [ ] Config management hoạt động (đọc .env)
   - [ ] Base Page/Test có đầy đủ common methods
   - [ ] POM pattern được tuân thủ
   - [ ] Smart waits — không có hard sleep
   - [ ] Example test chạy được (hoặc chạy được khi có app)
   - [ ] README.md hướng dẫn đầy đủ
   - [ ] .gitignore bao phủ đúng
   - [ ] Reporting tích hợp
   - [ ] Không có debug log, commented code, TODO placeholder

4. **Cập nhật `task.md`** với trạng thái hoàn thành

## Xử lý tình huống đặc biệt

| Tình huống | Cách xử lý |
|---|---|
| **User muốn hybrid (Web + Mobile)** | Tạo shared layer (utils, config) + tách pages vs screens |
| **User muốn hybrid (Web + API)** | Thêm API layer song song (api helpers + api tests folder) |
| **User có framework cũ cần refactor** | Đọc code hiện tại → đề xuất migration plan → refactor từng phần |
| **User muốn multi-browser** | Config parallel projects trong playwright.config.ts hoặc test suite XML |
| **User muốn multi-device (Appium)** | CapabilitiesManager hỗ trợ load từ JSON per device (Android/iOS) |
| **User không biết chọn stack** | Gợi ý dựa trên: team skill, project type, CI infra |

## Output

- **Project structure** đầy đủ (tất cả thư mục + files)
- **Build config** (package.json / pom.xml / requirements.txt)
- **Framework config** (playwright.config.ts / testng.xml / conftest.py)
- **Base classes** (BasePage, BaseTest, DriverFactory, ConfigReader)
- **Utilities** (TestDataGenerator, WaitHelper, ScreenshotUtil, Logger)
- **Example Page Object + Test** (LoginPage + LoginTest)
- **Reporting integration** (Allure / HTML Report)
- **CI/CD pipeline** (GitHub Actions template)
- **README.md** (setup guide + project overview)
- **Artifact `task.md`** (checklist tiến độ)