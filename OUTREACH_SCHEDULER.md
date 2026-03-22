# OUTREACH SCHEDULER - Automated Multi-Channel Lead Generation

## System Architecture

```
Daily Heartbeat → Lead Selection → Multi-Channel Outreach → Status Tracking → Notification
```

---

## Outreach Strategy

### Phase 1: Email Outreach (Primary - Most Effective)
- **Daily Limit:** 100 emails
- **Content:** Personalized + NGFI value prop
- **Timing:** Mon-Fri 9:00-10:00 AM
- **Tracking:** Open rates + Responses

### Phase 2: LinkedIn Outreach (Secondary)
- **Daily Limit:** 50 connection requests + messages
- **Content:** Connection request + personalized note
- **Timing:** Staggered (avoid detection)
- **Tracking:** Profile views + Message responses

### Phase 3: WhatsApp Outreach (Tertiary)
- **Daily Limit:** 30 messages
- **Content:** Short, casual, value-first
- **Timing:** Business hours
- **Tracking:** Read receipts + Responses

---

## Contact Cycle (Respecting Limits)

### Day 1-3: Email Wave 1
- Send to Top 100 qualified prospects
- Personalized subject lines
- NGFI value prop clear

### Day 4-7: LinkedIn Wave 1
- Connection requests with personalized notes
- 50 per day max
- Focus on non-responders from email

### Day 8-10: Follow-up Email Wave
- To non-responders from Wave 1
- Different angle/value prop
- "Quick question" format

### Day 11-14: WhatsApp Wave 1
- To prospects with phone numbers available
- Short, friendly, benefit-focused
- 30 per day max

### Ongoing: Refresh Cycle
- Every prospect gets 3-touch sequence
- 5-7 days between touches
- Different channels each time
- Respect "unresponsive" status after 3 touches

---

## Message Templates

### Email Template 1
```
Subject: Gagne 10h/semaine [Prénom] - NGFI

Salut [Prénom],

J'ai vu ton excellent travail sur [site/projet spécifique].

Les freelances perdent 30-40% de leur temps sur l'admin et la prospection.
NGFI automatise tout ça → 10h+ gagnées/semaine.

À 49€/mois, ça s'autofinance avec juste 2-3 clients en plus.

Ça t'intéresse ? Je peux te montrer en 15min.

[Lien démo / calendly]

À bientôt,
Idir
```

### LinkedIn Message Template
```
Salut [Prénom],

J'ai kiffer ton portfolio (notamment [projet spécifique]).

Je lance NGFI - un IA business pour freelances qui automatise prosp + admin.
Ça t'intéresse ?

On pourrait en parler 15min ?

À+
```

### WhatsApp Template
```
Yo [Prénom] 👋

J'ai vu que tu fais du [secteur]. Top !

Je lance NGFI - automatise la prosp et l'admin pour les freelances.
10h/semaine de gain.

Ça te dit une démo rapide ? (15min max)

Cheers
```

---

## Daily Heartbeat Execution

Every 24h at 09:00 GMT+1:

1. **Select prospects** for outreach (respecting daily limits)
2. **Generate personalized messages** using templates
3. **Track which channel** for each prospect
4. **Log all attempts** in NGFI_LEADS_DATABASE.json
5. **Notify user** of completed outreaches
6. **Alert immediately** if response received

---

## Response Tracking

### Auto-Detection Signals
- Email reply (any response)
- LinkedIn message response
- WhatsApp read + message received
- Calendar booking from demo link

### Prospect Statuses
- `not_contacted` → Initial state
- `email_sent` → Awaiting response
- `linkedin_requested` → Connection pending
- `whatsapp_sent` → Sent via WhatsApp
- `responded` → Got a reply!
- `qualified_for_call` → Ready for sales call
- `unresponsive_after_3` → Archive

---

## Data Storage

All tracking lives in: `NGFI_LEADS_DATABASE.json`

Structure:
```json
{
  "id": 1,
  "name": "Prospect Name",
  "contact_attempts": [
    {
      "date": "2026-03-14",
      "channel": "email",
      "status": "sent",
      "message_sent": "...",
      "response": null
    }
  ],
  "last_contact_date": "2026-03-14",
  "response_received": false,
  "status": "email_sent"
}
```

---

## Rules to Follow

✅ **DO:**
- Personalize every message (use website info + their work)
- Respect daily limits (100 email, 50 LinkedIn, 30 WhatsApp)
- Space out contacts (3+ days between channels)
- Track everything meticulously
- Alert user ONLY on responses/bookings

❌ **DON'T:**
- Send generic spam messages
- Exceed daily limits (ethical + effective)
- Contact same person more than 3 times
- Use auto-reply bots
- Send during off-hours

---

## Expected Results

**Weekly Targets (Conservative Estimate):**
- Email: 100 sent → 5-10% open rate (5-10 opens)
- LinkedIn: 50 sent → 20-30% acceptance + message response (10-15)
- WhatsApp: 30 sent → 30-50% read + response (10-15)

**Total responses/week:** ~25-40 positive signals

---

## Next Steps

1. Expand NGFI_LEADS_DATABASE.json to full 100+ prospects
2. Enable daily Heartbeat automation
3. Monitor responses in real-time
4. Adjust messaging based on sector/response rates
5. Scale to 200+ prospects by week 2
