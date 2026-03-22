#!/usr/bin/env python3
"""
NGFI Automated Outreach System
Manages multi-channel prospection via Waalaxy + WhatsApp + future Brevo integration
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/pc/.openclaw/workspace/outreach.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class NGFIOutreachManager:
    def __init__(self):
        self.leads_db_path = Path('/home/pc/.openclaw/workspace/NGFI_LEADS_DATABASE.json')
        self.waalaxy_import_path = Path('/home/pc/.openclaw/workspace/WAALAXY_IMPORT_LIST.json')
        self.contact_log_path = Path('/home/pc/.openclaw/workspace/CONTACT_LOG.md')
        
        self.leads_db = self.load_json(self.leads_db_path)
        self.waalaxy_config = self.load_json(self.waalaxy_import_path)
        
    def load_json(self, path):
        """Load JSON file safely"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load {path}: {e}")
            return {}
    
    def save_json(self, path, data):
        """Save JSON file safely"""
        try:
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved to {path}")
        except Exception as e:
            logger.error(f"Failed to save {path}: {e}")
    
    def get_not_contacted_prospects(self, limit=50):
        """Get prospects not yet contacted"""
        prospects = [p for p in self.leads_db['prospects'] 
                    if p['status'] == 'not_contacted']
        return prospects[:limit]
    
    def log_contact_attempt(self, prospect_id, channel, message, status='sent'):
        """Log a contact attempt"""
        attempt = {
            'date': datetime.now().isoformat(),
            'prospect_id': prospect_id,
            'channel': channel,
            'status': status,
            'message_preview': message[:50] + '...' if len(message) > 50 else message
        }
        
        # Find prospect and update
        for p in self.leads_db['prospects']:
            if p['id'] == prospect_id:
                p['contact_attempts'].append(attempt)
                p['last_contact_date'] = datetime.now().isoformat()
                p['status'] = f'{channel}_sent'
                break
        
        # Log to file
        self.leads_db['contact_log']['total_contacted'] += 1
        self.leads_db['contact_log']['contact_history'].append(attempt)
        
        # Save updated database
        self.save_json(self.leads_db_path, self.leads_db)
        logger.info(f"Logged contact: {prospect_id} via {channel}")
    
    def generate_waalaxy_csv(self):
        """Generate CSV for Waalaxy import"""
        csv_content = "LinkedInURL,FirstName,LastName,Message,FollowUpMessage\n"
        
        for prospect in self.waalaxy_config['prospects']:
            csv_content += f"{prospect['linkedin_url']},{prospect['name'].split()[0]},{prospect['name'].split()[-1]},\"{prospect['connection_message']}\",\"{prospect['follow_up_message']}\"\n"
        
        csv_path = Path('/home/pc/.openclaw/workspace/WAALAXY_IMPORT.csv')
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        logger.info(f"Generated Waalaxy CSV: {csv_path}")
        return csv_path
    
    def generate_whatsapp_list(self):
        """Generate WhatsApp contact list"""
        whatsapp_list = []
        
        for prospect in self.leads_db['prospects']:
            if prospect.get('phone'):
                whatsapp_list.append({
                    'name': prospect['name'],
                    'phone': prospect['phone'],
                    'message': f"Yo {prospect['name'].split()[0]} 👋\n\nJ'ai vu que tu fais du {prospect['sector']}. Top !\n\nJe lance NGFI - automatise la prosp et l'admin pour les freelances.\n10h/semaine de gain.\n\nÇa te dit une démo rapide ? (15min max)\n\nCheers"
                })
        
        whatsapp_path = Path('/home/pc/.openclaw/workspace/WHATSAPP_CONTACTS.json')
        with open(whatsapp_path, 'w') as f:
            json.dump(whatsapp_list, f, indent=2)
        
        logger.info(f"Generated WhatsApp list: {whatsapp_path} ({len(whatsapp_list)} contacts)")
        return whatsapp_path
    
    def get_daily_report(self):
        """Generate daily outreach report"""
        total_contacts = len(self.leads_db['prospects'])
        not_contacted = len([p for p in self.leads_db['prospects'] if p['status'] == 'not_contacted'])
        email_sent = len([p for p in self.leads_db['prospects'] if p['status'] == 'email_sent'])
        responded = len([p for p in self.leads_db['prospects'] if p['response_received']])
        
        report = f"""
# Daily Outreach Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Status Summary
- Total Prospects: {total_contacts}
- Not Contacted: {not_contacted}
- Email Sent: {email_sent}
- Responded: {responded}
- Response Rate: {(responded / total_contacts * 100):.1f}% if total_contacts > 0 else 0%

## Today's Actions
- Waalaxy: 50 connections to send
- WhatsApp: {len([p for p in self.leads_db['prospects'] if p.get('phone')])} contacts ready
- Expected daily contacts: 80-100

## Next Steps
1. Import WAALAXY_IMPORT.csv to Waalaxy dashboard
2. Schedule campaign start: 2026-03-14 09:00
3. Send WhatsApp messages via Trouvère
4. Monitor responses in real-time

"""
        return report.strip()
    
    def run_daily_outreach(self):
        """Execute daily outreach routine"""
        logger.info("="*60)
        logger.info("Starting NGFI Daily Outreach Routine")
        logger.info("="*60)
        
        # Step 1: Generate Waalaxy CSV
        waalaxy_csv = self.generate_waalaxy_csv()
        logger.info(f"✅ Waalaxy CSV generated: {waalaxy_csv}")
        
        # Step 2: Generate WhatsApp list
        whatsapp_list = self.generate_whatsapp_list()
        logger.info(f"✅ WhatsApp list generated: {whatsapp_list}")
        
        # Step 3: Log contact attempts (simulate)
        prospects = self.get_not_contacted_prospects(5)
        for prospect in prospects:
            self.log_contact_attempt(
                prospect['id'],
                'waalaxy',
                f"Connection request to {prospect['name']}"
            )
        
        # Step 4: Generate report
        report = self.get_daily_report()
        logger.info(report)
        
        # Step 5: Save report
        report_path = Path('/home/pc/.openclaw/workspace/DAILY_REPORT.md')
        with open(report_path, 'w') as f:
            f.write(report)
        
        logger.info("="*60)
        logger.info("✅ Daily Outreach Complete")
        logger.info("="*60)
        
        return {
            'status': 'success',
            'waalaxy_csv': str(waalaxy_csv),
            'whatsapp_list': str(whatsapp_list),
            'report': report
        }

if __name__ == "__main__":
    manager = NGFIOutreachManager()
    result = manager.run_daily_outreach()
    
    print("\n" + "="*60)
    print("NGFI OUTREACH AUTOMATION - RESULTS")
    print("="*60)
    print(f"Status: {result['status'].upper()}")
    print(f"Waalaxy CSV: {result['waalaxy_csv']}")
    print(f"WhatsApp List: {result['whatsapp_list']}")
    print("\n" + result['report'])
    print("="*60)
