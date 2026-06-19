# 🏗️ Iruka Multi-Agent Pipeline — Kế hoạch Triển khai Chi tiết (V2.0)

> **Mục tiêu:** Xây dựng hệ thống MCP Hub Server cho phép 3 cửa sổ Antigravity (3 Google Account khác nhau) phối hợp làm việc tự động trên cùng một dự án game. Master gõ 1 lệnh → Workers tự nhận task và xử lý không cần can thiệp thêm.

---

## 📌 Ngữ cảnh & Giới hạn quan trọng

- **Antigravity** là giao diện chat AI chạy trong VS Code — **không thể** điều khiển lẫn nhau từ xa.
- Giải pháp: Dùng **MCP Hub Server** (file Python chạy nền) làm trung gian.
- Mỗi Worker Antigravity **chủ động hỏi** Hub → nhận task → xử lý → nộp kết quả.
- Setup 1 lần buổi sáng: Mở 3 cửa sổ VS Code, gõ lệnh khởi động cho 2 Worker → cả ngày tự động.

---

## 🌐 Kiến trúc tổng thể

```
┌────────────────────────────────────────────────────────────────┐
│              VS Code Window 1 — MASTER (Account #1)            │
│                                                                │
│   Người dùng gõ: "/pipeline-task Thêm tính năng trace letter" │
│         │                                                      │
│         ▼  gọi MCP tool                                        │
│   [dispatch_task(goal, project_path)]                          │
│         │                                                      │
└─────────┼──────────────────────────────────────────────────────┘
          │ HTTP/stdio
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                  MCP HUB SERVER (hub_server.py)                 │
│              Chạy nền — Python + FastMCP + SQLite               │
│                                                                 │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────────────┐  │
│  │  hub.db      │  │  lock mgr   │  │   6 MCP Tools        │  │
│  │  (SQLite)    │  │  heartbeat  │  │   dispatch_task      │  │
│  │              │  │  timeout    │  │   poll_task          │  │
│  │  tasks       │  │  recovery   │  │   submit_phase       │  │
│  │  artifacts   │  │             │  │   get_task_status    │  │
│  │  history     │  │             │  │   list_tasks         │  │
│  └──────────────┘  └─────────────┘  │   cancel_task        │  │
│                                     └──────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
          ┌────────────────┘────────────────┐
          │ poll every 20s                  │ poll every 20s
          ▼                                 ▼
┌──────────────────────┐        ┌──────────────────────┐
│  VS Code Window 2     │        │  VS Code Window 3     │
│  WORKER: PLANNER      │        │  WORKER: CODER        │
│  Account Google #2    │        │  Account Google #3    │
│                       │        │                       │
│  "Đang chờ task..."   │        │  "Đang chờ task..."   │
│  (loop tự động)       │        │  (loop tự động)       │
└──────────────────────┘        └──────────────────────┘
```

---

## 📂 Cấu trúc file cần tạo

```
AI/agent-mcp/
├── hub_server.py          ← MCP Server chính (FastMCP + 6 tools)
├── hub_database.py        ← SQLite manager (CRUD operations)
├── hub_models.py          ← Pydantic models (Task, Phase, Artifact)
├── hub.db                 ← SQLite DB (tự tạo khi chạy lần đầu)
├── requirements.txt       ← Dependencies
├── skills/
│   └── pipeline_worker_skill.md  ← Kịch bản Worker chạy
├── MULTI_AGENT_PIPELINE.md       ← File này (kế hoạch)
└── README.md              ← Hướng dẫn setup
```

---

## 🗃️ Database Schema (SQLite — `hub.db`)

### Bảng `tasks`

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id          TEXT PRIMARY KEY,          -- UUID v4
    goal        TEXT NOT NULL,             -- Mô tả yêu cầu của người dùng
    project_path TEXT NOT NULL,            -- Đường dẫn dự án game
    context     TEXT,                      -- JSON array: danh sách file context ban đầu
    status      TEXT NOT NULL DEFAULT 'PENDING',
                                           -- PENDING | PLANNING | PLAN_READY | CODING
                                           -- CODE_READY | REVIEWING | FINISHED | FAILED | CANCELLED
    current_phase TEXT,                    -- Role đang xử lý: PLANNER | CODER | REVIEWER
    lock_owner  TEXT,                      -- Role đang giữ lock
    lock_heartbeat TEXT,                   -- ISO timestamp của heartbeat gần nhất
    created_at  TEXT NOT NULL,             -- ISO timestamp
    updated_at  TEXT NOT NULL              -- ISO timestamp
);
```

### Bảng `artifacts`

```sql
CREATE TABLE IF NOT EXISTS artifacts (
    id          TEXT PRIMARY KEY,
    task_id     TEXT NOT NULL REFERENCES tasks(id),
    phase       TEXT NOT NULL,             -- PLANNER | CODER | REVIEWER | REPORTER
    type        TEXT NOT NULL,             -- plan | code_changes | review_report | release_note
    content     TEXT NOT NULL,             -- Nội dung artifact (markdown hoặc JSON string)
    created_at  TEXT NOT NULL
);
```

### Bảng `history`

```sql
CREATE TABLE IF NOT EXISTS history (
    id          TEXT PRIMARY KEY,
    task_id     TEXT NOT NULL REFERENCES tasks(id),
    phase       TEXT NOT NULL,
    actor       TEXT NOT NULL,             -- PLANNER | CODER | REVIEWER | MASTER | SYSTEM
    action      TEXT NOT NULL,             -- dispatched | claimed | submitted | failed | cancelled
    summary     TEXT,                      -- Mô tả ngắn hành động
    timestamp   TEXT NOT NULL
);
```

---

## ⚙️ State Machine (Vòng đời Task)

```
                 dispatch_task()
                      │
                      ▼
                  [ PENDING ]
                      │
         poll_task(PLANNER) → claim
                      │
                      ▼
                 [ PLANNING ]  ←── heartbeat mỗi 60s
                      │
         submit_phase(PLANNER, plan_artifact)
                      │
                      ▼
                [ PLAN_READY ]
                      │
           poll_task(CODER) → claim
                      │
                      ▼
                  [ CODING ]  ←── heartbeat mỗi 60s
                      │
         submit_phase(CODER, code_artifact)
                      │
                      ▼
               [ CODE_READY ]
                      │
         poll_task(REVIEWER) → claim
                      │
                      ▼
               [ REVIEWING ]  ←── heartbeat mỗi 60s
                      │
         submit_phase(REVIEWER, review_artifact)
                      │
                      ▼
               [ FINISHED ] ──── hoặc ────► [ FAILED ]
```

**Timeout rule:** Nếu `lock_heartbeat` quá 3 phút (180s) không được cập nhật → Hub tự động unlock task → `status` quay về trạng thái trước đó để Worker khác claim.

---

## 🛠️ Đặc tả 6 MCP Tools

### Tool 1: `dispatch_task`

```python
@mcp.tool()
def dispatch_task(goal: str, project_path: str, context_files: list[str] = []) -> str:
    """
    Dùng bởi: Master (Antigravity cửa sổ 1).
    Tạo task mới và đẩy vào Hub để Workers nhận.
    
    Args:
        goal: Mô tả yêu cầu. VD: "Thêm tính năng hiển thị hint sau 5 giây idle"
        project_path: Đường dẫn tuyệt đối của project game.
        context_files: Danh sách file quan trọng cần Worker đọc. VD: ["src/Game.ts", "README.md"]
    
    Returns: JSON string
    {
        "task_id": "uuid",
        "status": "PENDING",
        "message": "Task đã được tạo. Workers sẽ tự động nhận."
    }
    """
```

### Tool 2: `poll_task`

```python
@mcp.tool()
def poll_task(role: str) -> str:
    """
    Dùng bởi: Workers (Planner, Coder, Reviewer).
    Hỏi Hub xem có task phù hợp với role không.
    
    Args:
        role: Một trong "PLANNER" | "CODER" | "REVIEWER"
    
    Returns khi CÓ task:
    {
        "status": "task_available",
        "task_id": "uuid",
        "goal": "Mô tả yêu cầu",
        "project_path": "đường/dẫn/project",
        "context_files": ["file1", "file2"],
        "previous_artifacts": {
            "plan": "nội dung plan markdown (nếu là CODER/REVIEWER)",
            "code_changes": "nội dung code changes (nếu là REVIEWER)"
        }
    }
    
    Returns khi KHÔNG có task:
    {
        "status": "idle",
        "message": "Không có task phù hợp. Thử lại sau 20 giây."
    }
    
    Logic nội bộ:
    - PLANNER nhận task khi status = PENDING
    - CODER nhận task khi status = PLAN_READY
    - REVIEWER nhận task khi status = CODE_READY
    - Khi nhận: set lock_owner = role, lock_heartbeat = now, cập nhật status
    - Kèm theo artifact từ phase trước để Worker có đủ context
    """
```

### Tool 3: `submit_phase`

```python
@mcp.tool()
def submit_phase(task_id: str, role: str, summary: str, artifact_content: str, artifact_type: str) -> str:
    """
    Dùng bởi: Workers sau khi hoàn thành công việc.
    Nộp kết quả và chuyển task sang phase tiếp theo.
    
    Args:
        task_id: UUID của task
        role: "PLANNER" | "CODER" | "REVIEWER"
        summary: Tóm tắt ngắn những gì đã làm
        artifact_content: Nội dung chi tiết kết quả (markdown hoặc JSON)
        artifact_type: "plan" | "code_changes" | "review_report"
    
    Returns:
    {
        "status": "success",
        "task_id": "uuid",
        "next_phase": "PLAN_READY | CODE_READY | FINISHED",
        "message": "Phase PLANNING hoàn thành. Task chuyển sang PLAN_READY."
    }
    
    Logic chuyển phase:
    - PLANNER submit → status: PLANNING → PLAN_READY
    - CODER submit → status: CODING → CODE_READY
    - REVIEWER submit → status: REVIEWING → FINISHED
    - Xóa lock sau khi submit
    """
```

### Tool 4: `send_heartbeat`

```python
@mcp.tool()
def send_heartbeat(task_id: str, role: str) -> str:
    """
    Dùng bởi: Workers trong khi đang xử lý task dài.
    Cập nhật timestamp để Hub biết Worker vẫn đang sống.
    Gọi mỗi 60 giây khi đang làm task phức tạp.
    
    Args:
        task_id: UUID của task đang xử lý
        role: Role của Worker đang gửi heartbeat
    
    Returns:
    {
        "status": "ok",
        "message": "Heartbeat đã được ghi nhận."
    }
    """
```

### Tool 5: `get_task_status`

```python
@mcp.tool()
def get_task_status(task_id: str) -> str:
    """
    Dùng bởi: Master để theo dõi tiến độ.
    
    Returns:
    {
        "task_id": "uuid",
        "goal": "...",
        "status": "CODING",
        "current_phase": "CODER",
        "lock_owner": "CODER",
        "artifacts": {
            "plan": "có | không",
            "code_changes": "có | không",
            "review_report": "có | không"
        },
        "history": [
            {"actor": "PLANNER", "action": "submitted", "summary": "...", "timestamp": "..."},
            ...
        ]
    }
    """
```

### Tool 6: `cancel_task`

```python
@mcp.tool()
def cancel_task(task_id: str) -> str:
    """
    Dùng bởi: Master khi muốn hủy task đang chạy.
    Set status = CANCELLED, xóa lock.
    
    Returns:
    {
        "status": "cancelled",
        "task_id": "uuid",
        "message": "Task đã bị hủy."
    }
    """
```

---

## 📝 Worker Skill — Kịch bản chạy tự động

**File:** `skills/pipeline_worker_skill.md`

```markdown
# Pipeline Worker Skill

## Cách Worker vận hành (Vòng lặp vô tận)

Bạn là [ROLE]. Bạn sẽ chạy vòng lặp sau MÃI MÃI cho đến khi được yêu cầu dừng:

### BƯỚC 1 — Hỏi Hub
Gọi MCP tool: `poll_task(role="[ROLE]")`

### BƯỚC 2 — Xử lý phản hồi

**Nếu status = "idle":**
- Hiện thị: "⏳ [ROLE] đang chờ task... (thử lại sau 20s)"
- Đợi 20 giây
- QUAY LẠI Bước 1

**Nếu status = "task_available":**
- Hiển thị: "🎯 Nhận task: [goal]"
- Thực hiện công việc theo chuyên môn (xem bên dưới)
- Gọi `submit_phase(...)` để nộp kết quả
- Hiển thị: "✅ [ROLE] hoàn thành. Chuyển task tiếp theo."
- QUAY LẠI Bước 1

**Nếu có lỗi:**
- Hiển thị: "⚠️ Lỗi: [mô tả lỗi]. Thử lại sau 30s..."
- Đợi 30 giây
- QUAY LẠI Bước 1

### BƯỚC 3 — Công việc theo role

**PLANNER làm gì khi có task:**
1. Đọc `project_path` và `context_files` từ task
2. Khảo sát cấu trúc thư mục dự án
3. Xác định Scope Lock (các file sẽ tạo/sửa)
4. Viết Implementation Plan chi tiết (markdown)
5. Submit với `artifact_type="plan"`

**CODER làm gì khi có task:**
1. Đọc nội dung `previous_artifacts.plan` từ Hub
2. Thực hiện đúng theo Scope Lock trong plan
3. Viết code với comment tiếng Việt
4. Tổng hợp danh sách file đã sửa
5. Submit với `artifact_type="code_changes"`

**REVIEWER làm gì khi có task:**  
1. Đọc `previous_artifacts.plan` và `previous_artifacts.code_changes`
2. Kiểm tra code có đúng với plan không
3. Tìm bug, side-effects, vấn đề bảo mật
4. Viết review report rõ ràng
5. Submit với `artifact_type="review_report"`

### Lưu ý quan trọng:
- Trong khi làm task phức tạp (> 1 phút), gọi `send_heartbeat()` mỗi 60s
- KHÔNG tự dừng vòng lặp trừ khi người dùng yêu cầu
- Mỗi lần bắt đầu vòng lặp mới, hiển thị trạng thái ngắn gọn
```

---

## 💻 Đặc tả code chi tiết

### `hub_models.py`

```python
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    PLANNING = "PLANNING"
    PLAN_READY = "PLAN_READY"
    CODING = "CODING"
    CODE_READY = "CODE_READY"
    REVIEWING = "REVIEWING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class WorkerRole(str, Enum):
    PLANNER = "PLANNER"
    CODER = "CODER"
    REVIEWER = "REVIEWER"

# Mapping: mỗi Role nhận task ở status nào
ROLE_PHASE_MAP = {
    WorkerRole.PLANNER: TaskStatus.PENDING,
    WorkerRole.CODER: TaskStatus.PLAN_READY,
    WorkerRole.REVIEWER: TaskStatus.CODE_READY,
}

# Mapping: sau khi submit thì chuyển sang status nào
SUBMIT_NEXT_STATUS = {
    WorkerRole.PLANNER: TaskStatus.PLAN_READY,
    WorkerRole.CODER: TaskStatus.CODE_READY,
    WorkerRole.REVIEWER: TaskStatus.FINISHED,
}
```

### `hub_database.py`

```python
"""
hub_database.py
Vai trò: Quản lý toàn bộ thao tác SQLite cho Hub.
Mọi function đều thread-safe nhờ SQLite WAL mode.
"""
import sqlite3
import uuid
import json
from datetime import datetime, timezone
from hub_models import TaskStatus, WorkerRole, ROLE_PHASE_MAP, SUBMIT_NEXT_STATUS

DB_PATH = "hub.db"  # Đặt cùng thư mục với hub_server.py
HEARTBEAT_TIMEOUT_SECONDS = 180  # 3 phút

def get_connection():
    """Tạo connection SQLite với WAL mode để tránh lock conflict."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row  # Truy xuất theo tên cột
    return conn

def init_db():
    """Khởi tạo schema database nếu chưa có."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                goal TEXT NOT NULL,
                project_path TEXT NOT NULL,
                context TEXT,
                status TEXT NOT NULL DEFAULT 'PENDING',
                current_phase TEXT,
                lock_owner TEXT,
                lock_heartbeat TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS artifacts (
                id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL REFERENCES tasks(id),
                phase TEXT NOT NULL,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS history (
                id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL REFERENCES tasks(id),
                phase TEXT NOT NULL,
                actor TEXT NOT NULL,
                action TEXT NOT NULL,
                summary TEXT,
                timestamp TEXT NOT NULL
            );
        """)

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def create_task(goal: str, project_path: str, context_files: list) -> str:
    """Tạo task mới, trả về task_id."""
    task_id = str(uuid.uuid4())
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO tasks (id, goal, project_path, context, status, created_at, updated_at)
               VALUES (?, ?, ?, ?, 'PENDING', ?, ?)""",
            (task_id, goal, project_path, json.dumps(context_files), now_iso(), now_iso())
        )
        conn.execute(
            "INSERT INTO history (id, task_id, phase, actor, action, summary, timestamp) VALUES (?,?,?,?,?,?,?)",
            (str(uuid.uuid4()), task_id, "INIT", "MASTER", "dispatched", goal, now_iso())
        )
    return task_id

def poll_for_role(role: str) -> dict | None:
    """
    Tìm task phù hợp với role và claim nó (atomic).
    Trả về dict task hoặc None nếu không có.
    """
    # Trước tiên: kiểm tra và release các lock bị timeout
    _release_timed_out_locks()
    
    target_status = ROLE_PHASE_MAP[WorkerRole(role)].value
    with get_connection() as conn:
        # Tìm task phù hợp (chưa bị lock)
        row = conn.execute(
            """SELECT * FROM tasks 
               WHERE status = ? AND lock_owner IS NULL
               ORDER BY created_at ASC LIMIT 1""",
            (target_status,)
        ).fetchone()
        
        if not row:
            return None
        
        task = dict(row)
        # Claim task: set lock và chuyển status
        new_status = {
            "PENDING": "PLANNING",
            "PLAN_READY": "CODING",
            "CODE_READY": "REVIEWING"
        }[target_status]
        
        conn.execute(
            """UPDATE tasks SET status=?, current_phase=?, lock_owner=?, lock_heartbeat=?, updated_at=?
               WHERE id=? AND lock_owner IS NULL""",
            (new_status, role, role, now_iso(), now_iso(), task["id"])
        )
        
        # Ghi history
        conn.execute(
            "INSERT INTO history (id, task_id, phase, actor, action, summary, timestamp) VALUES (?,?,?,?,?,?,?)",
            (str(uuid.uuid4()), task["id"], new_status, role, "claimed", f"{role} bắt đầu xử lý", now_iso())
        )
        
        # Lấy artifacts từ các phase trước
        artifacts_rows = conn.execute(
            "SELECT phase, type, content FROM artifacts WHERE task_id=? ORDER BY created_at",
            (task["id"],)
        ).fetchall()
        
        previous_artifacts = {}
        for ar in artifacts_rows:
            previous_artifacts[ar["type"]] = ar["content"]
        
        task["previous_artifacts"] = previous_artifacts
        task["context_files"] = json.loads(task["context"] or "[]")
        return task

def submit_phase_result(task_id: str, role: str, summary: str, artifact_content: str, artifact_type: str) -> str:
    """Lưu artifact và chuyển task sang phase tiếp theo."""
    next_status = SUBMIT_NEXT_STATUS[WorkerRole(role)].value
    with get_connection() as conn:
        # Lưu artifact
        conn.execute(
            "INSERT INTO artifacts (id, task_id, phase, type, content, created_at) VALUES (?,?,?,?,?,?)",
            (str(uuid.uuid4()), task_id, role, artifact_type, artifact_content, now_iso())
        )
        # Cập nhật task: chuyển phase, xóa lock
        conn.execute(
            """UPDATE tasks SET status=?, lock_owner=NULL, lock_heartbeat=NULL, current_phase=NULL, updated_at=?
               WHERE id=?""",
            (next_status, now_iso(), task_id)
        )
        # Ghi history
        conn.execute(
            "INSERT INTO history (id, task_id, phase, actor, action, summary, timestamp) VALUES (?,?,?,?,?,?,?)",
            (str(uuid.uuid4()), task_id, role, role, "submitted", summary, now_iso())
        )
    return next_status

def update_heartbeat(task_id: str, role: str) -> bool:
    """Cập nhật heartbeat timestamp."""
    with get_connection() as conn:
        result = conn.execute(
            "UPDATE tasks SET lock_heartbeat=?, updated_at=? WHERE id=? AND lock_owner=?",
            (now_iso(), now_iso(), task_id, role)
        )
        return result.rowcount > 0

def _release_timed_out_locks():
    """Tự động unlock task mà Worker đã bị timeout (không heartbeat > 3 phút)."""
    from datetime import timedelta
    cutoff = (datetime.now(timezone.utc) - timedelta(seconds=HEARTBEAT_TIMEOUT_SECONDS)).isoformat()
    
    # Map status hiện tại → status trước đó (rollback)
    rollback_map = {
        "PLANNING": "PENDING",
        "CODING": "PLAN_READY",
        "REVIEWING": "CODE_READY"
    }
    with get_connection() as conn:
        for current, previous in rollback_map.items():
            conn.execute(
                """UPDATE tasks SET status=?, lock_owner=NULL, lock_heartbeat=NULL, updated_at=?
                   WHERE status=? AND lock_heartbeat < ? AND lock_heartbeat IS NOT NULL""",
                (previous, now_iso(), current, cutoff)
            )
```

### `hub_server.py`

```python
"""
hub_server.py
Vai trò: MCP Server chính — expose 6 tools cho Antigravity.
Chạy: uv run python hub_server.py (hoặc python hub_server.py)
Transport: stdio (tích hợp với VS Code MCP config)
"""
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from mcp.server.fastmcp import FastMCP
import hub_database as db

# Khởi tạo DB khi server start
db.init_db()

mcp = FastMCP("IrukaHub")

@mcp.tool()
def dispatch_task(goal: str, project_path: str, context_files: list[str] = []) -> str:
    """Tạo task mới, đẩy vào Hub để Workers nhận. Dùng bởi Master."""
    task_id = db.create_task(goal, project_path, context_files)
    return json.dumps({
        "task_id": task_id,
        "status": "PENDING",
        "message": f"Task đã được tạo. Workers sẽ tự động nhận. ID: {task_id}"
    }, ensure_ascii=False)

@mcp.tool()
def poll_task(role: str) -> str:
    """Hỏi Hub xem có task không. Dùng bởi Workers (PLANNER/CODER/REVIEWER)."""
    if role not in ["PLANNER", "CODER", "REVIEWER"]:
        return json.dumps({"status": "error", "message": f"Role không hợp lệ: {role}"})
    
    task = db.poll_for_role(role)
    if not task:
        return json.dumps({
            "status": "idle",
            "message": f"Không có task cho {role}. Thử lại sau 20 giây."
        }, ensure_ascii=False)
    
    return json.dumps({
        "status": "task_available",
        "task_id": task["id"],
        "goal": task["goal"],
        "project_path": task["project_path"],
        "context_files": task["context_files"],
        "previous_artifacts": task["previous_artifacts"]
    }, ensure_ascii=False)

@mcp.tool()
def submit_phase(task_id: str, role: str, summary: str, artifact_content: str, artifact_type: str) -> str:
    """Nộp kết quả phase, chuyển task sang bước tiếp. Dùng bởi Workers."""
    next_status = db.submit_phase_result(task_id, role, summary, artifact_content, artifact_type)
    return json.dumps({
        "status": "success",
        "task_id": task_id,
        "next_phase": next_status,
        "message": f"Phase {role} hoàn thành. Task → {next_status}."
    }, ensure_ascii=False)

@mcp.tool()
def send_heartbeat(task_id: str, role: str) -> str:
    """Cập nhật heartbeat khi đang xử lý task dài. Gọi mỗi 60s."""
    success = db.update_heartbeat(task_id, role)
    return json.dumps({
        "status": "ok" if success else "error",
        "message": "Heartbeat ghi nhận." if success else "Không tìm thấy task hoặc không phải owner."
    }, ensure_ascii=False)

@mcp.tool()
def get_task_status(task_id: str) -> str:
    """Kiểm tra trạng thái task. Dùng bởi Master để theo dõi tiến độ."""
    import sqlite3
    with db.get_connection() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not row:
            return json.dumps({"status": "error", "message": "Task không tồn tại."})
        
        task = dict(row)
        artifacts = conn.execute(
            "SELECT type FROM artifacts WHERE task_id=?", (task_id,)
        ).fetchall()
        history = conn.execute(
            "SELECT actor, action, summary, timestamp FROM history WHERE task_id=? ORDER BY timestamp",
            (task_id,)
        ).fetchall()
        
        return json.dumps({
            "task_id": task_id,
            "goal": task["goal"],
            "status": task["status"],
            "lock_owner": task["lock_owner"],
            "artifacts_available": [a["type"] for a in artifacts],
            "history": [dict(h) for h in history]
        }, ensure_ascii=False)

@mcp.tool()
def cancel_task(task_id: str) -> str:
    """Hủy task đang chạy. Dùng bởi Master."""
    with db.get_connection() as conn:
        conn.execute(
            "UPDATE tasks SET status='CANCELLED', lock_owner=NULL, updated_at=? WHERE id=?",
            (db.now_iso(), task_id)
        )
        conn.execute(
            "INSERT INTO history (id, task_id, phase, actor, action, summary, timestamp) VALUES (?,?,?,?,?,?,?)",
            (db.str(db.uuid.uuid4()), task_id, "CANCEL", "MASTER", "cancelled", "Master hủy task", db.now_iso())
        )
    return json.dumps({"status": "cancelled", "task_id": task_id}, ensure_ascii=False)

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### `requirements.txt`

```
mcp[cli]>=1.0.0
fastmcp>=0.1.0
pydantic>=2.0.0
```

---

## 🔧 Cấu hình VS Code MCP (`settings.json`)

Thêm vào `.vscode/settings.json` của **cả 3 cửa sổ VS Code**:

```json
{
    "mcp": {
        "servers": {
            "iruka-hub": {
                "type": "stdio",
                "command": "uv",
                "args": [
                    "run",
                    "python",
                    "AI/agent-mcp/hub_server.py"
                ]
            }
        }
    }
}
```

> **Lưu ý:** Cả 3 cửa sổ đều kết nối vào cùng 1 `hub.db`. SQLite WAL mode đảm bảo không conflict.

---

## 🚀 Hướng dẫn vận hành hàng ngày

### Buổi sáng — Setup 1 lần (tổng ~2 phút)

```
Bước 1: Mở VS Code cửa sổ 1 (Account Google #1) — đây là MASTER
         → Mở project game như bình thường

Bước 2: Mở VS Code cửa sổ 2 (Account Google #2)
         → Mở thư mục bất kỳ (không cần mở project)
         → Chat với Antigravity: "Bạn là PLANNER. Hãy chạy Pipeline Worker Skill."

Bước 3: Mở VS Code cửa sổ 3 (Account Google #3)
         → Mở thư mục bất kỳ
         → Chat với Antigravity: "Bạn là CODER. Hãy chạy Pipeline Worker Skill."

→ Cả 2 Worker bắt đầu poll Hub mỗi 20 giây. Hiện: "⏳ Đang chờ task..."
```

### Làm việc — Chỉ cần làm ở cửa sổ 1

```
Gõ trong chat:
"dispatch_task với goal='Thêm logic hint sau 5s idle vào TraceScene',
 project_path='d:/works/Game/work-space/vietnamese-game-age-4to5/trace'"

→ Tự động xảy ra:
   1. Hub tạo task ID: abc-123
   2. PLANNER nhận task → khảo sát code → viết plan → submit
   3. CODER nhận plan → viết code → submit
   4. Master nhận thông báo hoàn thành

Theo dõi: "get_task_status với task_id='abc-123'"
```

---

## ⚠️ Rủi ro & Phòng ngừa

| Rủi ro | Cơ chế phòng ngừa |
|--------|-------------------|
| Worker crash giữa chừng | Heartbeat timeout 3 phút → Hub tự unlock |
| 2 Worker cùng claim 1 task | SQLite `WHERE lock_owner IS NULL` atomic |
| File DB bị corrupt | WAL mode + transaction bọc mọi thao tác |
| Worker ghi sai file | Scope Lock trong plan — Coder phải tuân theo |
| Master không biết tiến độ | `get_task_status` + history log |

---

## 📊 Scope Lock — File cần tạo/sửa

| File | Action | Thực hiện bởi |
|------|--------|---------------|
| `hub_models.py` | CREATE | Developer |
| `hub_database.py` | CREATE | Developer |
| `hub_server.py` | CREATE | Developer |
| `requirements.txt` | CREATE | Developer |
| `skills/pipeline_worker_skill.md` | CREATE | Developer |
| `.vscode/settings.json` (3 cửa sổ) | UPDATE | Developer |
| `README.md` | CREATE | Developer |

---

## ✅ Checklist kiểm tra sau khi build

```
[ ] hub_server.py chạy không lỗi: uv run python hub_server.py
[ ] DB hub.db được tạo tự động với đủ 3 bảng
[ ] Tool dispatch_task hoạt động: task xuất hiện trong DB
[ ] Tool poll_task(PLANNER) trả về task đúng khi status=PENDING
[ ] Tool submit_phase chuyển status PLANNING → PLAN_READY
[ ] Tool poll_task(CODER) trả về task đúng khi status=PLAN_READY
[ ] Heartbeat timeout: sau 3 phút không heartbeat → task unlock
[ ] End-to-end: PENDING → PLANNING → PLAN_READY → CODING → CODE_READY → REVIEWING → FINISHED
[ ] Cancel hoạt động: task chuyển sang CANCELLED, Worker bỏ qua
[ ] 3 VS Code window đều kết nối được Hub qua MCP settings
```
