#!/bin/bash
# NGFI Daily Email Wave - Automated at 09:00 GMT+1

set -e

WORKSPACE="/home/pc/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/email_wave_$(date +%Y-%m-%d).log"
LEADS_DB="$WORKSPACE/NGFI_LEADS_DATABASE.json"
SCRIPT="$WORKSPACE/NGFI_SMTP_EMAIL.py"
APP_PASSWORD="jlog vwul dqie qire"

# Create logs directory if needed
mkdir -p "$WORKSPACE/logs"

{
  echo "================================================"
  echo "🚀 NGFI DAILY EMAIL WAVE"
  echo "📅 $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "================================================"
  
  # Check if database exists
  if [ ! -f "$LEADS_DB" ]; then
    echo "❌ ERROR: Database not found at $LEADS_DB"
    exit 1
  fi
  
  # Check if script exists
  if [ ! -f "$SCRIPT" ]; then
    echo "❌ ERROR: Script not found at $SCRIPT"
    exit 1
  fi
  
  echo "✅ Database: OK"
  echo "✅ Script: OK"
  echo ""
  
  # Run email wave
  echo "📧 Starting email campaign..."
  python3 "$SCRIPT" "$APP_PASSWORD" 2>&1
  
  # Capture exit code
  EXIT_CODE=$?
  
  echo ""
  if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Email wave completed successfully"
    echo "📊 Check $LEADS_DB for updated status"
  else
    echo "❌ Email wave failed with exit code $EXIT_CODE"
  fi
  
  echo ""
  echo "================================================"
  echo "End time: $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "================================================"
  
} | tee -a "$LOG_FILE"

exit $EXIT_CODE
