import os
import pandas as pd
import requests
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class AdzunaExecutiveFetcher:
    def __init__(self):
        self.app_id = os.getenv("ADZUNA_APP_ID")
        self.app_key = os.getenv("ADZUNA_APP_KEY")
        # 'in' for India, 'gb' for UK, 'us' for USA depending on your search target
        self.country = os.getenv("ADZUNA_COUNTRY", "in") 
        self.base_url = f"http://api.adzuna.com/v1/api/jobs/{self.country}/search"

    def fetch_executive_jobs(self, pages:int = 20) -> List[Dict]:
        all_jobs = []
        # Target executive keywords using boolean logic
        query_what = '("VP")'
        
        for page in range(1, pages + 1):
            url = f"{self.base_url}/{page}"
            params = {
                "app_id": self.app_id,
                "app_key": self.app_key,
                "results_per_page": 50,
                "what": query_what,
                "content-type": "application/json"
            }
            
            try:
                print(f"🚀 Querying Adzuna Page {page} for executive roles...")
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                results = data.get("results", [])
                
                for job in results:
                    # Parse and safely unpack nested locations
                    location_data = job.get("location", {})
                    display_name = location_data.get("display_name", "Unknown Location")
                    areas = location_data.get("area", [])
                    
                    all_jobs.append({
                        "id": str(job.get("id")),
                        "title": job.get("title"),
                        "company": job.get("company", {}).get("display_name"),
                        "description": job.get("description"),
                        "location": display_name,
                        "regions": ", ".join(areas),
                        "salary_min": job.get("salary_min"),
                        "salary_max": job.get("salary_max"),
                        "redirect_url": job.get("redirect_url")
                    })
                    
            except Exception as e:
                print(f"❌ Failed to fetch page {page}: {e}")
                break
                
        print(f"✅ Extracted {len(all_jobs)} corporate leadership leads.")
        return all_jobs
    
if __name__ == "__main__":
    # Initialize the fetcher
        fetcher = AdzunaExecutiveFetcher()
        
        # Test it by fetching just 1 page to check the output quickly
        jobs = fetcher.fetch_executive_jobs(pages=20)
       # 🚨 ADD THIS GUARD CLAUSE: Break early if the network call fails or keys are missing
        if not jobs:
            print("⚠️ No data received from Adzuna. Check your API credentials or search limits.")
            
        
        # Print out the results to your terminal
        print("\n--- SAMPLE OUTPUT DATA ---")
        import json
        print(json.dumps(jobs[:2], indent=2)) # Prints the first 2 jobs cleanly