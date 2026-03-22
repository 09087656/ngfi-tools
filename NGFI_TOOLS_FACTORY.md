# 🏭 USINE MICRO-OUTILS NGFI

## Mission
Générer et déployer **1 micro-outil gratuit/jour** pour auto-entrepreneurs français.
Objectif: LinkedIn lead magnet → Convert directement vers NGFI Pro

---

## 📋 Architecture Technique

### Repo & Deploy
- **GitHub:** NGFI repo (dossier `/tools/`)
- **Deploy:** Vercel auto (push → live)
- **Domain:** `tools.ngfi.fr`
- **CDN:** Unpkg, CDN.js (pas de dépendances locales)

### Structure Par Outil
```
/tools/
  ├── vérificateur-facture/
  │   ├── index.html (single file)
  │   ├── README.md
  │   └── preview.png
  ├── simulateur-charges/
  │   └── index.html
  └── ...
```

---

## 🎯 Composants Chaque Outil

### 1️⃣ **HTML/CSS/JS (Single File)**
- Minimaliste, mobile-first
- Logo NGFI + lien ngfi.fr (footer)
- **Fully functional tool** (no gatekeeping)
- Responsive (mobile 320px+)
- Pas de frameworks externes (vanilla JS ok, Tailwind CDN ok)

### 2️⃣ **CTA NGFI (Footer)**
```html
<div class="ngfi-cta">
  <p>🚀 <strong>NGFI</strong> fait ça automatiquement pour toi</p>
  <a href="https://ngfi.fr/demo" class="btn-ngfi">Essaie gratuitement</a>
</div>
```

### 3️⃣ **Post LinkedIn**
Format: Hook → Problème → Solution → CTA
```
🎯 [HOOK - 1ère ligne percutante]

[PROBLÈME - contexte]
[SOLUTION - outil gratuit]

➡️ Essaie ici: [LIEN tools.ngfi.fr/outil]

#AutoEntrepreneur #Freelance #Gestion
```
**Format:** Prêt à copier/coller — utilisateur poste sur LinkedIn lui-même

### 4️⃣ **Post X (Twitter/X)**
Version courte (280 chars max)
```
[Hook] — Calcule [résultat] en 30s gratuitement
→ [LIEN]

#AE #Freelance #Productivité
```

---

## 📅 Liste des Outils (Ordre Production)

| # | Outil | Focus | Calcul Principal |
|---|-------|-------|------------------|
| 1 | Vérificateur conformité facture | Légal | Checklist 15 critères |
| 2 | Simulateur charges sociales | Charges | Cotisations auto-entrepreneur |
| 3 | Calculateur TJM | Tarif | Coût horaire → TJM optimal |
| 4 | Calculateur TVA | Impôts | TVA intracommunautaire |
| 5 | Estimateur retraite freelance | Retraite | Points retraite estimés |
| 6 | Calculateur rentabilité client | Business | ROI par client |
| 7 | Simulateur pénalités de retard | Légal | Calcul pénalités factures |
| 8 | Calculateur taux horaire réel | Tarif | TJM réel (frais + marge) |
| 9 | Comparateur portage vs AE | Structures | Gains net (portage vs AE) |
| 10 | Simulateur impact congés | CA | Impact vacances sur CA annuel |

---

## 🔄 Flow Quotidien

### 09:00 AM — Agent Autonome Lance
1. **Charger outil du jour** dans NGFI_TOOLS_QUEUE.json
2. **Générer code complet**
   - HTML template de base
   - Logique de calcul perso
   - Email capture + CTA NGFI
3. **Push GitHub** → `/tools/[nom-outil]/index.html`
4. **Vérifier Vercel deploy** (live check)
5. **Générer posts**
   - LinkedIn (hook + lien)
   - X (version courte)
6. **Envoyer rapport** → Telegram (avec lien + posts)

### À Midi — Utilisateur Action
- Copie/colle post LinkedIn
- Copie/colle post X
- Monitor engagement

### 13:00 GMT+1 — Daily Standup
- Outil déployé? ✅
- Vercel live? ✅
- Posts générés? ✅
- Leads captées? [X emails]

---

## 📊 Tracking Leads

### Option 1: Google Sheets
- Onglet: `leads-outils`
- Colonnes: `Date | Outil | Email | Source | Timestamp`
- Webhook: form → sheet via Zapier ou script Google Apps

### Option 2: Snov.io
- Webhook endpoint vers Snov.io
- Auto-sync vers CRM

**Configuration:** À définir avec utilisateur

---

## ✅ Règles Production

- ✅ **Un seul fichier HTML** (index.html dans le dossier outil)
- ✅ **CDN-only deps** (Tailwind, Chart.js, etc.)
- ✅ **Mobile-first** (responsive 320px+)
- ✅ **Logo NGFI + lien ngfi.fr** (footer obligatoire)
- ✅ **Outil GRATUIT et SANS gatekeeping** (accessible immédiatement)
- ✅ **CTA NGFI visible** ("Essaie NGFI gratuitement" en footer)
- ✅ **Tester calculs avant push** (validation manuelle)
- ✅ **Posts LinkedIn + X générés** (prêts à copier/coller)

---

## 🎬 Files de Référence

- **NGFI_TOOLS_QUEUE.json** — Queue des outils à produire
- **NGFI_TOOLS_FACTORY_STANDUP.md** — Daily reports
- **GitHub NGFI repo** — Source de vérité

---

## 📝 Template Outil (Base)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[NOM OUTIL]</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; }
    </style>
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-lg max-w-md w-full p-8">
        <!-- Header -->
        <div class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">[EMOJI] [TITRE]</h1>
            <p class="text-gray-600">[Description courte]</p>
        </div>

        <!-- Email Capture Form (Before Tool) -->
        <form id="emailForm" class="mb-8">
            <input type="email" id="userEmail" placeholder="ton@email.com" class="w-full px-4 py-2 border border-gray-300 rounded-lg mb-3" required>
            <button type="submit" class="w-full bg-indigo-600 text-white py-2 rounded-lg font-semibold hover:bg-indigo-700">
                Accéder à l'outil
            </button>
        </form>

        <!-- Tool Content (Hidden until email) -->
        <div id="toolContent" class="hidden">
            <!-- [Logique spécifique de l'outil] -->
            <div class="space-y-4">
                [INPUTS DE CALCUL]
                [RÉSULTAT]
            </div>
        </div>

        <!-- Footer NGFI CTA -->
        <div class="mt-8 pt-6 border-t border-gray-200 text-center">
            <p class="text-sm text-gray-600 mb-3">
                <strong>NGFI</strong> fait ça automatiquement pour toi
            </p>
            <a href="https://ngfi.fr/demo" class="inline-block bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-2 rounded-lg font-semibold hover:shadow-lg">
                Essaie gratuitement
            </a>
        </div>

        <!-- Logo NGFI -->
        <div class="mt-6 text-center">
            <a href="https://ngfi.fr" class="text-xs text-gray-500 hover:text-gray-700">
                Powered by NGFI
            </a>
        </div>
    </div>

    <script>
        // Email capture
        document.getElementById('emailForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('userEmail').value;
            
            // POST to Google Sheets or Snov.io
            await fetch('[WEBHOOK_URL]', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: email,
                    tool: '[NOM_OUTIL]',
                    timestamp: new Date().toISOString()
                })
            });

            // Show tool
            document.getElementById('emailForm').classList.add('hidden');
            document.getElementById('toolContent').classList.remove('hidden');
        });

        // Tool-specific logic here
    </script>
</body>
</html>
```

---

## 🚀 Status

- ⏳ **Queue:** À créer (NGFI_TOOLS_QUEUE.json)
- ⏳ **Sub-agent:** À spawner
- ⏳ **Première journée:** Lundi 24 mars (Vérificateur facture)

**Go? 🚀**
