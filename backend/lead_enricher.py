import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

class LeadEnricher:
    def __init__(self):
        # Setting a standard user-agent so the web request looks like a normal browser
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def find_decision_makers(self, company_name: str):
        print(f"🕵️‍♂️ Hunting for decision makers at: {company_name}")
        
        # Target executive roles specifically linked to the company name on LinkedIn
        roles_query = '("CEO" OR "Founder" OR "HR Head" OR "HR Director" OR "Managing Director")'
        search_phrase = f"site:linkedin.com/in/ \"{company_name}\" {roles_query}"
        
        # Using DuckDuckGo's lightweight HTML service for clean, no-token searching
        url = f"https://html.duckduckgo.com/html/?q={search_phrase}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                print(f"⚠️ Search engine throttled or returned status {response.status_code}")
                return []
                
            soup = BeautifulSoup(response.text, 'html.parser')
            discovered_people = []
            
            # Look for standard search snippet outcome blocks
            for result in soup.find_all('div', class_='result__body'):
                links = result.find_all('a', class_='result__url')
                snippets = result.find_all('a', class_='result__snippet')
                
                if links and snippets:
                    profile_url = links[0].get('href', '')
                    meta_text = snippets[0].get_text()
                    
                    # Double check it's a valid individual profile link
                    if 'linkedin.com/in/' in profile_url:
                        discovered_people.append({
                            "linkedin_url": profile_url,
                            "snippet_data": meta_text.strip()
                        })
                        
            return discovered_people[:2]  # Keep the top 2 best matches per company
            
        except Exception as e:
            print(f"❌ Failed searching for {company_name}: {e}")
            return []

    def run_enrichment_pipeline(self, input_csv: str):
        if not os.path.exists(input_csv):
            print(f"❌ File not found at: {input_csv}")
            return
            
        df = pd.read_csv(input_csv)
        
        # Drop rows where company name is blank or corrupted
        if 'company' not in df.columns:
            print("❌ Input CSV does not contain a 'company' column.")
            return
            
        unique_companies = df['company'].dropna().unique()
        print(f"📊 Loaded CSV. Found {len(unique_companies)} unique companies to process.")
        
        enriched_leads = []
        
        for company in unique_companies:
            if not company or company == 'unknown':
                continue
                
            contacts = self.find_decision_makers(company)
            
            for person in contacts:
                enriched_leads.append({
                    "target_company": company,
                    "linkedin_profile": person["linkedin_url"],
                    "raw_bio_text": person["snippet_data"]
                })
                
            # Anti-throttling courtesy delay: pause 2 seconds between lookups
            sleep(2)
            
        # Convert output to a new DataFrame and save it
        enriched_df = pd.DataFrame(enriched_leads)
        output_file = "app/data/enriched_contacts.csv"
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        enriched_df.to_csv(output_file, index=False)
        print(f"🎉 Pipeline Complete! Contact leads saved to {output_file}")
        return enriched_df

if __name__ == "__main__":
    enricher = LeadEnricher()
    # Path inside the Docker workspace maps directly to your app/data folder
    enricher.run_enrichment_pipeline("app/data/extracted_executives.csv")