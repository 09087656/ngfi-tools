#!/bin/bash
# Daily NGFI Outreach Execution
# Runs at 09:00 GMT+1 every day

WORKSPACE="/home/pc/.openclaw/workspace"
PYTHON_SCRIPT="$WORKSPACE/NGFI_AUTO_OUTREACH.py"
LOG_FILE="$WORKSPACE/logs/ngfi_outreach_$(date +%Y-%m-%d).log"

# Execute Python script
python3 "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1

# Generate timestamp
echo "✅ Execution completed at $(date)" >> "$LOG_FILE"
