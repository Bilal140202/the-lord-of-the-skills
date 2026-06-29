# Hướng Dẫn Sử Dụng Chi Tiết: Iruka Multi-Agent MCP Hub V2

Tài liệu này hướng dẫn bạn cách khởi chạy, vận hành và quản lý kiến trúc đa cửa sổ (Multi-Window) dành cho Iruka Pipeline. Hệ thống sử dụng chuẩn MCP của Google kết hợp SQLite, cấu hình qua JSON giúp bạn tùy biến chuỗi Role cực kỳ dễ dàng.

---

## 1. Chuẩn bị Môi Trường (Setup Lần Đầu)

### 1.1 Cài Đặt Thư Viện
Hệ thống Hub sử dụng các lõi `FastMCP` và `Pydantic`. Nên dùng `uv` để quản lý môi trường.
Mở Terminal tại thư mục `AI/agent-mcp` và chạy lệnh:
```powershell
uv pip install -r requirements.txt
```

### 1.2 Kiểm Tra Cấu Hình Antigravity IDE
Antigravity cần được thông báo về `iruka-hub` qua giao thức MCP. Tính năng này đã được đăng ký ngầm trong file cấu hình `.vscode/settings.json` của dự án.

> [!WARNING]
> **Lưu ý cực kỳ quan trọng:** Sau khi cấu hình file `.vscode/settings.json`, bạn **BUỘC PHẢI Restart Antigravity** (tắt toàn bộ cửa sổ và mở lại). Nếu không, Agent Editor dưới góc phải sẽ không load được Tool MCPHub lên đâu.

---

## 2. Dynamic Pipeline (Cấu hình chuỗi Role Tự Động)

Hệ thống giờ đây không gắn cứng mã nguồn. Bạn hoàn toàn có thể tự vẽ một "dây chuyền sản xuất" gồm bao nhiêu khâu tùy ý. 

### Bước 2.1: Chỉnh sửa `pipeline.json`
Mở file `AI/agent-mcp/pipeline.json`. Nó chứa một mảng trình tự vận hành của các Sub-Agents (viết In Hoa):

```json
{
  "sequence": [
    "PLANNER",
    "CODER",
    "TESTER",
    "REVIEWER",
    "REPORTER"
  ]
}
```

*Khi bạn thêm/xóa/đổi vị trí Role nào đó ở đây, tập lệnh cấu hình và Hub sẽ tự hiểu mạch dữ liệu, bạn không cần đụng vào code Python!* 
*(Lưu ý sau khi sửa chuỗi JSON này, bạn hãy chạy lại file script `setup_workers.ps1` để được cập nhật dư Icon ngoài Desktop).*

---

## 3. Vận Hành Thực Tế (Hàng Ngày)

Quy trình chuẩn đòi hỏi bạn phải có nhiều **Cửa sổ Antigravity IDE** cùng mở chung thư mục dự án. 

> [!TIP]  
> **Tuyệt kỹ chia cắt Account (Multi-Session):** Đừng bao giờ chép đè ứng dụng. Dự án này cung cấp lệnh rải quân tự động để phân lập ổ lưu Cookie và API Token của từng Agent, vượt Rate-Limit mà vẫn mượt mà không dùng thêm ổ đĩa. 

### Bước 3.1: Dàn Chân Rết (Shortcut Setup)
Mở cửa sổ Terminal PowerShell tại thư mục `AI/agent-mcp` và gõ:
```powershell
powershell -ExecutionPolicy Bypass -File .\setup_workers.ps1
```
Thao tác này đọc danh sách từ `pipeline.json` và "rải" các Cửa sổ (Biểu tượng Logo cá nhân hóa như AG_PLANNER, AG_CODER) ra ngoài màn hình chính Windows (Desktop).

### Bước 3.2: Kích hoạt các Cửa Sổ Nhân viên (Workers)
Đúp chuột vào icon tùy ý ngoài Desktop (như AG_PLANNER), đăng nhập vào account Gemini phụ bất kỳ. Nhờ hệ thống Workflow Automation gõ tắt, bạn không cần phải copy/paste rườm rà. Chỉ cần gõ lệnh Slash đúng với tên Role của cửa sổ đó và bấm Enter:

- Cửa sổ PLANNER: gõ `/start-planner`
- Cửa sổ CODER: gõ `/start-coder`  
- Cửa sổ TESTER: gõ `/start-tester`
- Cửa sổ REVIEWER: gõ `/start-reviewer`
- Cửa sổ REPORTER: gõ `/start-reporter`

(Động tác này sẽ tự động ép AI chạy file `skills/pipeline_worker_skill.md` và bước thẳng vào Vòng lặp Vô tận canh gác Hub Database!).

**Lúc này, con LLM sẽ tự động làm 2 việc:**
1. Nó chạy vào kho kiến thức nội bộ ở `.agent/plugins/iruka-team/skills/iruka-[role]/SKILL.md` để "đọc thần chú nghiệp vụ". Nó sẽ tự học trước form xuất JSON và cách xưng hô y như đợt cấu hình CrewAI cũ!
2. Nó báo: `⏳ [ROLE] đang chờ task...` và chui vào trạng thái canh gác.

### Bước 3.2: Master Giao Việc (Dispatcher)
Tại cửa sổ VS Code Account chính, bạn làm Chủ Quản (Master), không cần dùng skill loop gì cả.
Mỗi khi có yêu cầu lập trình hay làm game mới, hãy bảo AI (hoặc dùng Tool trực tiếp):
  > *"Hãy gọi Tool `dispatch_task` để lên task phát triển tính năng X. Thư mục đích là `ABC/` "*

Lập tức Master sẽ thông báo đã đẩy Task ID vào Hub DB.

### Bước 3.3: Hệ Thống Tự Động Kết Giới
Cứ thế, bạn chỉ cần xem chúng nó phối hợp:
1. Thằng đứng vị trí 1 trong `pipeline.json` phát hiện task, nó giằng lấy (Lock db), lên báo cáo và submit.
2. Thằng đứng vị trí 2 trong `pipeline.json` tiếp nhận ngay tức khắc, code thẳng trên file local cho bạn. Cứ 60s nó bắn báo cáo tim đập (Heartbeat) để không ai giành mất nhiệm vụ của nó.
3. Chạy qua hết chuỗi pipeline là Game xong.

---

## 4. Các Tool Giám Sát Dành Cho Master

Bạn ở lại tab Cửa sổ số 1 là có thể chỉ huy toàn diện: 
- *"Chạy `get_task_status` xem mã task `XXX` làm tới đâu rồi?"*
  Lệnh này sẽ trả về lịch sử (action) trong DB cùng các file Artifact đang lưu hiện tại.

Nếu Worker bị Treo/Code lỗi mắc kẹt:
- *"Chạy `cancel_task` cho task của đó đi giúp tôi."*
  Hệ thống sẽ ép trạng thái task về Cancelled, dẹp đường.

Nếu một Worker bị tắt máy ngang hoặc đứt kết nối wifi? 
Hệ thống Heartbeat ở Hub SQLite sẽ phát hiện mất sóng sau 3 phút, Hub sẽ gỡ khóa (Unlock) tự động và rớt xuống thành trạng thái Ready để Worker chạy lại!

---

## 5. Xử Lý Sự Cố Thường Gặp (Troubleshoot)

| Lỗi / Tình Trạng | Nguyên Nhân | Cách Xử Lý |
| :--- | :--- | :--- |
| Ở cửa sổ Master gọi `dispatch_task` báo "Tool không tồn tại". | Do VS Code chưa được Restart. | Nhấn `Ctrl + Shift + P` -> gõ `Developer: Reload Window`. Đợi Plugin nạp lại MCPServers. |
| Role mới của tôi bị Hub báo Role vô hiệu. | Do chưa xuất hiện trong `pipeline.json`. | Sửa file JSON, Restart Window và cho phép chạy lại. |
| Mở nhiều cửa sổ SQLite báo lỗi `database is locked`. | Do gọi lệnh trong cùng 1 phần ngàn giây. | Hệ thống cài đè WAL mode và timeout retry tự động nên 20s sau nó sẽ tự fix, không cần lo. |
