#!/usr/bin/env python3
"""
Send the 5 March 22 follow-up emails via Gmail SMTP
"""

import json
import time
import logging
import smtplib
from datetime import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/pc/.openclaw/workspace/NGFI_SEND_MARCH22_GMAIL.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Gmail credentials
GMAIL_USER = "idirakriche@gmail.com"
GMAIL_APP_PASSWORD = "ygkmdqqfgpvgrmac"  # App password (no spaces)

# The 5 emails from March 22 manifest
EMAILS_TO_SEND = [
    {
        "name": "Florent Parcevaux",
        "email": "florent@malt.fr",
        "subject": "Salut Florent - Retour sur NGFI (2ème contact)",
        "body": """Salut Florent,

Je reviens vers toi - je ne suis pas certain que mon premier message t'ai parlé.

Toi qui bosses sur des projets WordPress / WooCommerce, tu dois probablement passer pas mal de temps sur l'administrative - client follow-up, devis, invoicing, etc.

Chez NGFI, on a développé une solution d'automation qui permet aux freelancers comme toi de récupérer ~10h par semaine sur ces tâches. Ça libère du temps pour faire plus de deals ou simplement avoir une meilleure work-life balance.

On peut vraiment en parler 20min cette semaine ? Pas de commitment, juste une conversation.

Merci Florent,
Idir
NGFI
https://ngfi.fr"""
    },
    {
        "name": "Jérémy Mouzin",
        "email": "jeremy@mouzin-dev.fr",
        "subject": "Jérémy - Quick follow-up sur javascript developer",
        "body": """Hey Jérémy,

Dernier message sur NGFI, je te promets :)

Si tu penses toujours qu'avoir 10h de plus par semaine pour focus sur les vrais projets (au lieu de l'admin) serait utile, on devrait en parler.

J'aide des JavaScript developers exactement comme toi à automatiser le boring stuff. Un appel de 30min suffit pour voir si c'est un fit.

T'es dispo cette semaine pour 30min ?

À plus,
Idir
NGFI
https://ngfi.fr"""
    },
    {
        "name": "Guillaume Schott",
        "email": "guillaume@schott-design.fr",
        "subject": "Salut Guillaume - Retour sur NGFI (2ème contact)",
        "body": """Salut Guillaume,

Je reviens vers toi - je ne suis pas certain que mon premier message t'ai parlé.

En tant que UX/UI designer freelance, je sais que tu passes pas mal de temps sur les tasks admin: briefs, revisions, invoices, client communication, etc.

NGFI c'est une solution qui automatise tout ça. On voit régulièrement des designers gagner 10h/semaine + 3x plus de deals grâce à cette automation.

On peut vraiment en parler 20min cette semaine ? Pas de commitment, juste une conversation.

Merci Guillaume,
Idir
NGFI
https://ngfi.fr"""
    },
    {
        "name": "Sophie Leclerc",
        "email": "sophie@leclerc-marketing.fr",
        "subject": "Sophie - NGFI peut libérer 15h/semaine pour toi",
        "body": """Salut Sophie,

Je reviens vers toi - j'aimerais vraiment qu'on en parle.

En tant que marketing freelancer, je sais que tu passes énormément de temps sur: rapports clients, factures, suivi administratif, scheduling, relances...

NGFI automatise TOUT ça. Les marketers qu'on aide gagnent régulièrement 15h/semaine et peuvent se focus sur la stratégie et les vraies deliverables.

On peut vraiment en parler 20min cette semaine ? Pas de commitment, juste une conversation.

Merci Sophie,
Idir
NGFI
https://ngfi.fr"""
    },
    {
        "name": "Thomas Bernard",
        "email": "thomas@bernard-consulting.fr",
        "subject": "Thomas - Automation pour consultants",
        "body": """Salut Thomas,

Je reviens vers toi - j'aimerais vraiment qu'on en parle.

En tant que consultant indépendant, tu sais mieux que quiconque que l'admin absorbe une énorme partie de ton temps: devis, factures, relances, suivi de projets, etc.

NGFI c'est fait pour ça - automatiser 100% de cette partie. Les consultants qu'on aide gagnent en moyenne 12h/semaine et peuvent se focus sur ce qu'ils font vraiment bien.

On peut vraiment en parler 20min cette semaine ? Pas de commitment, juste une conversation.

Merci Thomas,
Idir
NGFI
https://ngfi.fr"""
    }
]

def send_email(name, email, subject, body):
    """Send email via Gmail SMTP"""
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD.replace(" ", ""))
        
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server.send_message(msg)
        server.quit()
        
        logger.info(f"✅ Email sent to {name} ({email})")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send to {email}: {str(e)}")
        return False

def main():
    logger.info("=" * 70)
    logger.info("🚀 NGFI March 22 Follow-up Campaign - Gmail SMTP")
    logger.info(f"Start Time: {datetime.now()}")
    logger.info(f"Total Emails: {len(EMAILS_TO_SEND)}")
    logger.info("=" * 70)
    
    sent_count = 0
    
    for i, email_data in enumerate(EMAILS_TO_SEND, 1):
        logger.info(f"\n📧 Email {i}/{len(EMAILS_TO_SEND)}: {email_data['name']}")
        logger.info(f"   To: {email_data['email']}")
        logger.info(f"   Subject: {email_data['subject']}")
        
        if send_email(email_data['name'], email_data['email'], email_data['subject'], email_data['body']):
            sent_count += 1
            
            # Wait 45 minutes between emails (2700 seconds)
            if i < len(EMAILS_TO_SEND):
                logger.info(f"   ⏳ Waiting 45 minutes before next email...")
                time.sleep(2700)
        
        time.sleep(1)
    
    logger.info("\n" + "=" * 70)
    logger.info(f"✅ Campaign Complete: {sent_count}/{len(EMAILS_TO_SEND)} emails sent")
    logger.info(f"End Time: {datetime.now()}")
    logger.info("=" * 70)

if __name__ == "__main__":
    main()
