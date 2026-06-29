---
marp: true
theme: uncover
class: invert
backgroundColor: #0f172a
color: #f8fafc
paginate: true
style: |
  section {
    font-family: 'Inter', 'Roboto', sans-serif;
    text-align: left;
    padding: 30px;
    font-size: 24px;
  }
  h1 { color: #38bdf8; text-shadow: 0 0 10px rgba(56, 189, 248, 0.5); font-size: 50px; }
  h2 { color: #f472b6; border-bottom: 2px solid #f472b6; padding-bottom: 5px; font-size: 35px; }
  h3 { color: #fbbf24; font-size: 28px; }
  strong { color: #fbbf24; }
  ul { list-style-type: '🚀 '; }
  li { margin-bottom: 10px; }
---

# 🤖 Multi-Agent Workflow
## Antigravity vs CrewAI Local

**Người trình bày:** Antigravity AI
**Dự án:** Iruka Multi-Agent Pipeline

---

## 🌊 01. Hệ thống "Dàn Chân Rết"
### (Cơ chế vận hành)

- **Độc lập:** Các IDE (Planner, Coder...) chạy riêng biệt
- **Kết nối:** Giao tiếp qua Hub trung tâm SQLite
- **Isolation:** Mỗi Agent có 1 Profile và Account riêng
- **Persistence:** Luôn giữ trạng thái "Thức" 45s/vòng

---

## 🌊 Workflow - Antigravity Hub

```
┌─────────┐    dispatch     ┌──────────────┐
│ MASTER  │ ─────────────▶ │   Hub SQLite  │
└─────────┘                └──────┬───────┘
                                  │  poll_task (45s)
          ┌───────────────────────┼───────────────────┐
          ▼                       ▼                   ▼
    ┌──────────┐           ┌──────────┐         ┌──────────┐
    │  PLANNER │           │  CODER   │         │  TESTER  │
    │ Lên kế   │──submit──▶│ Viết code│──submit─▶│ Kiểm tra│
    │  hoạch   │  plan     │          │  changes │          │
    └──────────┘           └──────────┘         └────┬─────┘
                                                     │ submit
                                                     ▼
                                               ┌──────────┐
                                               │ REPORTER │
                                               │ Báo cáo  │
                                               └──────────┘
```

---

## 🌊 Vòng lặp Worker (Zombie Loop)

```
    ┌──────────────────────────────────────────────┐
    │                                              │
    ▼                                              │
poll_task(role) ──────keep_alive──────────────────┘
    │
    │ task_available
    ▼
 Đọc Plan / Context từ Hub
    │
    ▼
 Làm việc chuyên môn
 (viết code / test / report)
    │
    ▼
submit_phase() ──▶ Hub chuyển task sang Role tiếp theo
    │
    └──▶ Quay lại poll_task (Zero Output)
```

---

## 🌟 Ưu điểm - Antigravity Hub

- **Visual:** Theo dõi Agent viết code trực tiếp.
- **Trí tuệ:** Dùng Cloud LLM nên cực kỳ thông minh.
- **Phân tách:** Lịch sử chat riêng, không bị loãng.
- **Tự động:** Cơ chế "Zombie" tự truyền tay nhau.

---

## ⚠️ Điểm yếu - Antigravity Hub

- **Tài nguyên:** Ngốn RAM do chạy nhiều IDE.
- **Tài khoản:** Cần nhiều tài khoản để tránh Limit.
- **Setup:** Cấu hình ban đầu khá phức tạp.

---

## 🛠️ 02. "CrewAI + Local Qwen"
### (Cơ chế & Luồng)

- **Orchestrator:** Một Script Python điều khiển tất cả
- **Local AI:** Gọi API tới LM Studio (Qwen 2.5)
- **Format:** Trao đổi dữ liệu qua JSON String
- **Centralized:** Mọi thứ nằm trong 1 Terminal

---

## 🛠️ Workflow - CrewAI + Qwen Local

```
  ┌────────────────────────────────────────────┐
  │          Python Script (CrewAI)            │
  │         [Orchestrator - 1 process]         │
  └──┬──────────────┬───────────────┬──────────┘
     │              │               │
     ▼              ▼               ▼
┌─────────┐   ┌─────────┐   ┌──────────────┐
│ Agent 1 │   │ Agent 2 │   │   Agent N    │
│ Planner │   │  Coder  │   │   Tester     │
└────┬────┘   └────┬────┘   └──────┬───────┘
     │              │               │
     └──────────────┴───────────────┘
                    │  API Call
                    ▼
         ┌──────────────────────┐
         │     LM Studio        │
         │  [Qwen-Coder 2.5]    │
         │  Running 100% Local  │
         └──────────────────────┘
```

---

## 🛠️ Vòng lặp CrewAI (Sequential)

```
User input Task
    │
    ▼
Planner Agent ──API──▶ Qwen ──▶ Trả về Plan (JSON)
    │
    ▼
Coder Agent ──API──▶ Qwen ──▶ Trả về Code (JSON String)
    │  ⚠️ Dễ lỗi format tại đây!
    ▼
Tester Agent ──API──▶ Qwen ──▶ Kết quả Test
    │
    ▼
Reporter Agent ──API──▶ Qwen ──▶ Báo cáo cuối cùng
    │
    ▼
Xong! (Không tự động lặp lại)
```

## 🌟 Ưu điểm - CrewAI Local

- **Chi phí:** Miễn phí 100% tài nguyên AI.
- **Bảo mật:** Dữ liệu không bao giờ rời khỏi máy.
- **Tùy biến:** Tự chỉnh được thông số Model.
- **Nhẹ:** Chỉ tốn tài nguyên cho 1 tiến trình Python.

---

## ⚠️ Điểm yếu - CrewAI Local

- **Model:** Qwen Local đôi khi "ngáo" logic phức tạp.
- **Hardware:** Cần GPU mạnh để chạy mượt nhiều Agent.
- **Parsing:** Dễ lỗi định dạng khi Agent giao tiếp.

---

## 📊 Bảng so sánh nhanh

| Đặc điểm | Antigravity Hub | CrewAI Local |
| :--- | :--- | :--- |
| **Trí tuệ** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Độ mượt** | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Tài nguyên** | 🔴 Tốn RAM | 🔵 Tốn VRAM |
| **Bảo mật** | Trung bình | 🟢 Tuyệt đối |
| **Giám sát** | ✅ Trực quan | ❌ Khó |

---

## 💡 Lời khuyên (Recommendation)

- **Dùng Antigravity Hub cho:** Task phức tạp, yêu cầu code chuẩn, cần giám sát từng dòng.
- **Dùng CrewAI Local cho:** Task đơn giản, bảo mật cao, hoặc khi không có Internet.

**=> Antigravity Hub là lựa chọn số 1 hiện tại!**

---

<!-- _class: lead -->
# 3. Phân tích thực tế: Multi-Agent vs. 1 Agent Độc Lập

---

## ⚖️ Sự thật về Hệ thống Multi-Agent (Hub)

### 👍 Những điều HAY (Ưu điểm vượt trội)
1. **Chuyên môn hóa tuyệt đối:** PLANNER không bị phân tâm bởi Cú pháp Code. CODER không bị gò bó bởi Kiến trúc tổng thể. TESTER là bên thứ 3 khách quan, không bị "ảo giác" tự khen code mình đẹp.
2. **Quản lý Context hiệu quả:** Task khổng lồ được chia nhỏ. Mỗi Agent chỉ mang theo lượng Context vừa đủ → Tiết kiệm Token, giảm thiểu tỷ lệ "ngáo".
3. **Traceability (Bắt mạch lỗi):** Khi dự án dở dang, dễ dàng xem lại Artifact để biết lỗi do PLANNER tư duy sai, hay do CODER gõ sai.

---

### 👎 Những điều DỞ (Nhược điểm)
1. **Đứt gãy thông tin (Information Loss):** Agent trao đổi với nhau bằng Text/JSON (Artifacts). Nếu PLANNER viết plan mơ hồ hoặc thiếu chi tiết, CODER chắc chắn sẽ làm sai.
2. **Cồng kềnh cho Task Nhỏ:** "Sửa màu 1 cái nút" mà đi qua 4 Agent (Plan -> Code -> Test -> Report) là quá lãng phí tài nguyên và thời gian. 
3. **Tiêu tốn Tài nguyên:** Chạy 4-5 bản thể Antigravity cùng lúc ngốn quá nhiều RAM, CPU và Token API. 

_**💡 MẸO:** Dùng **1 Agent (Master)** cho các task nhỏ, sửa bug nhanh. Dùng **Multi-Agent (Hub)** làm "Xưởng sản xuất" cho Feature lớn hoặc khởi tạo dự án._

---

## 🚀 Ứng dụng thực tế của Hệ thống Phân vai

### 🎨 1. Trong Thiết kế (Design & UI/UX)
- **Design Agent:** Chuyên nhận Prompt từ user, vẽ UI Mockup, lên định dạng Design System (Màu sắc, Font, Spacing, Animations). Sinh ra `design_specs.json`.
- **Frontend Agent:** Áp dụng Design Specs vào React/Vite. Không cần tự biên tự diễn màu sắc, chỉ tuân thủ đúng chuẩn.
- **Visual Tester:** Tự động chụp Screenshot, so sánh cấu trúc DOM với Design System gốc xem có bị vỡ layout hay thiếu Glassmorphism không.

---

### ✒️ 2. Trong Viết Nội dung (Content Creation)
- **Research Agent:** Cào dữ liệu từ Web, tổng hợp số liệu, phân tích đối thủ.
- **Writer Agent:** Nhận raw data, viết thành bài Blog/Kịch bản theo đúng Tone & Voice (Hài hước, Chuyên nghiệp).
- **Editor/SEO Agent:** Đóng vai trò Test. Duyệt bài viết, kiểm tra mật độ từ khóa SEO, bắt lỗi chính tả, rút gọn các câu rườm rà. Nếu không đạt → Reject bắt Writer viết lại.

---

### 🐛 3. Trong Kiểm thử & Fix Bug (Tự động hóa)
- Vòng lặp đỉnh cao: **CODER ↔ TESTER**
- Thay vì ném lỗi cho User, hệ thống tự động:
  1. TESTER chạy lệnh `npm test` hoặc `build`.
  2. Phát hiện lỗi vỡ giao diện (VD: thiếu Tailwind CSS).
  3. Gọi hàm `reject_phase` trả task và **Bug Report** ngược về CODER.
  4. CODER nhận báo lỗi, phân tích và sửa code.
  5. Vòng lặp tối đa 3 lần. Nếu vẫn Fail → Chuyển sang REPORTER để nhờ User (Con người) can thiệp với báo cáo lỗi cuối cùng.
