#!/usr/bin/env python3
"""
NGFI March 22 Follow-up Email Campaign - Execution Script
Sends 5 personalized follow-up emails at 45-minute intervals
Email Service: Resend API
From: idirakriche9@gmail.com
"""

import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging
import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/pc/.openclaw/workspace/NGFI_SEND_LOG_MARCH23.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class NGFIEmailSender:
    def __init__(self):
        # Load API key from environment or .env file
        env_file = Path('/home/pc/.openclaw/workspace/.env.ngfi')
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith('export RESEND_API_KEY='):
                        self.api_key = line.split('"')[1]
                    elif line.startswith('export RESEND_FROM_EMAIL='):
                        self.from_email = line.split('"')[1]
        
        self.api_key = os.getenv('RESEND_API_KEY', self.api_key if hasattr(self, 'api_key') else '')
        self.from_email = os.getenv('RESEND_FROM_EMAIL', self.from_email if hasattr(self, 'from_email') else 'idirakriche9@gmail.com')
        self.api_url = 'https://api.resend.com/emails'
        self.db_path = Path('/home/pc/.openclaw/workspace/NGFI_LEADS_DATABASE.json')
        
        if not self.api_key:
            raise ValueError("RESEND_API_KEY not found in environment or .env.ngfi")
        
        logger.info(f"Initialized with API key: {self.api_key[:10]}...")
        logger.info(f"From email: {self.from_email}")
    
    def send_email(self, to_email, subject, body, prospect_id, prospect_name):
        """Send single email via Resend API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'from': self.from_email,
            'to': to_email,
            'subject': subject,
            'text': body,
            'reply_to': self.from_email
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Email sent to {to_email} | ID: {result.get('id', 'N/A')}")
                return {
                    'status': 'sent',
                    'prospect_id': prospect_id,
                    'prospect_name': prospect_name,
                    'email': to_email,
                    'subject': subject,
                    'timestamp': datetime.now().isoformat(),
                    'resend_id': result.get('id', 'N/A')
                }
            else:
                logger.error(f"❌ Failed to send to {to_email} | Status: {response.status_code} | {response.text}")
                return {
                    'status': 'failed',
                    'prospect_id': prospect_id,
                    'email': to_email,
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"❌ Exception sending to {to_email}: {str(e)}")
            return {
                'status': 'error',
                'prospect_id': prospect_id,
                'email': to_email,
                'error': str(e)
            }
    
    def execute_campaign(self, dry_run=False):
        """Execute the March 22 follow-up campaign"""
        
        emails = [
            {
                'prospect_id': 'dev_florent_p_001',
                'prospect_name': 'Florent Parcevaux',
                'email': 'florent@malt.fr',
                'subject': 'Salut Florent - Retour sur NGFI (2ème contact)',
                'body': """Salut Florent,

Je reviens vers toi - je ne suis pas certain que mon premier message t'ai parlé.

Toi qui bosses sur des projets WordPress / WooCommerce, tu dois probablement passer pas mal de temps sur l'administrative - client follow-up, devis, invoicing, etc.

Chez NGFI, on a développé une solution d'automation qui permet aux freelancers comme toi de récupérer ~10h par semaine sur ces tâches. Ça libère du temps pour faire plus de deals ou simplement avoir une meilleure work-life balance.

On peut vraiment en parler 20min cette semaine ? Pas de commitment, juste une conversation.

Merci Florent,
Idir""",
                'delay_minutes': 0
            },
            {
                'prospect_id': 'dev_jeremy_m_001',
                'prospect_name': 'Jérémy Mouzin',
                'email': 'jeremy@mouzin-dev.fr',
                'subject': 'Jérémy - Quick follow-up sur javascript developer',
                'body': """Hey Jérémy,

Dernier message sur NGFI, je te promets :)

Si tu penses toujours qu'avoir 10h de plus par semaine pour focus sur les vrais projets (au lieu de l'admin) serait utile, on devrait en parler.

J'aide des JavaScript developers exactement comme toi à automatiser le boring stuff. Un appel de 30min suffit pour voir si c'est un fit.

T'es dispo cette semaine pour 30min ?

À plus,
Idir""",
                'delay_minutes': 45
            },
            {
                'prospect_id': 'design_guillaume_schott_001',
                'prospect_name': 'Guillaume Schott',
                'email': 'guillaume@schott-design.fr',
                'subject': 'Salut Guillaume - Retour sur NGFI (2ème contact)',
                'body': """Salut Guillaume,

Je reviens vers toi - je ne suis pas certain que mon premier message t'ai parlé.

En tant que UX/UI designer freelance, je sais que tu passes pas mal de temps sur les tasks admin: briefs, revisions, invoices, client communication, etc.

NGFI c'est une solution qui automatise tout ça. On voit régulièrement des designers gagner 10h/semaine + 3x plus de deals grâce à cette automation.

On peut vraiment en parler 20min cette semaine ? Pas de commitment, juste une conversation.

Merci Guillaume,
Idir""",
                'delay_minutes': 90
            },
            {
                'prospect_id': 'writer_arnaud_m_001',
                'prospect_name': 'Arnaud Masson',
                'email': 'arnaud@masson-copywriting.fr',
                'subject': 'Arnaud - Quick follow-up sur concepteur-rédacteur / copywriter',
                'body': """Hey Arnaud,

Dernier message sur NGFI, je te promets :)

Je comprends que tu sois busy avec les projets. Mais si tu as jamais pensé que 80% de ton temps est dédié aux tasks admin (briefs, devis, suivi client, invoices...), c'est là qu'on entre en jeu.

Les copywriters que j'aide disent que NGFI leur fait gagner 10h/semaine ET plus de leads.

Ça mérite 30min pour en discuter ?

À plus,
Idir""",
                'delay_minutes': 135
            },
            {
                'prospect_id': 'writer_stephen_001',
                'prospect_name': 'Stéphen Urani',
                'email': 'stephen@malt.fr',
                'subject': 'Salut Stéphen - Retour sur NGFI (2ème contact)',
                'body': """Salut Stéphen,

Je reviens vers toi - je ne suis pas certain que mon premier message t'ai parlé.

En tant que copywriter, tu dois certainement passer pas mal de temps sur l'admin: briefs clients, négociations, invoices, follow-ups, etc. C'est normal, ça fait partie du job.

Sauf que chez NGFI, on a trouvé un moyen d'automatiser 80% de ça. Les copywriters qu'on aide gagnent ~10h par semaine + 3x plus de deals.

On peut vraiment en parler 20min cette semaine ? Pas de commitment, juste une conversation entre freelancers.

Merci Stéphen,
Idir""",
                'delay_minutes': 180
            }
        ]
        
        results = []
        start_time = datetime.now()
        
        logger.info("=" * 70)
        logger.info("🚀 NGFI March 22 Follow-up Campaign - EXECUTION START")
        logger.info(f"Campaign Date: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Total Emails: {len(emails)}")
        logger.info(f"Spacing: 45 minutes")
        logger.info(f"DRY RUN: {dry_run}")
        logger.info("=" * 70)
        
        for i, email in enumerate(emails, 1):
            # Calculate send time
            send_time = start_time + timedelta(minutes=email['delay_minutes'])
            
            # Wait if needed
            now = datetime.now()
            if send_time > now:
                wait_seconds = (send_time - now).total_seconds()
                logger.info(f"\n⏳ Email {i}/{len(emails)} scheduled for {send_time.strftime('%H:%M:%S')}")
                logger.info(f"   Waiting {wait_seconds:.0f} seconds...")
                
                if not dry_run:
                    time.sleep(wait_seconds)
            
            logger.info(f"\n📧 Email {i}/{len(emails)}: {email['prospect_name']}")
            logger.info(f"   To: {email['email']}")
            logger.info(f"   Subject: {email['subject']}")
            
            if dry_run:
                logger.info("   [DRY RUN - Not actually sent]")
                results.append({
                    'status': 'dry_run',
                    'prospect_id': email['prospect_id'],
                    'prospect_name': email['prospect_name'],
                    'email': email['email'],
                    'subject': email['subject']
                })
            else:
                result = self.send_email(
                    email['email'],
                    email['subject'],
                    email['body'],
                    email['prospect_id'],
                    email['prospect_name']
                )
                results.append(result)
        
        logger.info("\n" + "=" * 70)
        logger.info("📊 CAMPAIGN SUMMARY")
        logger.info("=" * 70)
        
        sent_count = sum(1 for r in results if r['status'] == 'sent')
        failed_count = sum(1 for r in results if r['status'] in ['failed', 'error'])
        
        logger.info(f"✅ Sent: {sent_count}")
        logger.info(f"❌ Failed: {failed_count}")
        logger.info(f"⏱️  Duration: {(datetime.now() - start_time).total_seconds():.1f} seconds")
        
        # Update database
        self.update_database(results)
        
        return results
    
    def update_database(self, results):
        """Update NGFI_LEADS_DATABASE.json with send results"""
        try:
            with open(self.db_path) as f:
                db = json.load(f)
            
            for result in results:
                if result['status'] in ['sent', 'dry_run']:
                    for prospect in db['prospects']:
                        if prospect['id'] == result['prospect_id']:
                            prospect['status'] = 'email_sent'
                            
                            if prospect['id'] not in [a.get('prospect_id') for a in prospect.get('contact_attempts', [])]:
                                if 'contact_attempts' not in prospect:
                                    prospect['contact_attempts'] = []
                                
                                prospect['contact_attempts'].append({
                                    'date': result.get('timestamp', datetime.now().isoformat()),
                                    'channel': 'smtp',
                                    'status': result['status'],
                                    'subject': result.get('subject', 'N/A'),
                                    'resend_id': result.get('resend_id', 'N/A')
                                })
                            
                            prospect['last_contact_date'] = result.get('timestamp', datetime.now().isoformat())
                            logger.info(f"✅ Updated database for {prospect['name']}")
                            break
            
            with open(self.db_path, 'w') as f:
                json.dump(db, f, indent=2)
            
            logger.info(f"✅ Database updated: {self.db_path}")
        except Exception as e:
            logger.error(f"❌ Failed to update database: {str(e)}")


if __name__ == '__main__':
    import sys
    
    # Check for dry-run flag
    dry_run = '--dry-run' in sys.argv or '-d' in sys.argv
    
    try:
        sender = NGFIEmailSender()
        results = sender.execute_campaign(dry_run=dry_run)
        
        logger.info("\n✨ Campaign execution completed successfully")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Campaign failed: {str(e)}")
        sys.exit(1)
