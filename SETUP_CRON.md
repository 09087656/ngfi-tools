# ⏰ NGFI Daily Email Wave - Cron Setup

## Automated Scheduling

### Current Setup
- **Script**: `/home/pc/.openclaw/workspace/NGFI_DAILY_WAVE.sh`
- **Schedule**: Daily at 09:00 GMT+1 (= 08:00 UTC)
- **Trigger**: Automatic via cron
- **Password**: Embedded in script

### To Activate Cron Job

Run this command in terminal:

```bash
(crontab -l 2>/dev/null; echo "0 8 * * * /home/pc/.openclaw/workspace/NGFI_DAILY_WAVE.sh >> /home/pc/.openclaw/workspace/logs/cron.log 2>&1") | crontab -
```

### Verify Installation

```bash
crontab -l | grep NGFI_DAILY_WAVE
```

Expected output:
```
0 8 * * * /home/pc/.openclaw/workspace/NGFI_DAILY_WAVE.sh >> ...
```

### View Logs

```bash
tail -f /home/pc/.openclaw/workspace/logs/email_wave_$(date +%Y-%m-%d).log
tail -f /home/pc/.openclaw/workspace/logs/cron.log
```

### Schedule Details

| Item | Value |
|------|-------|
| **Time** | 09:00 GMT+1 |
| **UTC equivalent** | 08:00 UTC |
| **Frequency** | Every day |
| **Email volume** | 50 emails/day (configurable) |
| **Rate limiting** | 1.5s between each |

### Manual Test

```bash
bash /home/pc/.openclaw/workspace/NGFI_DAILY_WAVE.sh
```

### Files Involved

- **Script**: `NGFI_DAILY_WAVE.sh` (runs the Python email script)
- **Email script**: `NGFI_SMTP_EMAIL.py` (sends emails via Gmail)
- **Database**: `NGFI_LEADS_DATABASE.json` (tracks prospects)
- **Logs**: `logs/email_wave_*.log` (daily logs)
- **Cron logs**: `logs/cron.log` (cron execution logs)

### Troubleshooting

**Cron not running?**
- Check if cron daemon is active: `sudo service cron status`
- Check system logs: `sudo tail -f /var/log/syslog | grep CRON`

**Emails not sending?**
- Check logs: `tail -f logs/email_wave_$(date +%Y-%m-%d).log`
- Verify Gmail password: `echo "jlog vwul dqie qire" | wc -c` (should be 19)
- Test manually: `python3 NGFI_SMTP_EMAIL.py "jlog vwul dqie qire"`

**Database errors?**
- Check JSON validity: `python3 -m json.tool NGFI_LEADS_DATABASE.json`
- Verify file permissions: `ls -la NGFI_LEADS_DATABASE.json`

---

**Status**: ✅ Ready for production
**Next**: Activate cron job for daily automation
