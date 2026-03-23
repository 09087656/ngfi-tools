#!/usr/bin/env python3
"""
NGFI Cold Email Campaign - Gmail SMTP
Sends personalized follow-up emails via Gmail
"""

import json
import time
import logging
import smtplib
from datetime import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/pc/.openclaw/workspace/NGFI_SEND_LOG_GMAIL.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class NGFIEmailSenderGmail:
    def __init__(self):
        # Gmail credentials
        self.gmail_user = "idirakriche@gmail.com"  # Your Gmail
        self.gmail_app_password = "ygkm dqqf gpvg rmac"  # Gmail App Password (16 chars, spaces)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
        self.db_path = Path('/home/pc/.openclaw/workspace/NGFI_LEADS_DATABASE.json')
        
        logger.info(f"Initialized Gmail sender: {self.gmail_user}")
    
    def load_database(self):
        """Load prospects from database"""
        with open(self.db_path) as f:
            return json.load(f)
    
    def save_database(self, db):
        """Save updated database"""
        with open(self.db_path, 'w') as f:
            json.dump(db, f, indent=2)
    
    def get_email_template(self, prospect):
        """Generate personalized email"""
        name = prospect['name'].split()[0]
        sector = prospect['sector']
        
        templates = [
            {
                "subject": f"Salut {name} - 5h/semaine d'admin en moins?",
                "body": f"""Salut {name},

Combien de temps tu passes chaque semaine sur l'admin? Factures, relances, TVA, charges...

Pour la plupart des {sector.lower()} que je rencontre, c'est 5-10h/semaine qui partent en fumée.

J'ai développé NGFI justement pour ça — tout automatisé en 15 min, pas plus.

Tu veux tester? C'est gratuit.

À plus
Idir
NGFI
https://ngfi.fr
"""
            },
            {
                "subject": f"{name} - Les freelancers gagnent 30% plus avec l'automation",
                "body": f"""Salut {name},

87% des {sector.lower()} frustré par l'admin.

Ceux qui automatisent? Ils gagnent 30% plus (vrais chiffres).

C'est pas magique — c'est juste qu'ils récupèrent 8-10h/semaine.

NGFI = 1 clic, tout automatisé.

Gratuit si tu veux essayer.

Idir
NGFI
https://ngfi.fr
"""
            }
        ]
        
        import random
        template = random.choice(templates)
        return template
    
    def send_email(self, prospect, subject, body):
        """Send email via Gmail SMTP"""
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.gmail_user, self.gmail_app_password)
            
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = prospect['email']
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server.send_message(msg)
            server.quit()
            
            logger.info(f"✅ Email sent to {prospect['name']} ({prospect['email']})")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send to {prospect['email']}: {str(e)}")
            return False
    
    def run(self):
        """Main execution"""
        logger.info("=" * 70)
        logger.info("🚀 NGFI Cold Email Campaign - Gmail SMTP")
        logger.info(f"Campaign Date: {datetime.now()}")
        logger.info("=" * 70)
        
        db = self.load_database()
        
        # Get prospects with status "not_contacted" or "email_ready"
        targets = [p for p in db['prospects'] 
                   if p.get('status') in ['not_contacted', 'email_ready', 'pending_send']][:10]
        
        sent_count = 0
        for i, prospect in enumerate(targets, 1):
            template = self.get_email_template(prospect)
            
            logger.info(f"\n📧 Email {i}/{len(targets)}: {prospect['name']}")
            logger.info(f"   To: {prospect['email']}")
            logger.info(f"   Subject: {template['subject']}")
            
            if self.send_email(prospect, template['subject'], template['body']):
                # Update database
                prospect['status'] = 'email_sent'
                prospect['last_contact_date'] = datetime.now().isoformat()
                prospect['contact_attempts'] = prospect.get('contact_attempts', [])
                prospect['contact_attempts'].append({
                    'date': datetime.now().isoformat(),
                    'channel': 'smtp_gmail',
                    'status': 'sent',
                    'subject': template['subject']
                })
                sent_count += 1
                
                # Wait 45 minutes between emails (or 30 seconds for testing)
                if i < len(targets):
                    logger.info(f"   ⏳ Waiting 45 minutes before next email...")
                    time.sleep(2700)  # 45 minutes
            
            # Save after each send
            self.save_database(db)
        
        logger.info("\n" + "=" * 70)
        logger.info(f"✅ Campaign Complete: {sent_count}/{len(targets)} emails sent")
        logger.info("=" * 70)
        
        return sent_count

if __name__ == "__main__":
    sender = NGFIEmailSenderGmail()
    sender.run()
