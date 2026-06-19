# 🛠️ Iruka Agent MCP — Hướng dẫn Vận hành & Workflow Chi tiết

Tài liệu này giải thích cách hệ thống Multi-Agent Pipeline hoạt động, từ kiến trúc tổng thể đến các cơ chế kỹ thuật bên dưới.

---

## 1. Tổng quan Kiến trúc (Master - Hub - Worker)

Hệ thống hoạt động dựa trên mô hình **Trung tâm Điều phối (Hub)** giúp các Agent (Worker) khác nhau có thể phối hợp làm việc trên cùng một Task mà không cần giao tiếp trực tiếp.

- **Master (Cửa sổ 1)**: Người dùng hoặc AI đóng vai trò quản lý. Nhiệm vụ là giao việc (`dispatch_task`) và theo dõi tiến độ.
- **Hub (MCP Server)**: Chạy bằng Python (`hub_server.py`), kết nối với database SQLite. Đây là "bảng tin" nơi lưu trữ mọi thông tin về Task và kết quả xử lý.
- **Workers (Cửa sổ 2, 3...)**: Các Agent chạy loop tự động (`poll_task`). Mỗi Agent tự nhận diện vai trò của mình (PLANNER, CODER, TESTER...) và chủ động lấy việc từ Hub.

---

## 2. Luồng hoạt động từng bước (Step-by-step)

Mỗi Task đi qua một chu trình khép kín (Pipeline) được cấu hình trong `pipeline.json`:

1.  **Giai đoạn Giao việc (DISPATCH)**: Master gọi lệnh `dispatch_task` kèm theo yêu cầu (`goal`). Task được tạo trong database với trạng thái `PENDING`.
2.  **Giai đoạn Lập kế hoạch (PLANNING)**:
    - **PLANNER** poll thấy task `PENDING` -> Chuyển sang `PLANNING` (Lock task).
    - PLANNER nghiên cứu code, viết kế hoạch -> Gửi kết quả (`submit_phase`).
    - Task chuyển sang trạng thái `PLAN_READY`.
3.  **Giai đoạn Lập trình (CODING)**:
    - **CODER** poll thấy task `PLAN_READY` -> Chuyển sang `CODING` (Lock task).
    - CODER đọc plan, sửa code thực tế -> Gửi báo cáo thay đổi (`submit_phase`).
    - Task chuyển sang trạng thái `CODER_READY`.
4.  **Giai đoạn Kiểm thử (TESTING)**:
    - **TESTER** poll thấy task `CODER_READY` -> Chuyển sang `TESTER_ING`.
    - TESTER chạy test, kiểm tra lỗi.
    - **Nếu OK**: Submit -> Chuyển sang `REPORTER` (trạng thái `TESTER_READY`).
    - **Nếu có BUG**: Gọi `reject_phase` -> Task bị đẩy ngược về `CODER_READY` để Coder sửa lại.
5.  **Giai đoạn Báo cáo (REPORTING)**:
    - **REPORTER** tổng hợp toàn bộ quá trình từ Plan, Code đến Test kết quả -> Viết báo cáo cuối.
    - Task chuyển sang trạng thái `FINISHED`.

---

## 3. Cơ chế Poll Task (Lấy việc tự động)

Hệ thống sử dụng cơ chế **Long Polling** kết hợp với **Locking** để đảm bảo tính ổn định:

### Cách Hoạt Động của poll_task
Khi một Worker gọi `poll_task(role="CODER")`:
1.  **Hub Check**: Hub kiểm tra trong database xem có task nào có trạng thái "đang đợi" Role đó không (ví dụ: Coder đợi task `PLAN_READY`).
2.  **Wait Loop (Long Polling)**: Nếu chưa có task, Hub không trả về ngay mà sẽ giữ kết nối và kiểm tra lại mỗi 2 giây, kéo dài tới tối đa **44 giây**. Nếu trong lúc này có task mới, Hub trả về ngay lập tức. Điều này giúp Worker nhận task "real-time" mà không cần spam request quá nhiều.
3.  **Atomic Claim (Locking)**: Khi tìm thấy task, Hub sẽ thực hiện:
    - Đánh dấu `lock_owner = "CODER"`.
    - Cập nhật `lock_heartbeat = [thời gian hiện tại]`.
    - Đổi `status` sang trạng thái đang xử lý (ví dụ: `CODING`).
    - Việc này diễn ra trong 1 giao dịch database (Atomic) để đảm bảo dù có 10 Coder cùng poll, chỉ có DUY NHẤT 1 người nhận được task.

> [!NOTE]
> **Tự động hóa 100%**: Khi hết 44 giây mà chưa có task, Hub sẽ trả về một tín hiệu "Keep Alive". Worker sẽ nhận tín hiệu này và **ngay lập tức** tự động kích hoạt lượt poll mới. Anh không cần phải khởi động lại hay can thiệp thủ công, Agent sẽ luôn ở trạng thái "trực chiến" 24/7.

---

## 4. Cơ chế Heartbeat & Tự phục hồi (Recovery)

Để tránh trường hợp một Worker đang làm việc thì bị crash (mất điện, lỗi mạng) dẫn đến Task bị "kẹt lock" mãi mãi:

- **Heartbeat Mỗi 60s**: Worker đang làm task phải gọi `send_heartbeat` mỗi phút để báo với Hub là "tôi vẫn đang chạy".
- **Timeout 3 phút**: Mỗi khi có ai đó gọi `poll_task`, Hub sẽ tranh thủ kiểm tra toàn bộ database. Nếu thấy task nào có `lock_heartbeat` cũ hơn 3 phút, Hub coi như Worker đó đã "chết".
- **Auto Unlock**: Hub sẽ tự động xóa `lock_owner` và trả `status` về trạng thái trước đó để các Worker khác có thể nhảy vào nhận lại task đó.

---

## 5. Cấu trúc Database (SQLite)

Dữ liệu được lưu tại `AI/agent-mcp/hub.db`. Hệ thống sử dụng chế độ **WAL (Write-Ahead Logging)** giúp nhiều cửa sổ VS Code đọc/ghi cùng lúc mà không bị lỗi `Database is locked`.

### Các bảng chính:
- **`tasks`**: Lưu trạng thái hiện tại, đường dẫn project, yêu cầu (goal) và thông tin lock.
- **`artifacts`**: Lưu "sản phẩm" của từng phase (file kế hoạch của Planner, danh sách file sửa của Coder, báo cáo lỗi của Tester).
- **`history`**: Nhật ký chi tiết — Ai đã làm gì, lúc nào, kết quả ra sao.

---

## 6. Cấu hình Pipeline linh hoạt

Thứ tự làm việc các Role không bị code cứng. Bạn có thể chỉnh sửa file `pipeline.json`:

```json
{
  "sequence": ["PLANNER", "CODER", "TESTER", "REPORTER"]
}
```

Hệ thống sẽ tự động hiểu:
- Role đứng trước hoàn thành thì Role đứng sau mới được phép "bốc" task.
- Nếu bạn thêm `REVIEWER` vào giữa `CODER` và `TESTER`, hệ thống sẽ tự sinh ra thêm các trạng thái trung gian tương ứng.
