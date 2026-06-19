import sys
import time
import os
import json

# Thêm đường dẫn để import hub_database
sys.path.append(os.path.join(os.getcwd(), 'AI', 'agent-mcp'))

try:
    import hub_database
    hub_database.init_db()
except ImportError:
    print(json.dumps({"status": "error", "message": "Could not import hub_database. Check path."}), flush=True)
    sys.exit(1)

def poll_once():
    role = 'CODER'
    task = hub_database.poll_for_role(role)
    if not task:
        return {"status": "idle", "message": f"Không có task cho {role}."}
    
    # Xử lý trường hợp keep_alive (timeout)
    if task.get("status") == "keep_alive":
        return task
    
    return {
        "status": "task_available",
        "task_id": task["id"],
        "goal": task["goal"],
        "project_path": task["project_path"],
        "context_files": task["context_files"],
        "previous_artifacts": task["previous_artifacts"]
    }

if __name__ == "__main__":
    result = poll_once()
    print(json.dumps(result, ensure_ascii=False), flush=True)
