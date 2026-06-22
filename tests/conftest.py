"""Test fixtures and configuration."""
import sys
from pathlib import Path

# Ensure crawler/ is importable
CRAWLER_DIR = Path(__file__).parent.parent / "crawler"
if str(CRAWLER_DIR) not in sys.path:
    sys.path.insert(0, str(CRAWLER_DIR))

# Ensure scripts/ is importable (for restructure_repo etc.)
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
if Path(SCRIPTS_DIR).exists() and str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
