# 📊 Google Sheets Webhook Setup - NGFI Invoice Checker

**Objet:** Capturer automatiquement les emails des utilisateurs du vérificateur de facture dans une feuille Google Sheets.

---

## **ÉTAPE 1: Créer un Google Sheet**

1. Ouvre [sheets.google.com](https://sheets.google.com)
2. Clique sur **"+ Nouveau"** → **"Feuille de calcul"**
3. Nomme-la: `NGFI_Invoice_Checker_Leads`
4. Dans la première ligne, ajoute les colonnes:
   - **A1:** `Timestamp`
   - **B1:** `Email`
   - **C1:** `IP_Address`
   - **D1:** `Score`
   - **E1:** `Source`
   - **F1:** `Notes`

**Sauve la feuille.**

---

## **ÉTAPE 2: Créer le Apps Script**

1. Dans ton Google Sheet, va à **Extensions** → **Apps Script**
2. Un nouvel onglet s'ouvre avec l'éditeur
3. **Efface** le code par défaut
4. **Copie-colle** ce code complet:

```javascript
// NGFI Invoice Checker - Email Capture Webhook
// Deployed as Web App (execute as your account)

function doPost(e) {
  try {
    // Parse incoming JSON
    const data = JSON.parse(e.postData.contents);
    
    // Get active spreadsheet
    const sheet = SpreadsheetApp.getActiveSheet();
    
    // Prepare row data
    const timestamp = new Date().toLocaleString('fr-FR', { 
      timeZone: 'Europe/Paris' 
    });
    const email = data.email || '';
    const ipAddress = data.ip || 'N/A';
    const score = data.score || 0;
    const source = data.source || 'invoice-checker.html';
    const notes = data.notes || '';
    
    // Append to sheet
    sheet.appendRow([
      timestamp,
      email,
      ipAddress,
      score,
      source,
      notes
    ]);
    
    // Return success
    return ContentService.createTextOutput(
      JSON.stringify({ 
        success: true, 
        message: 'Email captured successfully',
        timestamp: timestamp 
      })
    ).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    // Return error
    return ContentService.createTextOutput(
      JSON.stringify({ 
        success: false, 
        error: error.toString() 
      })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

// Test function (run locally to check)
function testWebhook() {
  const testData = {
    email: 'test@example.com',
    ip: '192.168.1.1',
    score: 12,
    source: 'invoice-checker.html',
    notes: 'Test entry'
  };
  
  const sheet = SpreadsheetApp.getActiveSheet();
  const timestamp = new Date().toLocaleString('fr-FR', { 
    timeZone: 'Europe/Paris' 
  });
  
  sheet.appendRow([
    timestamp,
    testData.email,
    testData.ip,
    testData.score,
    testData.source,
    testData.notes
  ]);
  
  Logger.log('Test entry added');
}
```

5. **Sauve** le fichier (Ctrl+S / Cmd+S)

---

## **ÉTAPE 3: Déployer en tant que Web App**

1. En haut, clique sur **"Deploy"** (le bouton triangle)
2. Sélectionne **"New deployment"**
3. En haut à gauche, clique sur **"Select type"** → **"Web app"**
4. Configure ainsi:
   - **Execute as:** Ton compte Google (email NGFI)
   - **Who has access:** **"Anyone"** (important pour le webhook)
5. Clique **"Deploy"**
6. Tu verras une URL du style:
   ```
   https://script.google.com/macros/d/YOUR_SCRIPT_ID/useweb
   ```
   **COPIE cette URL — tu en auras besoin.**

7. Un popup demande les permissions → **"Authorize"** → Sélectionne ton compte → **"Allow"**

---

## **ÉTAPE 4: Tester le Webhook**

### Option A: Test direct dans Apps Script

1. Retourne à l'onglet **Editor**
2. En haut, sélectionne **"testWebhook"** dans le dropdown (si tu le vois pas, rafraîchis)
3. Clique **"▶ Run"**
4. Retour au Google Sheet — tu dois voir une ligne test ajoutée avec timestamp

### Option B: Test via cURL (terminal)

```bash
curl -X POST \
  "https://script.google.com/macros/d/YOUR_SCRIPT_ID/useweb" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "idir@ngfi.fr",
    "ip": "192.168.1.1",
    "score": 14,
    "source": "invoice-checker.html",
    "notes": "Test from terminal"
  }'
```

**Remplace `YOUR_SCRIPT_ID`** par ton ID réel de la URL.

---

## **ÉTAPE 5: Intégrer le Webhook dans invoice-checker.html**

La version mise à jour (voir `invoice-checker.html`) contient déjà:

```javascript
// À la fin du script, avant </script>
async function captureEmail(email, currentScore) {
  const webhookUrl = 'REPLACE_WITH_YOUR_WEBHOOK_URL';
  
  try {
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email,
        score: currentScore,
        ip: 'auto-detected',
        source: 'invoice-checker.html',
        notes: `Score final: ${currentScore}/15`
      })
    });
    
    if (response.ok) {
      console.log('✅ Email captured successfully');
      return true;
    }
  } catch (error) {
    console.error('Webhook error:', error);
  }
  return false;
}
```

**À faire:**
1. Remplace `REPLACE_WITH_YOUR_WEBHOOK_URL` par ta URL Apps Script réelle
2. Sauvegarde le fichier

---

## **ÉTAPE 6: Vérification Finale**

### Checklist:

- ✅ Google Sheet créé avec colonnes (`Timestamp`, `Email`, `IP_Address`, `Score`, `Source`, `Notes`)
- ✅ Apps Script déployé en tant que Web App
- ✅ Webhook URL testée (entrée test visible dans le sheet)
- ✅ URL intégrée dans `invoice-checker.html`
- ✅ CORS activé (Apps Script gère ça nativement pour Web App)

---

## **📌 Support & Maintenance**

**Si le webhook échoue:**
1. Vérifie que l'Apps Script est toujours déployé (check dans **"Deploy"** → **"Manage deployments"**)
2. Vérifie les logs: Apps Script → **"Exécutions"** (onglet à gauche) pour voir les erreurs
3. Assure-toi que le Google Sheet est partagé/accessible (permissions)

**Limites:**
- Google Apps Script: ~20 requests/min par utilisateur (largement suffisant pour ce use case)
- Stockage: illimité dans Google Sheets

---

## **🎯 Utilisation**

Dès que quelqu'un remplit le formulaire email dans `invoice-checker.html`, une ligne est ajoutée au sheet avec:
- Timestamp exact
- Email fourni
- Score de conformité final
- Métadonnées (IP, source, notes)

**Prêt à productionner lundi! 🚀**
