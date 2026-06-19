"""
hub_models.py (Dynamic V2)
Thay vì hardcode Enum, giờ đây cấu hình pipeline được nạp động từ pipeline.json.
User chỉ cần sửa json là hệ thống hiểu luồng tiếp theo.
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINE_FILE = os.path.join(BASE_DIR, "pipeline.json")

def load_pipeline():
    try:
        with open(PIPELINE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [r.upper() for r in data.get("sequence", [])]
    except Exception:
        # Fallback nếu file lỗi
        return ["PLANNER", "CODER", "REVIEWER"]

# Mảng chứa danh sách thứ tự xử lý của các Role
SEQUENCE = load_pipeline()

def get_valid_roles():
    return SEQUENCE

def get_target_status(role: str) -> str:
    """Task phải ở status nào thì Role này được phép bốc?"""
    role = role.upper()
    if role not in SEQUENCE:
        raise ValueError(f"Role {role} không nằm trong pipeline sequence.")
    
    idx = SEQUENCE.index(role)
    if idx == 0:
        return "PENDING"
    # Role đứng thứ idx sẽ đợi task hoàn thành bởi role trước đó
    return f"{SEQUENCE[idx-1]}_READY"

def get_running_status(role: str) -> str:
    """Khi Role đang xử lý task, status chuyển thành gì?"""
    return f"{role.upper()}_ING"

def get_next_status(role: str) -> str:
    """Sau khi Role submit, task chuyển thành status nào?"""
    role = role.upper()
    idx = SEQUENCE.index(role)
    if idx == len(SEQUENCE) - 1:
        return "FINISHED"
    return f"{role}_READY"

def get_rollback_map() -> dict:
    """Tự động sinh dictionary [RUNNING_STATUS] -> [PREVIOUS_STATUS] dùng để Rollback Timeout"""
    rmap = {}
    for role in SEQUENCE:
        ing_status = get_running_status(role)
        prev_status = get_target_status(role)
        rmap[ing_status] = prev_status
    return rmap
