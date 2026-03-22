#!/usr/bin/env python3
"""
NGFI SMTP Email Automation (Simple & Direct)
Sends personalized cold emails via Gmail SMTP
50 emails/day with optimal timing
Requires: Gmail App Password (not regular password)
"""

import json
import smtplib
import time
from datetime import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SMTPEmailManager:
    def __init__(self, from_email='idirakriche9@gmail.com', app_password=None):
        """Initialize SMTP Email manager"""
        self.from_email = from_email
        self.app_password = app_password or self.load_app_password()
        self.leads_db_path = Path('/home/pc/.openclaw/workspace/NGFI_LEADS_DATABASE.json')
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        
        logger.info("📧 SMTP Email Manager initialized")
        logger.info(f"   From: {self.from_email}")
    
    def load_app_password(self):
        """Load app password from environment or file"""
        import os
        password = os.getenv('GMAIL_APP_PASSWORD')
        if not password:
            # Try to load from secure file
            pwd_file = Path('/home/pc/.openclaw/workspace/.gmail_app_password')
            if pwd_file.exists():
                with open(pwd_file) as f:
                    password = f.read().strip()
        
        if not password:
            raise ValueError("❌ Gmail app password not found. Set GMAIL_APP_PASSWORD env var or create .gmail_app_password file")
        
        return password
    
    def load_leads(self):
        """Load prospects from database"""
        try:
            with open(self.leads_db_path) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load leads: {e}")
            return {}
    
    def get_not_contacted_prospects(self, limit=50):
        """Get prospects not yet contacted via email"""
        leads_db = self.load_leads()
        prospects = [
            p for p in leads_db.get('prospects', [])
            if p.get('status') == 'not_contacted' and p.get('email')
        ]
        return prospects[:limit]
    
    def generate_email_body(self, prospect):
        """Generate personalized email body using PAS framework"""
        name = prospect.get('name', 'there').split()[0]
        sector = prospect.get('sector', 'freelance')
        
        body = f"""Salut {name},

J'ai découvert ton super travail en tant que {sector}.

Les freelances comme toi passent 30-40% de leur temps sur l'admin et la prospection — du temps qu'on pourrait mieux utiliser.

NGFI c'est l'IA pour freelances:
→ 10h+ gagnées chaque semaine
→ Prospection 24/7 automatisée
→ Admin zéro stress
→ 49€/mois (s'autofinance avec 2-3 clients de plus)

Ça t'intéresse une démo rapide? (15 min max)

À bientôt,
Idir
---
NGFI - L'IA pour freelances
https://ngfi.fr"""
        
        return body.strip()
    
    def send_email(self, prospect):
        """Send personalized email via SMTP"""
        try:
            email = prospect.get('email')
            name = prospect.get('name', 'Prospect')
            
            if not email:
                logger.warning(f"No email for {name}")
                return None
            
            subject = f"Gagne 10h/semaine {name.split()[0]} - NGFI"
            body = self.generate_email_body(prospect)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = email
            
            # Text part
            text_part = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # Send via SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.from_email, self.app_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"✅ Email sent to {email} ({name})")
            
            return {
                'success': True,
                'email': email,
                'prospect_id': prospect.get('id'),
                'timestamp': datetime.now().isoformat(),
                'subject': subject
            }
        
        except smtplib.SMTPAuthenticationError:
            logger.error(f"❌ SMTP Auth failed - check app password")
            raise
        except Exception as e:
            logger.error(f"❌ Failed to send to {email}: {e}")
            return None
    
    def send_batch(self, limit=50):
        """Send batch of emails"""
        prospects = self.get_not_contacted_prospects(limit)
        
        if not prospects:
            logger.info("No prospects to contact")
            return []
        
        logger.info(f"🚀 Sending {len(prospects)} emails via SMTP (Gmail)...")
        
        results = []
        for i, prospect in enumerate(prospects, 1):
            result = self.send_email(prospect)
            if result:
                results.append(result)
            
            # Rate limiting - Gmail SMTP allows ~1 per second
            if i < len(prospects):
                logger.info(f"   [{i}/{len(prospects)}] Waiting 1.5s...")
                time.sleep(1.5)
        
        logger.info(f"✅ Batch complete: {len(results)}/{len(prospects)} sent")
        return results
    
    def update_database(self, email_results):
        """Update database with email send status"""
        leads_db = self.load_leads()
        
        for result in email_results:
            prospect_id = result['prospect_id']
            for p in leads_db['prospects']:
                if p['id'] == prospect_id:
                    p['status'] = 'email_sent'
                    p['last_contact_date'] = result['timestamp']
                    if 'contact_attempts' not in p:
                        p['contact_attempts'] = []
                    p['contact_attempts'].append({
                        'date': result['timestamp'],
                        'channel': 'smtp',
                        'status': 'sent',
                        'subject': result.get('subject')
                    })
                    break
        
        # Save
        with open(self.leads_db_path, 'w') as f:
            json.dump(leads_db, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Database updated: {len(email_results)} prospects marked as emailed")
    
    def run_daily_email_wave(self, limit=50):
        """Execute daily email sending wave"""
        logger.info("="*60)
        logger.info(f"📧 NGFI Email Wave - Gmail SMTP")
        logger.info(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"👤 From: {self.from_email}")
        logger.info("="*60)
        
        try:
            results = self.send_batch(limit)
            
            if results:
                self.update_database(results)
                logger.info(f"✅ Email wave complete: {len(results)} emails sent")
            else:
                logger.info("⚠️ No emails sent this wave")
            
            return {
                'status': 'success',
                'emails_sent': len(results),
                'timestamp': datetime.now().isoformat(),
                'method': 'smtp'
            }
        
        except Exception as e:
            logger.error(f"❌ Email wave failed: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

if __name__ == "__main__":
    import sys
    
    # Get app password from command line or environment
    app_password = None
    if len(sys.argv) > 1:
        app_password = sys.argv[1]
    
    try:
        manager = SMTPEmailManager(app_password=app_password)
        result = manager.run_daily_email_wave(50)
        
        print("\n" + "="*60)
        print("GMAIL SMTP EMAIL WAVE - RESULTS")
        print("="*60)
        print(f"Status: {result['status'].upper()}")
        print(f"Emails Sent: {result.get('emails_sent', 'N/A')}")
        print(f"Method: {result.get('method', 'N/A')}")
        print(f"Timestamp: {result['timestamp']}")
        if 'error' in result:
            print(f"Error: {result['error']}")
        print("="*60)
    
    except ValueError as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTo use this script, you need a Gmail App Password:")
        print("1. Go to: myaccount.google.com/apppasswords")
        print("2. Select 'Mail' and 'Windows Computer'")
        print("3. Google generates a 16-char password")
        print("4. Use it: python NGFI_SMTP_EMAIL.py '<your-app-password>'")
        print("   OR set: export GMAIL_APP_PASSWORD='<your-app-password>'")
        sys.exit(1)
