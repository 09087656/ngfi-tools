#!/usr/bin/env python3
"""
NGFI Gmail Email Automation
Sends personalized cold emails via Gmail API
50 emails/day max with optimal timing
"""

import json
import base64
import pickle
import os
from datetime import datetime
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from google.auth.oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials as OAuth2Credentials
from googleapiclient.discovery import build
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GmailEmailManager:
    def __init__(self, credentials_file='/home/pc/.openclaw/workspace/credentials.json'):
        """Initialize Gmail API manager"""
        self.credentials_file = credentials_file
        self.service = None
        self.from_email = 'idirakriche9@gmail.com'
        self.leads_db_path = Path('/home/pc/.openclaw/workspace/NGFI_LEADS_DATABASE.json')
        
        logger.info("📧 Gmail Email Manager initialized")
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Gmail API"""
        try:
            # Check if token exists
            token_file = Path('/home/pc/.openclaw/workspace/gmail_token.pickle')
            
            if token_file.exists():
                with open(token_file, 'rb') as token:
                    creds = pickle.load(token)
                    if creds.expired and creds.refresh_token:
                        creds.refresh(Request())
            else:
                # Create new auth flow
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
                
                # Save token
                with open(token_file, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("✅ Gmail API authenticated")
            
        except Exception as e:
            logger.error(f"❌ Authentication failed: {e}")
            raise
    
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
        """Send personalized email via Gmail API"""
        try:
            email = prospect.get('email')
            name = prospect.get('name', 'Prospect')
            
            if not email:
                logger.warning(f"No email for {name}")
                return None
            
            subject = f"Gagne 10h/semaine {name.split()[0]} - NGFI"
            body = self.generate_email_body(prospect)
            
            # Create message
            message = {
                'raw': base64.urlsafe_b64encode(
                    f"""From: {self.from_email}
To: {email}
Subject: {subject}

{body}""".encode()
                ).decode()
            }
            
            # Send
            result = self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()
            
            logger.info(f"✅ Email sent to {email} ({name})")
            
            return {
                'success': True,
                'email': email,
                'prospect_id': prospect.get('id'),
                'message_id': result.get('id'),
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"❌ Failed to send to {email}: {e}")
            return None
    
    def send_batch(self, limit=50):
        """Send batch of emails"""
        prospects = self.get_not_contacted_prospects(limit)
        
        if not prospects:
            logger.info("No prospects to contact")
            return []
        
        logger.info(f"🚀 Sending {len(prospects)} emails (Gmail API)...")
        
        results = []
        for i, prospect in enumerate(prospects):
            result = self.send_email(prospect)
            if result:
                results.append(result)
            
            # Rate limiting - Gmail allows ~1 email per second
            if i < len(prospects) - 1:
                import time
                time.sleep(1.2)
        
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
                        'channel': 'gmail_api',
                        'status': 'sent',
                        'message_id': result.get('message_id')
                    })
                    break
        
        # Save
        with open(self.leads_db_path, 'w') as f:
            json.dump(leads_db, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Database updated: {len(email_results)} prospects marked as emailed")
    
    def run_daily_email_wave(self, limit=50):
        """Execute daily email sending wave"""
        logger.info("="*60)
        logger.info(f"📧 NGFI Email Wave - Gmail API")
        logger.info(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*60)
        
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
            'method': 'gmail_api'
        }

if __name__ == "__main__":
    manager = GmailEmailManager()
    result = manager.run_daily_email_wave(50)
    
    print("\n" + "="*60)
    print("GMAIL EMAIL WAVE - RESULTS")
    print("="*60)
    print(f"Status: {result['status'].upper()}")
    print(f"Emails Sent: {result['emails_sent']}")
    print(f"Method: {result['method']}")
    print(f"Timestamp: {result['timestamp']}")
    print("="*60)
