#!/bin/bash
# Daily AI news update wrapper
# Usage: GITHUB_TOKEN=xxx ./run_daily.sh

# Token must be provided via environment variable
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN not set"
    exit 1
fi

export GITHUB_USER="DSeaStar"
export REPO_NAME="ai-timeline"

cd /root/.openclaw/workspace/ai-timeline

# Log file
LOG_FILE="/tmp/ai-timeline-daily.log"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"
python3 scripts/daily_update.py >> "$LOG_FILE" 2>&1
echo "" >> "$LOG_FILE"
