"""
hub_server.py
Vai trò: MCP Server chính — expose 6 tools cho Antigravity.
Chạy: uv run python hub_server.py (hoặc python hub_server.py)
Transport: stdio (tích hợp với VS Code MCP config)
"""
import json
import sys
import io

import uuid
# Ép buộc stdout/stderr dùng UTF-8 trên Windows
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
    """Hỏi Hub xem có task không. Dùng bởi Workers."""
    import hub_models
    valid_roles = hub_models.get_valid_roles()
    role = str(role).upper()
    if role not in valid_roles:
        return json.dumps({"status": "error", "message": f"Role không hợp lệ: {role}. Chỉ hỗ trợ {valid_roles}"}, ensure_ascii=False)
    
    try:
        task = db.poll_for_role(role)
        if not task:
            return json.dumps({
                "status": "idle",
                "message": f"Không có task cho {role}. Thử lại sau 20 giây."
            }, ensure_ascii=False)
        
        if task.get("status") == "keep_alive":
            return json.dumps(task, ensure_ascii=False)
            
        sys.stderr.write(f"DEBUG: Task found for {role}: {list(task.keys()) if isinstance(task, dict) else type(task)}\n")
        
        return json.dumps({
            "status": "task_available",
            "task_id": task.get("id"),
            "goal": task.get("goal"),
            "project_path": task.get("project_path"),
            "context_files": task.get("context_files", []),
            "previous_artifacts": task.get("previous_artifacts", {})
        }, ensure_ascii=False)
    except Exception as e:
        import traceback
        err_msg = f"Error in poll_task: {str(e)}\n{traceback.format_exc()}"
        sys.stderr.write(err_msg)
        return json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False)



@mcp.tool()
def submit_phase(task_id: str, role: str, summary: str, artifact_content: str, artifact_type: str) -> str:
    """Nộp kết quả phase, chuyển task sang bước tiếp. Dùng bởi Workers."""
    role = str(role).upper()
    try:
        next_status = db.submit_phase_result(task_id, role, summary, artifact_content, artifact_type)
        return json.dumps({
            "status": "success",
            "task_id": task_id,
            "next_phase": next_status,
            "message": f"Phase {role} hoàn thành. Task → {next_status}."
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False)

@mcp.tool()
def reject_phase(task_id: str, role: str, bug_report: str) -> str:
    """TESTER dùng khi phát hiện lỗi nghiêm trọng. Trả task về CODER để sửa thay vì đẩy sang REPORTER."""
    role = str(role).upper()
    try:
        result = db.reject_phase(task_id, role, bug_report)
        if result["status"] == "rejected_back_to_coder":
            return json.dumps({
                "status": "rejected",
                "message": f"Task trả về CODER. Lần reject thứ {result['retry_count']}. Còn {result['remaining']} lần retry.",
                "task_id": task_id
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "status": "max_retry_exceeded",
                "message": f"Đã reject {result['retries']} lần (tối đa). Chuyển REPORTER báo cáo lỗi.",
                "task_id": task_id
            }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False)


@mcp.tool()
def send_heartbeat(task_id: str, role: str) -> str:
    """Cập nhật heartbeat khi đang xử lý task dài. Gọi mỗi 60s."""
    role = str(role).upper()
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
            (str(uuid.uuid4()), task_id, "CANCEL", "MASTER", "cancelled", "Master hủy task", db.now_iso())
        )
    return json.dumps({"status": "cancelled", "task_id": task_id}, ensure_ascii=False)

if __name__ == "__main__":
    mcp.run(transport="stdio")
