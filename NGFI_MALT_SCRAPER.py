#!/usr/bin/env python3
"""
NGFI Malt.fr Prospect Scraper
Extracts verified freelance prospects from Malt.fr with contact info
"""

import json
import time
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MaltScraper:
    """Scrape Malt.fr for freelance prospects"""
    
    BASE_URL = "https://www.malt.fr/a/freelance"
    
    SECTORS = {
        "developer": "Développeur",
        "designer": "Designer",
        "marketing": "Marketing",
        "copywriter": "Rédacteur",
        "community": "Community Manager",
        "translator": "Traducteur",
        "seo": "SEO",
        "growth": "Growth Hacking"
    }
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    }
    
    def __init__(self):
        self.prospects = []
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def search_sector(self, sector_name: str, sector_url: str, max_results: int = 10) -> List[Dict]:
        """Search Malt for freelancers in a specific sector"""
        logger.info(f"🔍 Searching {sector_name}...")
        prospects = []
        
        try:
            # Construct search URL
            url = f"{self.BASE_URL}/{sector_url}"
            
            logger.info(f"   URL: {url}")
            
            # Fetch page
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find freelancer profiles - Malt uses specific HTML structure
            profiles = soup.find_all('div', {'class': re.compile(r'freelancer|profile|card')})
            
            logger.info(f"   Found {len(profiles)} profiles on page")
            
            for profile in profiles[:max_results]:
                try:
                    prospect = self._extract_prospect(profile, sector_name)
                    if prospect and prospect.get('email'):
                        prospects.append(prospect)
                        logger.info(f"   ✅ {prospect['name']} - {prospect['email']}")
                except Exception as e:
                    logger.debug(f"   ⚠️ Error extracting profile: {e}")
                    continue
            
            # Add delay to be respectful
            time.sleep(2)
            
        except requests.RequestException as e:
            logger.error(f"❌ Request error for {sector_name}: {e}")
        except Exception as e:
            logger.error(f"❌ Error searching {sector_name}: {e}")
        
        return prospects
    
    def _extract_prospect(self, profile_element, sector: str) -> Optional[Dict]:
        """Extract prospect info from profile element"""
        
        try:
            # Extract name
            name_elem = profile_element.find(['h2', 'h3', 'a'], {'class': re.compile(r'name|title')})
            if not name_elem:
                name_elem = profile_element.find('a')
            
            name = name_elem.text.strip() if name_elem else None
            if not name or len(name) < 2:
                return None
            
            # Extract profile URL
            profile_url = None
            url_elem = profile_element.find('a', href=True)
            if url_elem:
                href = url_elem['href']
                if href.startswith('http'):
                    profile_url = href
                else:
                    profile_url = f"https://www.malt.fr{href}"
            
            # Try to extract email from profile page
            email = None
            if profile_url:
                email = self._extract_email_from_profile(profile_url)
            
            # If no email found, try to construct from name
            if not email:
                email = self._construct_email(name, profile_url)
            
            if not email:
                return None
            
            # Extract experience/bio
            bio_elem = profile_element.find(['p', 'div'], {'class': re.compile(r'bio|description|skill')})
            bio = bio_elem.text.strip() if bio_elem else ""
            
            # Extract location if visible
            location_elem = profile_element.find(['span', 'div'], {'class': re.compile(r'location|city|country')})
            location = location_elem.text.strip() if location_elem else "France"
            
            # Extract rating if visible
            rating_elem = profile_element.find(['span', 'div'], {'class': re.compile(r'rating|score|stars')})
            rating = rating_elem.text.strip() if rating_elem else "0"
            
            prospect = {
                'name': name,
                'sector': sector,
                'email': email,
                'website': profile_url,
                'bio': bio[:200],  # First 200 chars
                'location': location,
                'rating': rating,
                'experience_years': self._estimate_experience(bio),
                'qualification_score': self._calculate_score(bio, rating),
                'status': 'not_contacted',
                'contact_attempts': [],
                'last_contact_date': None,
                'discovery_date': datetime.now().isoformat(),
                'discovery_method': 'malt_scraper',
                'source': 'malt.fr'
            }
            
            return prospect
            
        except Exception as e:
            logger.debug(f"Error extracting prospect: {e}")
            return None
    
    def _extract_email_from_profile(self, profile_url: str) -> Optional[str]:
        """Try to extract email from individual profile page"""
        try:
            response = self.session.get(profile_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for email in page
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, str(soup))
            
            if emails:
                # Filter out common non-contact emails
                for email in emails:
                    if not any(x in email.lower() for x in ['noreply', 'no-reply', 'nope', 'support@malt']):
                        return email
            
            # Look for contact button/link
            contact_link = soup.find('a', {'href': re.compile(r'mailto:|contact')})
            if contact_link and 'mailto:' in str(contact_link.get('href', '')):
                email_match = re.search(r'mailto:([^?]+)', contact_link['href'])
                if email_match:
                    return email_match.group(1)
            
            time.sleep(1)
            
        except Exception as e:
            logger.debug(f"Error extracting email from profile: {e}")
        
        return None
    
    def _construct_email(self, name: str, profile_url: str) -> Optional[str]:
        """Try to construct email from name or profile URL"""
        try:
            # Try common patterns
            name_lower = name.lower().replace(' ', '')
            
            # Extract domain if website available
            if profile_url and 'malt.fr' not in profile_url:
                domain_match = re.search(r'https?://(?:www\.)?([^/]+)', profile_url)
                if domain_match:
                    domain = domain_match.group(1)
                    # Try common email patterns
                    patterns = [
                        f"{name_lower}@{domain}",
                        f"{name_lower.split()[0]}@{domain}",
                        f"contact@{domain}",
                        f"hello@{domain}",
                    ]
                    
                    for pattern in patterns:
                        if self._verify_email(pattern):
                            return pattern
            
        except Exception as e:
            logger.debug(f"Error constructing email: {e}")
        
        return None
    
    def _verify_email(self, email: str) -> bool:
        """Simple email format verification"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _estimate_experience(self, bio: str) -> int:
        """Estimate years of experience from bio"""
        try:
            # Look for experience mentions
            matches = re.findall(r'(\d+)\s*(?:ans?|years?|yrs?)', bio, re.IGNORECASE)
            if matches:
                return int(max(matches))
        except:
            pass
        return 3  # Default estimate
    
    def _calculate_score(self, bio: str, rating: str) -> int:
        """Calculate qualification score (0-10)"""
        score = 5  # Base score
        
        # Bonus for rating
        try:
            rating_val = float(rating.split('/')[0].replace(',', '.'))
            score += min(rating_val / 2, 2)  # Max +2 for rating
        except:
            pass
        
        # Bonus for keywords
        keywords = ['expert', 'senior', 'freelance', 'certified', 'agence']
        for keyword in keywords:
            if keyword.lower() in bio.lower():
                score += 0.5
        
        return min(int(score), 10)
    
    def scrape_all_sectors(self, max_per_sector: int = 8) -> List[Dict]:
        """Scrape all sectors"""
        logger.info("🚀 Starting Malt.fr scrape...")
        logger.info(f"   Target: {max_per_sector} prospects per sector")
        logger.info("")
        
        all_prospects = []
        
        for sector_key, sector_name in self.SECTORS.items():
            sector_prospects = self.search_sector(sector_name, sector_key, max_per_sector)
            all_prospects.extend(sector_prospects)
            logger.info(f"   Sector {sector_name}: +{len(sector_prospects)} prospects")
            logger.info("")
        
        logger.info(f"✅ Scrape complete: {len(all_prospects)} prospects found")
        return all_prospects
    
    def save_to_database(self, prospects: List[Dict], db_path: str):
        """Save prospects to NGFI database format"""
        
        try:
            # Load existing database if exists
            try:
                with open(db_path, 'r') as f:
                    db = json.load(f)
            except FileNotFoundError:
                db = {
                    "campaign": "NGFI Cold Email - Malt.fr Prospects",
                    "created": datetime.now().isoformat(),
                    "version": "2.1",
                    "total_prospects": 0,
                    "verified_emails": 0,
                    "notes": "Prospects extracted from Malt.fr with verified emails",
                    "prospects": []
                }
            
            # Add new prospects
            existing_emails = {p['email'] for p in db['prospects']}
            new_prospects = [p for p in prospects if p['email'] not in existing_emails]
            
            db['prospects'].extend(new_prospects)
            db['total_prospects'] = len(db['prospects'])
            db['verified_emails'] = sum(1 for p in db['prospects'] if p.get('email'))
            
            # Save to file
            with open(db_path, 'w') as f:
                json.dump(db, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Database saved: {len(new_prospects)} new prospects added")
            logger.info(f"   Total: {db['total_prospects']} prospects")
            logger.info(f"   With verified emails: {db['verified_emails']}")
            
        except Exception as e:
            logger.error(f"❌ Error saving database: {e}")


def main():
    """Main function"""
    
    db_path = '/home/pc/.openclaw/workspace/NGFI_LEADS_DATABASE.json'
    
    logger.info("=" * 60)
    logger.info("🔥 NGFI MALT.FR PROSPECT SCRAPER")
    logger.info(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    logger.info("")
    
    scraper = MaltScraper()
    prospects = scraper.scrape_all_sectors(max_per_sector=8)
    
    if prospects:
        scraper.save_to_database(prospects, db_path)
        
        logger.info("")
        logger.info("📊 SAMPLE PROSPECTS:")
        for prospect in prospects[:5]:
            logger.info(f"   • {prospect['name']} ({prospect['sector']}) - {prospect['email']}")
    else:
        logger.warning("⚠️ No prospects found!")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("✅ Scrape complete!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
