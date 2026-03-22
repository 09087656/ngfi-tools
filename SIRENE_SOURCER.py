#!/usr/bin/env python3
"""
SIRENE Sourcer — Extract French independents (auto-entrepreneurs)
API: https://api.insee.fr/catalogue/site/themes/sirene
"""

import requests
import json
import csv
from datetime import datetime
import time

# SIRENE API endpoint (updated 2024)
SIRENE_API = "https://api.insee.fr/entreprises/sirene/V3.11"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "NGFI-Sourcer/1.0"
}

def search_independents(limit=100):
    """
    Search SIRENE for independent workers (auto-entrepreneurs, freelancers)
    Filter: Active businesses, individual entrepreneurs
    """
    
    prospects = []
    
    # Query: Auto-entrepreneurs, all sectors
    # Using basic search without auth (limited but works)
    params = {
        "q": "etatAdministratifUniteLegale:Actif AND natureJuridiqueUniteLegale:1000",
        "nombre": min(limit, 100),  # API limits to 100 per request
        "format": "json"
    }
    
    try:
        print(f"🔍 Querying SIRENE API for {limit} independents...")
        response = requests.get(f"{SIRENE_API}/siret", params=params, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("etablissements", [])
            print(f"✅ Found {len(results)} results")
            
            for est in results[:limit]:
                try:
                    prospect = {
                        "siret": est.get("siret"),
                        "siren": est.get("siren"),
                        "name": est.get("uniteLegaleVoieEtablissement", "N/A"),
                        "sector": est.get("libelleSectionEconomique", "Unknown"),
                        "activity": est.get("libelleActivitePrincipaleEtablissement", "N/A"),
                        "city": est.get("libelleCommuneEtablissement", "N/A"),
                        "postal_code": est.get("codePostalEtablissement", "N/A"),
                        "status": "not_enriched",
                        "created_at": datetime.now().isoformat()
                    }
                    prospects.append(prospect)
                except Exception as e:
                    print(f"⚠️  Error parsing record: {e}")
                    continue
            
            return prospects
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return []


def save_to_json(prospects, filename="SIRENE_PROSPECTS.json"):
    """Save prospects to JSON for next step (enrichment)"""
    output = {
        "source": "SIRENE",
        "count": len(prospects),
        "extracted_at": datetime.now().isoformat(),
        "prospects": prospects
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Saved {len(prospects)} prospects to {filename}")
    return filename


def save_to_csv(prospects, filename="SIRENE_PROSPECTS.csv"):
    """Also save as CSV for easy viewing"""
    if not prospects:
        print("⚠️  No prospects to save")
        return None
    
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=prospects[0].keys())
        writer.writeheader()
        writer.writerows(prospects)
    
    print(f"📊 CSV saved: {filename}")
    return filename


def main():
    print("=" * 50)
    print("SIRENE SOURCER - Extract French Independents")
    print("=" * 50)
    
    # Extract 100 independents
    prospects = search_independents(limit=100)
    
    if prospects:
        # Save both formats
        save_to_json(prospects)
        save_to_csv(prospects)
        
        print(f"\n✅ SUCCESS: {len(prospects)} prospects extracted")
        print("\nNext steps:")
        print("1. Use SIRENE_PROSPECTS.json for Dropcontact enrichment")
        print("2. Enrich with emails via Dropcontact API")
        print("3. Verify emails before outreach")
    else:
        print("❌ No prospects found. Check API/internet connection.")


if __name__ == "__main__":
    main()
