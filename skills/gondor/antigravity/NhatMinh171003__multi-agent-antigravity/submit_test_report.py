import sys
import os
import json

# Thêm đường dẫn để import hub_database
sys.path.append(os.path.join(os.getcwd(), 'AI', 'agent-mcp'))

try:
    import hub_database
    from hub_models import WorkerRole
except ImportError:
    print("Error: Could not import hub_database or hub_models.")
    sys.exit(1)

def submit_test():
    task_id = "3f9dd2d5-e65d-4738-9ef6-a30e5b3c05be"
    role = "TESTER"
    
    report = {
        "status": "failed",
        "errors": [
            "Thiếu file assets/data/level_meta.json khiến BootScene fallback về ['trace1', 'trace2'], không load được phase 'paint'.",
            "Thiếu asset decoration: assets/images/decoration/deco1.png.",
            "Lỗi giải mã âm thanh (Decoding audio failed) cho hint_paint.mp3 và intro_paint.mp3.",
            "ColorLetterLevel báo lỗi thiếu 'trace_target' khi quét phase 'paint' (do logic loop chung)."
        ],
        "recommendations": [
            "Tạo file level_meta.json với nội dung { \"phases\": [\"trace1\", \"paint\"] }.",
            "Bổ sung asset deco1.png vào đúng thư mục hoặc gỡ bỏ config decoration trong manifest_trace1.",
            "Kiểm tra lại định dạng file audio hint_paint.mp3 và intro_paint.mp3.",
            "Cập nhật ColorLetterLevel để bỏ qua kiểm tra 'trace_target' nếu phase đó là paint."
        ]
    }
    
    summary = "Kiểm thử thất bại. Phát hiện lỗi cấu hình phase và thiếu asset."
    
    try:
        next_status = hub_database.submit_phase_result(
            task_id=task_id,
            role=role,
            summary=summary,
            artifact_content=json.dumps(report, ensure_ascii=False),
            artifact_type="test_report"
        )
        print(f"SUCCESS: Submitted test_report. Next status: {next_status}")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    submit_test()
