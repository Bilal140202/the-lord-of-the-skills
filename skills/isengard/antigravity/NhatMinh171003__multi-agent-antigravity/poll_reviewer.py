import sys
import time
import os

# Thêm đường dẫn để import hub_database
sys.path.append(os.path.join(os.getcwd(), 'AI', 'agent-mcp'))

try:
    import hub_database
    hub_database.init_db()
except ImportError:
    print("Error: Could not import hub_database. Check path.", flush=True)
    sys.exit(1)

def poll_loop(iterations=10, delay=2):
    print(f"Starting poll loop for REVIEWER role ({iterations} iterations)...", flush=True)
    for i in range(iterations):
        task = hub_database.poll_for_role('REVIEWER')
        if not task:
            print(f"Poll {i+1}: idle", flush=True)
        elif task.get("status") == "keep_alive":
            print(f"Poll {i+1}: keep_alive (timeout)", flush=True)
        else:
            # Chuyển đổi dict sang string để in ra
            import json
            print(f"TASK_FOUND: {json.dumps(task, ensure_ascii=False)}", flush=True)
            return
        
        if i < iterations - 1:
            time.sleep(delay)
    print("FINAL_STATUS: idle", flush=True)

if __name__ == "__main__":
    poll_loop()
