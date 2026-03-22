# HEARTBEAT.md - Tâches Périodiques Autonomes

## 1️⃣ MULTI-CHANNEL OUTREACH - NGFI (PRIMARY TASK)

**Fréquence:** Quotidienne (Sub-agent autonome) — PRODUCTION STARTS MONDAY 24 MARCH
**Type:** Cold email warm-up (3 semaines)
**Manager:** NGFI Cold Email Manager (sub-agent autonome)

### Phase Actuelle:
- **Week 1 (March 24-30):** Soft test 3-5 emails/day → Learn best template
- **Week 2 (March 31-April 6):** Scale 10-15 emails/day → Optimize by sector  
- **Week 3 (April 7-13):** Full velocity 20-25 emails/day → Maximize leads
- **Final:** Analysis + pivot based on engagement

### Actions du Sub-Agent (Daily):
1. Load NGFI_LEADS_DATABASE.json
2. Send personalized emails via idirakriche@getngfi.com (spacing 45min-2hrs apart)
3. Track opens, replies, bounces
4. Log all attempts in database
5. Generate daily standup (13:00 GMT+1) — UPDATED TIME
6. Weekly analysis + adjustments
7. Follow-up sequences (Day 5, Day 10)

### Configuration:
- **Daily limit:** Max 25 emails/day (Gmail safety)
- **Templates:** A (Hook), B (Pain-point), C (Social Proof), D (Teaser)
- **Personalization:** MANDATORY (name, sector, pain points)
- **Warm-up:** Progressive (Week 1: 10-15 → Week 3: 100+)

### Templates utilisés (NGFI):
- Email A: Hook-based ("Combien tu passes d'admin chaque semaine?")
- Email B: Pain-point ("87% des freelancers frustré par l'admin")
- Email C: Social proof ("Freelancers utilisant automation gagnent 30% plus")
- Email D: Teaser ("Ça change 100% la façon de faire")

### Statuts de notification:
- 🔴 **Demo booked** → NOTIFIER IMMÉDIATEMENT (priorité CRITIQUE)
- 🟠 **Réponse positive** → NOTIFIER IMMÉDIATEMENT (priorité haute)
- 🟡 **Daily standup** → Report 13:00 GMT+1 (routine)
- ⚠️ **Issues** → Bounce >5%, Response <3% → Action taken
- 🟢 **No activity** → HEARTBEAT_OK (silent/routine)

### Notes:
- Sub-agent est AUTONOME (décisions propres)
- Tracking complet via NGFI_LEADS_DATABASE.json
- Daily standups à NGFI_DAILY_STANDUP.md
- User n'intervient que si demo/issue critique

---

## 1b️⃣ MICRO-TOOLS FACTORY (LINKEDIN LEAD MAGNET)

**Fréquence:** Quotidienne (Sub-agent autonome) — PRODUCTION STARTS MONDAY 24 MARCH
**Type:** LinkedIn lead magnet (free tools to convert on LinkedIn)
**Manager:** NGFI Tools Factory (sub-agent autonome)

### Phase Actuelle:
- **Queue:** 10 micro-tools (Monday 24 - Tuesday 2 April — 10 consecutive days)
- **Daily at 09:00 AM:** Generate tool + push GitHub → Vercel auto-deploys
- **Daily at 13:00 PM:** Deploy verification + LinkedIn post ready + X post ready + daily standup
- **Strategy:** Post free tool on LinkedIn → Users try tool → Convert to NGFI

### Actions du Sub-Agent (Daily):
1. Load NGFI_TOOLS_QUEUE.json
2. Generate HTML/CSS/JS (single file, mobile-first, fully functional)
3. Push GitHub → `/tools/[nom-outil]/index.html`
4. Verify Vercel deployment live
5. Generate LinkedIn post (hook → problem → solution → "Essaie l'outil" + link)
6. Generate X/Twitter post (short version)
7. Send daily standup at 13:00 GMT+1 (with LinkedIn post ready to copy/paste)

### Configuration:
- **Deploy:** Vercel auto on push
- **Domain:** tools.ngfi.fr
- **LinkedIn:** Post 1x/jour (morning or afternoon — user posts)
- **CTA:** "Essaie NGFI gratuitement" (in tool footer + LinkedIn post)

### Outils à produire (ordre):
1. Vérificateur conformité facture
2. Simulateur charges sociales
3. Calculateur TJM
4. Calculateur TVA
5. Estimateur retraite freelance
6. Calculateur rentabilité client
7. Simulateur pénalités de retard
8. Calculateur taux horaire réel
9. Comparateur portage vs AE
10. Simulateur impact congés sur CA

### Statuts de notification:
- 🟢 **Tool deployed + posts generated** → Daily standup 13:00 GMT+1 (routine)
- 🔴 **Deploy failed** → ALERT IMMÉDIAT (critical)
- 🟡 **Vercel error** → Rollback + redeploy (auto-handled)

### Notes:
- Sub-agent AUTONOME (decisions + error handling propres)
- **PRODUCTION START:** Monday 24 March, 09:00 AM
- **Tool #1:** Vérificateur Conformité Facture (already tested ✅)
- **Tools #2-10:** Queue ready in NGFI_TOOLS_QUEUE.json
- **Posts:** LinkedIn + X (100% copier/coller ready)
- **Deploy:** GitHub push → Vercel auto-deploy (no manual intervention)
- **Leads capture:** Optional (webhook if configured)

---

## 2️⃣ NEW PROSPECT DISCOVERY (SECONDARY TASK)

**Fréquence:** 2-3 fois par semaine (lundi/mercredi/vendredi)
**Type:** Recherche web + extraction de nouveaux prospects

### Actions à effectuer:
1. Lancer 5-10 recherches web sur ICP NGFI (différents secteurs)
2. Extraire infos de contact (email, phone, website)
3. Pré-qualifier selon critères (1+ an XP, >2000€/mois, frustrated avec admin)
4. Ajouter à NGFI_LEADS_DATABASE.json
5. Notifier utilisateur des prospects trouvés

### Paramètres:
- **Volume cible:** 30-50 nouveaux prospects par cycle
- **Secteurs à alterner:** Dev, Design, Marketing, Rédaction, Traduction, etc.
- **Géographie:** France (focus régions tech-friendly)

### Statuts de notification:
- ✅ **30+ prospects trouvés** → Notifier avec résumé
- ❌ **<10 prospects trouvés** → HEARTBEAT_OK (reessayer plus tard)

---

## 3️⃣ RESPONSE MONITORING (CONTINUOUS)

**Fréquence:** Temps réel (checker à chaque heartbeat)
**Type:** Monitor inbound responses/feedback

### Actions à effectuer:
1. Checker les réponses aux emails/LinkedIn/WhatsApp
2. Parser les réponses positives vs négatives
3. Mettre à jour statut prospect ("responded", "qualified_for_call", etc)
4. NOTIFIER IMMÉDIATEMENT utilisateur si réponse positive

### Signaux positifs à détecter:
- "Oui, montre-moi"
- "Intéressé"
- Réponse avec questions sur NGFI
- Calendrier booking créé
- Demande de démo

---

## Priorités d'Alerte

| Priorité | Action | Notification |
|----------|--------|--------------|
| 🔴 CRITIQUE | Booking/Demo créé | IMMÉDIAT + details |
| 🟠 HAUTE | Réponse positive | IMMÉDIAT + réponse quote |
| 🟡 MOYENNE | Bulk outreach complété (100 emails) | Silent/HEARTBEAT_OK |
| 🟢 BASSE | Aucune réponse | Silent/HEARTBEAT_OK |

---

## Files de Référence

- **NGFI_LEADS_DATABASE.json** - Source de vérité pour tous les prospects
- **OUTREACH_SCHEDULER.md** - Documentation de la stratégie
- **Templates** - Embeddés dans OUTREACH_SCHEDULER.md

---

## Exemple Heartbeat OK Flow

```
09:00 → Heartbeat trigger
  ✅ Charger 100 prospects "not_contacted"
  ✅ Générer 100 emails perso
  ✅ Marquer status = "email_sent"
  ✅ Logger tentatives
  ❌ Aucune réponse = HEARTBEAT_OK (silencieux)

À 14:00 → Une réponse arrive
  🔴 ALERT IMMÉDIAT! Prospect a répondu oui
  📧 Forward réponse à utilisateur
  🎯 Marquer "qualified_for_call"
```
