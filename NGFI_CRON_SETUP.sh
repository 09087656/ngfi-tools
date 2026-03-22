#!/bin/bash
# NGFI Automated Outreach - Cron Setup Script
# Run this once to install the daily automation

set -e

WORKSPACE="/home/pc/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs"
SCRIPT="$WORKSPACE/NGFI_AUTO_OUTREACH.py"

# Create logs directory
mkdir -p "$LOG_DIR"

# Create cron job script
cat > "$WORKSPACE/ngfi_daily_outreach.sh" << 'EOF'
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
EOF

chmod +x "$WORKSPACE/ngfi_daily_outreach.sh"

echo "✅ Cron setup script created: $WORKSPACE/ngfi_daily_outreach.sh"
echo ""
echo "Now installing cron job..."
echo ""

# Install cron job (runs daily at 09:00)
# Using UTC+1 (GMT+1) = 08:00 UTC for safety
CRON_ENTRY="0 8 * * * $WORKSPACE/ngfi_daily_outreach.sh"

# Check if already installed
if crontab -l 2>/dev/null | grep -q "NGFI_AUTO_OUTREACH"; then
    echo "ℹ️  Cron job already exists, updating..."
    (crontab -l 2>/dev/null | grep -v NGFI_AUTO_OUTREACH; echo "$CRON_ENTRY # NGFI_AUTO_OUTREACH") | crontab -
else
    echo "📝 Installing new cron job..."
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY # NGFI_AUTO_OUTREACH") | crontab -
fi

echo ""
echo "✅ Cron job installed successfully!"
echo ""
echo "Cron Schedule:"
echo "  → Every day at 09:00 GMT+1 (08:00 UTC)"
echo "  → Executes: $WORKSPACE/ngfi_daily_outreach.sh"
echo "  → Logs to: $WORKSPACE/logs/ngfi_outreach_YYYY-MM-DD.log"
echo ""
echo "Verify with: crontab -l"
