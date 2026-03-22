#!/usr/bin/env python3
"""
NGFI Email Verification Tool
Checks if emails are valid and deliverable
"""

import json
import time
import logging
import re
import socket
from datetime import datetime
from typing import Dict, List, Tuple

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EmailVerifier:
    """Verify email deliverability"""
    
    def __init__(self):
        self.results = []
    
    def verify_format(self, email: str) -> Tuple[bool, str]:
        """Check email format validity"""
        if not email:
            return False, "Empty email"
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid format"
        
        return True, "Valid format"
    
    def verify_domain_exists(self, email: str) -> Tuple[bool, str]:
        """Check if domain has MX records (can receive emails)"""
        try:
            domain = email.split('@')[1]
            
            # Try to get MX records
            try:
                mx_records = socket.getmxhost(domain)
                if mx_records:
                    return True, f"Domain OK (MX found: {mx_records[0]})"
            except socket.error:
                pass
            
            # Fallback: check if domain resolves
            try:
                socket.gethostbyname(domain)
                return True, "Domain resolves (DNS OK)"
            except socket.gaierror:
                return False, f"Domain not found: {domain}"
        
        except Exception as e:
            return False, f"Error checking domain: {str(e)}"
    
    def verify_common_patterns(self, email: str, name: str) -> Tuple[bool, str]:
        """Check for common email patterns (firstname@, contact@, etc)"""
        email_lower = email.lower()
        name_lower = name.lower()
        
        # Suspicious patterns
        suspicious = [
            ('noreply', 'Noreply address'),
            ('no-reply', 'No-reply address'),
            ('nope', 'Invalid pattern'),
            ('test', 'Test email'),
            ('fake', 'Fake email'),
            ('example', 'Example domain'),
            ('temp', 'Temporary email'),
        ]
        
        for pattern, reason in suspicious:
            if pattern in email_lower:
                return False, f"Suspicious pattern: {reason}"
        
        # Positive patterns
        positive = [
            ('freelance', 'Professional domain'),
            ('dev', 'Professional domain (dev)'),
            ('design', 'Professional domain (design)'),
            ('agency', 'Professional domain (agency)'),
            ('studio', 'Professional domain (studio)'),
            ('pro', 'Professional domain (pro)'),
            ('marketing', 'Professional domain (marketing)'),
        ]
        
        for pattern, reason in positive:
            if pattern in email_lower:
                return True, f"Professional: {reason}"
        
        # Check if email follows name pattern
        name_parts = name_lower.split()
        firstname = name_parts[0] if name_parts else ''
        lastname = name_parts[-1] if len(name_parts) > 1 else ''
        
        common_patterns = [
            f"{firstname}@",
            f"{firstname}.{lastname}@",
            f"{firstname}_{lastname}@",
            f"contact@",
            f"hello@",
            f"info@",
        ]
        
        for pattern in common_patterns:
            if pattern in email_lower:
                return True, f"Matches naming pattern: {pattern}"
        
        return None, "Unknown pattern"
    
    def calculate_confidence(self, checks: Dict[str, Tuple[bool, str]]) -> int:
        """Calculate confidence score (0-100)"""
        score = 50  # Base score
        
        # Format check
        if checks.get('format', (False,))[0]:
            score += 15
        else:
            return 0  # Invalid format = 0% confidence
        
        # Domain check
        if checks.get('domain', (False,))[0]:
            score += 20
        else:
            score -= 30
        
        # Pattern check
        pattern_result = checks.get('pattern', (None,))[0]
        if pattern_result is True:
            score += 15
        elif pattern_result is False:
            score -= 35
        
        return max(0, min(100, score))
    
    def verify_email(self, email: str, name: str) -> Dict:
        """Verify a single email"""
        checks = {}
        
        # Format check
        checks['format'] = self.verify_format(email)
        
        if not checks['format'][0]:
            return {
                'email': email,
                'name': name,
                'confidence': 0,
                'status': 'INVALID',
                'reason': checks['format'][1],
                'checks': checks
            }
        
        # Domain check
        checks['domain'] = self.verify_domain_exists(email)
        
        # Pattern check
        checks['pattern'] = self.verify_common_patterns(email, name)
        
        # Calculate confidence
        confidence = self.calculate_confidence(checks)
        
        # Determine status
        if confidence >= 70:
            status = "VALID ✅"
        elif confidence >= 40:
            status = "UNCERTAIN ⚠️"
        else:
            status = "INVALID ❌"
        
        return {
            'email': email,
            'name': name,
            'confidence': confidence,
            'status': status,
            'checks': checks
        }
    
    def verify_all(self, db_path: str) -> List[Dict]:
        """Verify all emails in database"""
        
        logger.info("=" * 80)
        logger.info("🔍 NGFI EMAIL VERIFICATION")
        logger.info(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)
        logger.info("")
        
        # Load database
        try:
            with open(db_path, 'r') as f:
                db = json.load(f)
        except Exception as e:
            logger.error(f"Error loading database: {e}")
            return []
        
        prospects = db.get('prospects', [])
        logger.info(f"Verifying {len(prospects)} emails...\n")
        
        results = []
        valid_count = 0
        uncertain_count = 0
        invalid_count = 0
        
        for prospect in prospects:
            email = prospect.get('email')
            name = prospect.get('name')
            
            result = self.verify_email(email, name)
            results.append(result)
            
            # Count by status
            if '✅' in result['status']:
                valid_count += 1
                emoji = "✅"
            elif '⚠️' in result['status']:
                uncertain_count += 1
                emoji = "⚠️"
            else:
                invalid_count += 1
                emoji = "❌"
            
            confidence = result['confidence']
            print(f"{emoji} [{confidence:3d}%] {name:30s} | {email:45s}")
        
        # Summary
        logger.info("")
        logger.info("=" * 80)
        logger.info("📊 VERIFICATION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"✅ VALID (70-100%):       {valid_count:3d} emails")
        logger.info(f"⚠️ UNCERTAIN (40-69%):   {uncertain_count:3d} emails")
        logger.info(f"❌ INVALID (0-39%):      {invalid_count:3d} emails")
        logger.info(f"\nTotal:                   {len(results):3d} emails")
        logger.info("")
        
        # Breakdown by confidence
        confidence_ranges = {
            '90-100': 0,
            '70-89': 0,
            '40-69': 0,
            '20-39': 0,
            '0-19': 0,
        }
        
        for result in results:
            conf = result['confidence']
            if conf >= 90:
                confidence_ranges['90-100'] += 1
            elif conf >= 70:
                confidence_ranges['70-89'] += 1
            elif conf >= 40:
                confidence_ranges['40-69'] += 1
            elif conf >= 20:
                confidence_ranges['20-39'] += 1
            else:
                confidence_ranges['0-19'] += 1
        
        logger.info("Confidence Distribution:")
        for range_name, count in confidence_ranges.items():
            logger.info(f"  {range_name}%: {count:3d} emails")
        
        logger.info("")
        logger.info("=" * 80)
        
        return results
    
    def export_report(self, results: List[Dict], output_path: str):
        """Export verification report to CSV"""
        
        try:
            with open(output_path, 'w') as f:
                # Header
                f.write("Name,Email,Confidence,Status,Format,Domain,Pattern\n")
                
                # Rows
                for result in results:
                    name = result['name']
                    email = result['email']
                    confidence = result['confidence']
                    status = result['status'].split()[0]  # Remove emoji
                    
                    checks = result['checks']
                    format_check = "✅" if checks.get('format', (False,))[0] else "❌"
                    domain_check = "✅" if checks.get('domain', (False,))[0] else "❌"
                    pattern_check = checks.get('pattern', (None,))[0]
                    if pattern_check is True:
                        pattern_check = "✅"
                    elif pattern_check is False:
                        pattern_check = "❌"
                    else:
                        pattern_check = "?"
                    
                    f.write(f'"{name}","{email}",{confidence},{status},{format_check},{domain_check},{pattern_check}\n')
            
            logger.info(f"✅ Report exported to: {output_path}")
        
        except Exception as e:
            logger.error(f"Error exporting report: {e}")


def main():
    db_path = '/home/pc/.openclaw/workspace/NGFI_LEADS_DATABASE.json'
    report_path = '/home/pc/.openclaw/workspace/EMAIL_VERIFICATION_REPORT.csv'
    
    verifier = EmailVerifier()
    results = verifier.verify_all(db_path)
    verifier.export_report(results, report_path)
    
    logger.info("")
    logger.info("🎯 Recommendations:")
    logger.info("  - Use only VALID (90%+) emails for first campaign")
    logger.info("  - Test UNCERTAIN emails on small batch (5-10)")
    logger.info("  - Replace INVALID emails with new prospects")
    logger.info("")


if __name__ == "__main__":
    main()
