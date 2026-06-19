"""
hub_database.py
Vai trò: Quản lý toàn bộ thao tác SQLite cho Hub.
Mọi function đều thread-safe nhờ SQLite WAL mode.
"""
import sqlite3
import uuid
import json
import os
from datetime import datetime, timezone
import hub_models

# Lấy đường dẫn cùng thư mục với script này
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "hub.db")
HEARTBEAT_TIMEOUT_SECONDS = 180  # 3 phút

def get_connection():
    """Tạo connection SQLite với WAL mode để tránh lock conflict."""
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
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
    Hỗ trợ Long Polling: Đợi tối đa 20s nếu chưa có task.
    """
    import time
    
    attempts = 0
    max_attempts = 22  # 44s
    
    while attempts < max_attempts:
        _release_timed_out_locks()
        
        target_status = hub_models.get_target_status(role)
        with get_connection() as conn:
            row = conn.execute(
                """SELECT * FROM tasks 
                   WHERE status = ? AND lock_owner IS NULL
                   ORDER BY created_at ASC LIMIT 1""",
                (target_status,)
            ).fetchone()
            
            if row:
                task = dict(row)
                new_status = hub_models.get_running_status(role)
                
                try:
                    conn.execute(
                        """UPDATE tasks SET status=?, current_phase=?, lock_owner=?, lock_heartbeat=?, updated_at=?
                           WHERE id=? AND lock_owner IS NULL""",
                        (new_status, role, role, now_iso(), now_iso(), task["id"])
                    )
                    
                    conn.execute(
                        "INSERT INTO history (id, task_id, phase, actor, action, summary, timestamp) VALUES (?,?,?,?,?,?,?)",
                        (str(uuid.uuid4()), task["id"], new_status, role, "claimed", f"{role} bắt đầu xử lý", now_iso())
                    )
                    
                    artifacts_rows = conn.execute(
                        "SELECT phase, type, content FROM artifacts WHERE task_id=? ORDER BY created_at",
                        (task["id"],)
                    ).fetchall()
                    
                    previous_artifacts = {}
                    for ar in artifacts_rows:
                        previous_artifacts[ar["type"]] = ar["content"]
                    
                    # Ensure task has an id even if dict(row) fails slightly
                    if "id" not in task:
                        task["id"] = row["id"]
                    
                    task["previous_artifacts"] = previous_artifacts
                    task["context_files"] = json.loads(task["context"] or "[]")
                    task["status"] = new_status
                    task["lock_owner"] = role
                    return task
                except (sqlite3.Error, KeyError, Exception) as e:
                    import sys
                    sys.stderr.write(f"DEBUG: Error processing row in poll_for_role: {e}\n")
                    pass
        
        time.sleep(2)
        attempts += 1
        
    return {"status": "keep_alive", "role": role}

def submit_phase_result(task_id: str, role: str, summary: str, artifact_content: str, artifact_type: str) -> str:
    """Lưu artifact và chuyển task sang phase tiếp theo."""
    next_status = hub_models.get_next_status(role)
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

def reject_phase(task_id: str, role: str, bug_report: str, max_retries: int = 3) -> dict:
    """
    TESTER gọi hàm này khi phát hiện lỗi nghiêm trọng.
    Trả task ngược về CODER để sửa (thay vì chuyển sang REPORTER).
    Có cơ chế max_retries để tránh vòng lặp vô tận.
    """
    with get_connection() as conn:
        # Đếm số lần task đã bị reject trước đó
        reject_count = conn.execute(
            "SELECT COUNT(*) FROM history WHERE task_id=? AND action='rejected'",
            (task_id,)
        ).fetchone()[0]
        
        if reject_count >= max_retries:
            # Đã vượt quá số lần retry → Chuyển sang REPORTER để báo cáo lỗi
            next_status = hub_models.get_next_status(role)
            conn.execute(
                """UPDATE tasks SET status=?, lock_owner=NULL, lock_heartbeat=NULL, updated_at=?
                   WHERE id=?""",
                (next_status, now_iso(), task_id)
            )
            conn.execute(
                "INSERT INTO artifacts (id, task_id, phase, type, content, created_at) VALUES (?,?,?,?,?,?)",
                (str(uuid.uuid4()), task_id, role, "test_report_final_fail", bug_report, now_iso())
            )
            conn.execute(
                "INSERT INTO history (id, task_id, phase, actor, action, summary, timestamp) VALUES (?,?,?,?,?,?,?)",
                (str(uuid.uuid4()), task_id, role, role, "rejected_max_retry",
                 f"Đã reject {reject_count} lần, vượt ngưỡng. Chuyển REPORTER.", now_iso())
            )
            return {"status": "max_retry_exceeded", "next": next_status, "retries": reject_count}
        
        # Còn trong ngưỡng → Trả về CODER_READY
        conn.execute(
            "INSERT INTO artifacts (id, task_id, phase, type, content, created_at) VALUES (?,?,?,?,?,?)",
            (str(uuid.uuid4()), task_id, role, "bug_report", bug_report, now_iso())
        )
        conn.execute(
            """UPDATE tasks SET status='CODER_READY', lock_owner=NULL, lock_heartbeat=NULL,
               current_phase=NULL, updated_at=? WHERE id=?""",
            (now_iso(), task_id)
        )
        conn.execute(
            "INSERT INTO history (id, task_id, phase, actor, action, summary, timestamp) VALUES (?,?,?,?,?,?,?)",
            (str(uuid.uuid4()), task_id, role, role, "rejected",
             f"Lần {reject_count + 1}: TESTER reject → trả về CODER. Lỗi: {bug_report[:100]}", now_iso())
        )
    return {"status": "rejected_back_to_coder", "retry_count": reject_count + 1, "remaining": max_retries - reject_count - 1}


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
    
    # Lấy map động rollback từ hub_models
    rollback_map = hub_models.get_rollback_map()
    with get_connection() as conn:
        for current, previous in rollback_map.items():
            conn.execute(
                """UPDATE tasks SET status=?, lock_owner=NULL, lock_heartbeat=NULL, updated_at=?
                   WHERE status=? AND lock_heartbeat < ? AND lock_heartbeat IS NOT NULL""",
                (previous, now_iso(), current, cutoff)
            )
