#!/usr/bin/env python3
"""
NGFI Resend Email Automation
Sends personalized emails via Resend API
"""

import json
import requests
import os
from datetime import datetime
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/pc/.openclaw/workspace/logs/resend_email.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ResendEmailManager:
    def __init__(self):
        self.api_key = os.getenv('RESEND_API_KEY', 're_Bo8g2f47_7KBim8rM1bKAfHRPigcMn9hJ')
        self.from_email = os.getenv('RESEND_FROM_EMAIL', 'idirakriche9@gmail.com')  # ✅ Compte vérifié
        self.api_url = "https://api.resend.com/emails"
        self.leads_db_path = Path('/home/pc/.openclaw/workspace/NGFI_LEADS_DATABASE.json')
        
        if not self.api_key:
            raise ValueError("❌ RESEND_API_KEY not found in environment")
        
        logger.info(f"✅ Resend Manager initialized")
        logger.info(f"   From: {self.from_email}")
        logger.info(f"   API Key: {self.api_key[:20]}...")
    
    def load_leads(self):
        """Load prospects from database"""
        try:
            with open(self.leads_db_path) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load leads: {e}")
            return {}
    
    def get_not_contacted_prospects(self, limit=100, test_mode=False):
        """Get prospects not yet contacted via email"""
        leads_db = self.load_leads()
        prospects = [
            p for p in leads_db.get('prospects', [])
            if p.get('status') == 'not_contacted'
        ]
        
        if test_mode:
            # Test mode: envoyer vers email du compte
            logger.info("⚠️ TEST MODE: Envoi vers email de test")
            prospects = prospects[:limit]
        else:
            # Production: seulement prospects avec email
            prospects = [p for p in prospects if p.get('email')][:limit]
        
        return prospects
    
    def generate_email_body(self, prospect):
        """Generate personalized email body"""
        name = prospect.get('name', 'there').split()[0]
        sector = prospect.get('sector', 'freelance')
        website = prospect.get('website', '')
        
        body = f"""
Salut {name},

J'ai découvert ton super travail en tant que {sector}.

Les freelances passent 30-40% de leur temps sur l'admin et la prospection — du temps perdu !

NGFI automatise tout ça :
→ 10h+ gagnées chaque semaine
→ Prospection 24/7
→ Admin zéro stress
→ 49€/mois (s'autofinance avec 2-3 clients de plus)

Ça t'intéresse une démo rapide ? (15 min max)

À bientôt,
Idir
---
NGFI - L'IA pour freelances
https://ngfi.fr
"""
        
        return body.strip()
    
    def send_email(self, prospect, test_mode=False):
        """Send personalized email via Resend API"""
        try:
            name = prospect.get('name', 'Prospect')
            
            # TEST MODE: envoyer vers le compte de test
            if test_mode:
                email = 'idirakriche9@gmail.com'
                logger.info(f"📧 TEST MODE: {name} → {email}")
            else:
                email = prospect.get('email')
                if not email:
                    logger.warning(f"No email for {name}")
                    return None
            
            subject = f"Gagne 10h/semaine {name.split()[0]} - NGFI"
            body = self.generate_email_body(prospect)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "from": self.from_email,
                "to": email,
                "subject": subject,
                "html": f"<p>{body.replace(chr(10), '<br>')}</p>"
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"✅ Email sent to {email} ({name})")
                return {
                    'success': True,
                    'email': email,
                    'prospect_id': prospect.get('id'),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                logger.error(f"❌ Failed to send to {email}: {response.text}")
                return None
        
        except Exception as e:
            logger.error(f"Exception sending email: {e}")
            return None
    
    def send_batch(self, limit=100, test_mode=False):
        """Send batch of emails"""
        prospects = self.get_not_contacted_prospects(limit, test_mode=test_mode)
        
        if not prospects:
            logger.info("No prospects to contact")
            return []
        
        if test_mode:
            logger.info(f"🧪 TEST MODE: Sending {len(prospects)} test emails to {self.from_email}...")
        else:
            logger.info(f"Sending {len(prospects)} emails...")
        
        results = []
        for i, prospect in enumerate(prospects):
            result = self.send_email(prospect, test_mode=test_mode)
            if result:
                results.append(result)
            # Rate limiting (2 req/sec max)
            if (i + 1) % 2 == 0:
                import time
                time.sleep(0.6)
        
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
                    p['contact_attempts'].append({
                        'date': result['timestamp'],
                        'channel': 'email_resend',
                        'status': 'sent'
                    })
                    break
        
        # Save
        with open(self.leads_db_path, 'w') as f:
            json.dump(leads_db, f, indent=2)
        
        logger.info(f"✅ Database updated: {len(email_results)} prospects marked as emailed")
    
    def run_daily_email_wave(self, limit=100, test_mode=False):
        """Execute daily email sending wave"""
        logger.info("="*60)
        if test_mode:
            logger.info("🧪 TEST MODE: NGFI Email Wave (Resend)")
        else:
            logger.info("🚀 PRODUCTION: NGFI Email Wave (Resend)")
        logger.info("="*60)
        
        results = self.send_batch(limit, test_mode=test_mode)
        
        if results:
            self.update_database(results)
            logger.info(f"✅ Email wave complete: {len(results)} emails sent")
        else:
            logger.info("⚠️ No emails sent this wave")
        
        return {
            'status': 'success',
            'emails_sent': len(results),
            'timestamp': datetime.now().isoformat(),
            'mode': 'test' if test_mode else 'production'
        }

if __name__ == "__main__":
    # Load environment variables directly
    import os
    import sys
    os.environ['RESEND_API_KEY'] = 're_Bo8g2f47_7KBim8rM1bKAfHRPigcMn9hJ'
    os.environ['RESEND_FROM_EMAIL'] = 'onboarding@resend.dev'
    
    manager = ResendEmailManager()
    
    # Check if TEST_MODE argument passed
    test_mode = '--test' in sys.argv or 'test' in sys.argv
    result = manager.run_daily_email_wave(100, test_mode=test_mode)
    
    print("\n" + "="*60)
    print("RESEND EMAIL WAVE - RESULTS")
    print("="*60)
    print(f"Status: {result['status'].upper()}")
    print(f"Emails Sent: {result['emails_sent']}")
    print(f"Timestamp: {result['timestamp']}")
    print("="*60)
