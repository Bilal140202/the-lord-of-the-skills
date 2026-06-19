#!/usr/bin/env bash
# Lord of the Skills — Monthly Refresh Script
# ============================================
# Re-runs the full pipeline to refresh the package with newly-published skills.
# Scheduled monthly via cron: 1st of month at 03:00 IST.
#
# Steps:
#   1. Crawler (spider GitHub, clone new repos, extract skill files)
#   2. Classifier (tag each file with LOTR kingdom + framework + skill type)
#   3. Dedup (cluster similar, mark canonical ⭐)
#   4. Build package (themed folder structure + README + CREDITS + MAP + INDEX)
#   5. Generate Excel index
#   6. Generate PDF master catalog
#
# Usage:
#   bash /home/z/my-project/scripts/refresh_lord_of_skills.sh
#
# Cron schedule (1st of month at 03:00 IST = 21:30 UTC on last day of month):
#   30 21 28-31 * * [ "$(date -d '+1 day' +%d)" = "01" ] && /home/z/my-project/scripts/refresh_lord_of_skills.sh

set -euo pipefail

PROJECT_ROOT="/home/z/my-project"
SCRIPTS="$PROJECT_ROOT/scripts"
WORK_ROOT="$PROJECT_ROOT/the-lord-of-the-skills"
LOG="$WORK_ROOT/_cache/refresh-$(date +%Y%m%d-%H%M%S).log"

mkdir -p "$WORK_ROOT/_cache"

exec > >(tee -a "$LOG") 2>&1
echo "============================================================"
echo "Lord of the Skills — Refresh started at $(date -Iseconds)"
echo "============================================================"

# Pre-flight: ensure Python is available
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 not found"
    exit 1
fi

# Step 0: Reset phase-completion state so crawler re-runs (but keeps cached repos)
# (We do NOT delete _cache/repos/ — git clone skips already-cloned repos, so this is incremental.)
STATE="$WORK_ROOT/_cache/crawler_state.json"
if [ -f "$STATE" ]; then
    echo "Resetting phase-completion state (keeping cached repos for incremental update)..."
    python3 -c "
import json
s = json.load(open('$STATE'))
s['phase_completed'] = []  # force re-run of all phases
# but keep cloned_repos and discovered_repos so we don't re-clone
json.dump(s, open('$STATE', 'w'), indent=2)
"
fi

# Step 1: Crawler (resumable — skips already-cloned repos)
echo ""
echo "[1/6] Crawler — discover + clone + extract"
python3 "$SCRIPTS/crawler.py"

# Step 2: Classifier
echo ""
echo "[2/6] Classifier — tag LOTR kingdom + framework + skill type"
python3 "$SCRIPTS/classify.py"

# Step 3: Dedup
echo ""
echo "[3/6] Dedup — cluster + canonical marking"
python3 "$SCRIPTS/dedup.py"

# Step 4: Build package
echo ""
echo "[4/6] Build package — themed folder structure"
python3 "$SCRIPTS/build_package.py"

# Step 5: Excel index
echo ""
echo "[5/6] Generate Excel index"
python3 "$SCRIPTS/generate_excel.py"

# Step 6: PDF catalog
echo ""
echo "[6/6] Generate PDF master catalog"
python3 "$SCRIPTS/generate_pdf.py"

echo ""
echo "============================================================"
echo "Refresh complete at $(date -Iseconds)"
echo "Package: /home/z/my-project/download/the-lord-of-the-skills/"
echo "Log:     $LOG"
echo "============================================================"

# Optional: prune old logs (keep last 12)
cd "$WORK_ROOT/_cache"
ls -t refresh-*.log 2>/dev/null | tail -n +13 | xargs -r rm -v
