# Iruka Multi-Agent Pipeline (Hub V2)

Đây là hệ thống Dispatch Hub thay thế cho giải pháp CrewAI cũ. Hệ thống này sử dụng chuẩn bảo mật MCP của Google để kết nối nhiều cửa sổ Antigravity với nhau thông qua một file SQLite duy nhất.

## Tính Năng Nổi Bật
- **Multi-Account:** Chia các sub-agents ra nhiều tab VS Code đăng nhập Google Account khác nhau, tránh kẹt API Rate limit vì chia sẻ IP/Account chung.
- **SQLite Database:** Không bị lỗi Write Conflict/File Corrupt như V1 dùng `.json`.
- **Worker Logic Skill:** Quản lý vòng lặp chủ động từ chính các Agents, với hệ thống Heartbeat chống Crash/Sleep.
- **MCP Server Local:** Chuẩn hóa theo Server Protocol của Anthropic/Google.

## Cài đặt (Run Once)

1. Cài đặt Python 3.10+ (Đã cấu hình trong uv lock).
2. Cài dependency MCP Server (nếu thiếu):
```powershell
mcp[cli]>=1.0.0
fastmcp>=0.1.0
pydantic>=2.0.0
```
3. Khởi tạo cấu hình File `.vscode/settings.json` tại root path của Workspace theo mô tả tại [MULTI_AGENT_PIPELINE.md](MULTI_AGENT_PIPELINE.md).

## Vận Hành (Hàng Ngày)

### Bước 1: Setup Hub + Workers
1. Mở Cửa sổ 1 (Dự Án Chính - Account #1): Đây là Master.
2. Mở Cửa sổ 2 (Account #2): Nhắn riêng vào Antigravity ở đó: `"Bạn là PLANNER. Hãy chạy Pipeline Worker Skill."` (Có thể nhắc nó tham chiếu folder Agent-MCP skills).
3. Mở Cửa sổ 3 (Account #3): Nhắn với Antigravity: `"Bạn là CODER. Hãy chạy Pipeline Worker Skill."`

### Bước 2: Bắt Đầu Chạy (Chỉ làm ở Cửa Sổ 1)
- Ở cửa sổ Master, chạy lệnh MCP tool `dispatch_task` kèm Goal và Project Path.
- Chờ đợi hệ thống báo hoàn thành! Planner và Coder sẽ tiếp nhận chuỗi qua SQLite db ngầm.
