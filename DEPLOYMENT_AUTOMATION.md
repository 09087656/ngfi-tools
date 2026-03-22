# 🚀 DEPLOYMENT AUTOMATION - Production Ready

**Objectif:** Zéro problème de deploy à partir de lundi.

---

## ✅ CI/CD Pipeline Checklist (Automatisé)

### AVANT CHAQUE DEPLOY:

1. **Test Local**
   ```bash
   python3 -m http.server 8000
   # Visit http://localhost:8000 → Vérificateur charge?
   ```

2. **Vérifier Structure**
   ```bash
   ls -la public/
   # Doit avoir: index.html (main) + /tools/* (future)
   ```

3. **Git Check**
   ```bash
   git status
   git add -A
   git commit -m "Outil #X: [nom]"
   git push
   ```

4. **Vercel Deploy**
   - Auto-trigger on push ✅
   - Status: Check Vercel dashboard

5. **Verify Live**
   ```bash
   curl https://ngfi-tools.vercel.app/
   # Should return HTML, not 404
   ```

---

## 📋 Structure Production (FINAL)

```
ngfi-tools/
├── public/                    ← Vercel serves this
│   ├── index.html            ← Outil #1 (verificateur-facture)
│   ├── tool-2.html           ← Outil #2 (simulateur-charges)
│   ├── tool-3.html           ← Outil #3 (calculateur-tjm)
│   └── README.md
├── tools/                     ← Source (for reference)
│   ├── verificateur-facture/index.html
│   ├── simulateur-charges/index.html
│   └── ...
├── vercel.json               ← Config
├── README.md
└── .gitignore
```

**Deploy URL:**
- Outil #1: `https://ngfi-tools.vercel.app/`
- Outil #2: `https://ngfi-tools.vercel.app/tool-2.html`
- Custom domain: `tools.ngfi.fr` (après setup DNS)

---

## 🤖 Sub-Agent Daily Checklist (AUTOMATED)

**Chaque jour à 09:00 AM — Task 1b (Tools Factory):**

```
✅ Step 1: Load NGFI_TOOLS_QUEUE.json
   - Get outil #N du jour
   - Extract: name, emoji, description

✅ Step 2: Generate Code
   - Create HTML: public/tool-N.html
   - Include: emoji, description, CTA NGFI
   - Test in browser locally

✅ Step 3: Git Workflow
   - cd /home/pc/.openclaw/workspace
   - git add public/tool-N.html
   - git commit -m "Tool #N: [name]"
   - git push

✅ Step 4: Verify Deploy
   - Wait 30-60s for Vercel
   - curl https://ngfi-tools.vercel.app/tool-N.html
   - If 200 OK → Continue
   - If 404 → Retry push + wait

✅ Step 5: Generate Posts
   - LinkedIn post (prêt copier/coller)
   - X post (courte version)

✅ Step 6: Daily Standup (13:00 GMT+1)
   - Report: ✅ Deployed
   - URL live: [confirm]
   - Posts ready: [confirm]
```

---

## 🛡️ Error Prevention (Lundi+ STRICT)

### ❌ NEVER DO:
- ❌ Vercel API calls (use dashboard only)
- ❌ Subdirectories in public/ (flat structure)
- ❌ Vercel config with custom domains (set in UI)
- ❌ Multiple deployments per tool (one per day)

### ✅ ALWAYS DO:
- ✅ Test locally first (http.server)
- ✅ Flat file structure (public/tool-N.html)
- ✅ Simple vercel.json (outputDirectory only)
- ✅ Check curl output (200 OK)

---

## 📊 Deploy Workflow (Automated Monday+)

```
09:00 AM
  ↓
Sub-agent generates tool (HTML)
  ↓
Git: add + commit + push
  ↓
Vercel auto-builds (30-60s)
  ↓
Verify: curl check
  ↓
13:00 PM: Daily standup
  ├─ ✅ URL: https://ngfi-tools.vercel.app/tool-N.html
  ├─ ✅ Posts: Ready
  └─ ✅ Status: Live
```

---

## 🔧 Tools for Automation

### Test Script (run before push):

```bash
#!/bin/bash
# verify-deploy.sh

echo "📋 Checking structure..."
if [ ! -f "public/index.html" ]; then
  echo "❌ public/index.html missing"
  exit 1
fi

echo "🌐 Testing locally..."
python3 -m http.server 8000 &
SERVER_PID=$!
sleep 2

RESPONSE=$(curl -s http://localhost:8000/)
if echo "$RESPONSE" | grep -q "<!DOCTYPE html>"; then
  echo "✅ Local test OK"
else
  echo "❌ Local test failed"
  kill $SERVER_PID
  exit 1
fi

kill $SERVER_PID
echo "✅ Ready to push"
```

### Deploy Check (after push):

```bash
#!/bin/bash
# check-vercel.sh

echo "⏳ Waiting for Vercel deploy..."
sleep 60

RESPONSE=$(curl -s https://ngfi-tools.vercel.app/)
if echo "$RESPONSE" | grep -q "<!DOCTYPE html>"; then
  echo "✅ Vercel live!"
else
  echo "❌ Vercel deploy failed"
  exit 1
fi
```

---

## 🎯 SLA - Production Guarantee

**For each tool (daily):**
- ✅ Code generated: 09:00 AM
- ✅ Deployed live: 10:00 AM (max 60 min)
- ✅ Posts ready: 13:00 PM standup
- ✅ URL responsive: Mobile + desktop

**Downtime tolerance:** 0 (if error, rollback + report)

---

## 📝 Next Steps

1. **Monday 24 mars, 09:00 AM:**
   - Sub-agent uses this checklist
   - Generates Outil #1 ✅
   - Deploys to Vercel ✅
   - Posts LinkedIn ✅

2. **Daily 09:00 AM (Tuesday - Tuesday 2 April):**
   - Repeat workflow
   - 10 tools in 10 days ✅

3. **If error:**
   - Sub-agent reports immediately
   - Idir fixes + redeploy
   - NO silent failures

---

**Status: PRODUCTION READY FOR MONDAY 🚀**

