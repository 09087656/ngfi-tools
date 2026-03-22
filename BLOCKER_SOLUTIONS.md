# 🔧 BLOCKERS SOLUTIONS - Samedi 23 Mars

## BLOCKER #1: Google Sheets Webhook Configuration

### Setup Google Sheets (5 min)

**Step 1: Create Google Sheet**
1. Go: https://sheets.google.com
2. Create new spreadsheet: `ngfi-tools-leads`
3. Create sheet tab: `leads-outils`
4. Columns: `Date | Outil | Email | Timestamp | Source`

**Step 2: Enable Apps Script**
1. Tools → Script Editor
2. Paste code:

```javascript
function doPost(e) {
  const sheet = SpreadsheetApp.getActiveSheet();
  const data = JSON.parse(e.postData.contents);
  
  sheet.appendRow([
    new Date().toLocaleString(),
    data.tool || 'Unknown',
    data.email || '',
    new Date().toISOString(),
    'Tools Factory'
  ]);
  
  return ContentService.createTextOutput('OK');
}
```

3. Deploy → New deployment → Web app
4. Execute as: Your account
5. Who has access: Anyone (copy URL)

**Step 3: Copy Webhook URL**
- Format: `https://script.google.com/macros/d/[DEPLOYMENT_ID]/userweb`
- This is your: `WEBHOOK_URL`

---

## BLOCKER #2: GitHub Path Confirmation

### Confirmed Structure:
```
ngfi-tools repo
├── tools/
│   ├── verificateur-facture/
│   │   ├── index.html (the tool)
│   │   ├── README.md
│   │   └── preview.png
│   ├── simulateur-charges/
│   │   └── index.html
│   └── ...
├── README.md (root)
└── vercel.json (optional)
```

**Deploy URL:** `https://tools.ngfi.fr/tools/verificateur-facture/`

---

## BLOCKER #3: Vercel Auto-Deploy

### Setup Vercel (2 min)

1. Go: https://vercel.com
2. Import project: `ngfi-tools` (from GitHub)
3. Set domain: `tools.ngfi.fr`
4. Auto-deploy: On (default)

**Test live URL:**
```bash
curl https://tools.ngfi.fr/tools/verificateur-facture/
# Should return HTML
```

---

## BLOCKER #4: Webhook Code in HTML

### Add to invoice-checker.html (before `</head>`):

```javascript
const WEBHOOK_URL = 'https://script.google.com/macros/d/[YOUR_DEPLOYMENT_ID]/userweb';

// Function to send email to webhook
async function captureEmail(email, toolName) {
  try {
    await fetch(WEBHOOK_URL, {
      method: 'POST',
      mode: 'no-cors',
      body: JSON.stringify({
        email: email,
        tool: toolName,
        timestamp: new Date().toISOString()
      })
    });
    console.log('Email captured:', email);
  } catch (error) {
    console.error('Webhook error:', error);
  }
}

// Call this when tool loads or on action
window.addEventListener('load', () => {
  // Optional: capture anonymous usage
  // captureEmail('anonymous@ngfi.fr', 'verificateur-facture');
});
```

### Usage in HTML:
```html
<!-- Optional: Add email capture form (non-blocking) -->
<div class="email-opt-in" style="margin-top: 20px; padding: 15px; background: #f0f7ff; border-radius: 8px;">
  <p style="font-size: 12px; color: #666; margin-bottom: 10px;">
    Veux-tu des outils bonus? Laisse ton email (optionnel)
  </p>
  <div style="display: flex; gap: 10px;">
    <input type="email" id="emailOptIn" placeholder="ton@email.com" style="flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
    <button onclick="captureEmailOptIn()" style="padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer;">OK</button>
  </div>
</div>

<script>
function captureEmailOptIn() {
  const email = document.getElementById('emailOptIn').value;
  if (email) {
    captureEmail(email, 'verificateur-facture');
    document.getElementById('emailOptIn').value = '';
    alert('✅ Email reçu!');
  }
}
</script>
```

---

## SAMEDI ROADMAP (23 Mars)

### 09:00 AM - Setup Phase (30 min)
- [ ] Create Google Sheet
- [ ] Deploy Apps Script
- [ ] Copy webhook URL
- [ ] Add to HTML code
- [ ] Git commit + push

### 10:00 AM - Vercel Setup (15 min)
- [ ] Connect GitHub to Vercel
- [ ] Set domain: tools.ngfi.fr
- [ ] Verify deploy live

### 10:15 AM - Testing Phase (30 min)
- [ ] Test tool on desktop (Chrome)
- [ ] Test on mobile (iPhone simulator)
- [ ] Test email capture (Google Sheet)
- [ ] Verify Vercel URL

### 11:00 AM - Final Checks
- [ ] All 4 blockers resolved ✅
- [ ] Readiness score: 100/100
- [ ] GO for Monday

---

## SUNDAY (24 Mars) - LAUNCH DAY

### 09:00 AM - Sub-Agent Generates Next Tool
- Load queue
- Generate code
- Push GitHub
- Vercel auto-deploys
- Posts generated

### 13:00 PM - Daily Standup
- ✅ Tool deployed
- ✅ URL live
- ✅ Posts ready

**Status: READY FOR PRODUCTION** 🚀

---

## Files to Update Samedi

1. `/home/pc/.openclaw/workspace/invoice-checker.html`
   - Add webhook code
   - Verify email capture works

2. GitHub `/tools/verificateur-facture/index.html`
   - Same as above + committed

3. `/home/pc/.openclaw/workspace/HEARTBEAT.md`
   - Update webhook URL config
   - Confirm Vercel domain

---

## Checklist Samedi

- [ ] Google Sheets: Created + webhook URL copied
- [ ] invoice-checker.html: Webhook code added
- [ ] GitHub: Code committed + pushed
- [ ] Vercel: Domain configured + live
- [ ] Testing: All 3 tests pass (desktop, mobile, email)
- [ ] Status: 100/100 readiness ✅

**IF ALL ✅ → GO FOR MONDAY 09:00 AM LAUNCH**

