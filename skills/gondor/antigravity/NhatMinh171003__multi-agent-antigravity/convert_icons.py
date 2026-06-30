import os
import sys
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw, ImageFont

def convert_png_to_ico(png_path, ico_name):
    if not os.path.exists(png_path):
        return False
    try:
        img = Image.open(png_path)
        # Crop center square if not square
        width, height = img.size
        size = min(width, height)
        left = (width - size)/2
        top = (height - size)/2
        right = (width + size)/2
        bottom = (height + size)/2
        img = img.crop((left, top, right, bottom))
        
        # Resize to 256x256
        img = img.resize((256, 256), Image.Resampling.LANCZOS)
        out_path = os.path.join(os.path.dirname(png_path), ico_name)
        img.save(out_path, format="ICO", sizes=[(256, 256)])
        print(f"✅ Converted: {out_path}")
        return True
    except Exception as e:
        print(f"Error converting {png_path}: {e}")
        return False

def generate_fallback_ico(role_name, color, ico_name, output_dir):
    try:
        # Create a blank image with a dark background
        img = Image.new('RGB', (256, 256), color=(20, 20, 25))
        draw = ImageDraw.Draw(img)
        
        # Draw a glowing border
        draw.rounded_rectangle([(10, 10), (246, 246)], radius=40, outline=color, width=8)
        draw.rounded_rectangle([(20, 20), (236, 236)], radius=30, outline=(color[0]//2, color[1]//2, color[2]//2), width=3)
        
        # Draw the first letter of the role
        text = role_name[0]
        # Calculate text position (basic center approximation without external fonts)
        draw.text((80, 60), text, fill=color, font=None)
        
        out_path = os.path.join(output_dir, ico_name)
        img.save(out_path, format="ICO", sizes=[(256, 256)])
        print(f"✅ Created synthetic icon: {out_path}")
    except Exception as e:
        print(f"Error generating {ico_name}: {e}")

if __name__ == "__main__":
    artifact_dir = r"C:\Users\Admin\.gemini\antigravity\brain\6ca6dcb7-9cf2-4fd6-b9ff-619506c50968"
    project_dir = r"d:\works\Game\work-space\AI\agent-mcp"
    
    # 1. Convert successful AI generations
    planner_png = os.path.join(artifact_dir, "ag_planner_1776430261934.png")
    reporter_png = os.path.join(artifact_dir, "ag_reporter_1776430277245.png")
    
    convert_png_to_ico(planner_png, "icon_PLANNER_v2.ico")
    convert_png_to_ico(reporter_png, "icon_REPORTER_v2.ico")
    
    coder_png = os.path.join(artifact_dir, "ag_coder_1776430461820.png")
    tester_png = os.path.join(artifact_dir, "ag_tester_1776430474700.png")
    reviewer_png = os.path.join(artifact_dir, "ag_reviewer_1776430490858.png")
    
    convert_png_to_ico(coder_png, "icon_CODER_v2.ico")
    convert_png_to_ico(tester_png, "icon_TESTER_v2.ico")
    convert_png_to_ico(reviewer_png, "icon_REVIEWER_v2.ico")
    
    # Also copy all 5 from artifact dir to project dir
    import shutil
    roles = ["PLANNER", "CODER", "TESTER", "REVIEWER", "REPORTER"]
    for role in roles:
        src = os.path.join(artifact_dir, f"icon_{role}_v2.ico")
        dst = os.path.join(project_dir, f"icon_{role}_v2.ico")
        if os.path.exists(src):
            shutil.copy(src, dst)
            print(f"Copied to {dst}")
