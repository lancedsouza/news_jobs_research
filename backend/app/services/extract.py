from adzuna_fetcher import AdzunaExecutiveFetcher
import os 
import json
import pandas as pd

def extract_and_save_executives():
    fetcher = AdzunaExecutiveFetcher()
    
    # 1. Fetch from Adzuna (testing with 1 page first)
    executives = fetcher.fetch_executive_jobs(pages=20)

    jobs = []
    for job in executives:
        clean_job = {
            'company': (job.get('company') or '').lower(),
            'title': (job.get('title') or '').lower(),
            'location': (job.get('location') or '').lower(),
            'regions': (job.get('regions') or '').lower(),
            'salary_min': job.get('salary_min'),
            'salary_max': job.get('salary_max'),    
        }
        # FIX 1: Indented this inside the loop so EVERY job gets added to the list!
        jobs.append(clean_job)

    # 2. Convert the list of dictionaries directly into a DataFrame
    df = pd.DataFrame(jobs)

    print("\n--- PANDAS DATAFRAME COMPLETED ---")
    print(df.head())
    
    # 3. Define where you want to save it and export it to a clean CSV
    output_file = "app/data/extracted_executives.csv"
    
    # Ensure the directory exists so it doesn't fail
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save the dataframe to a CSV file without the index numbers column
    df.to_csv(output_file, index=False)
    print(f"✅ Saved {len(df)} executive leads to {output_file}")
    
    # Return it so other scripts can access it if needed
    return df

if __name__ == "__main__":
    # FIX 2: Capture the dataframe variable returned by the function
    extracted_df = extract_and_save_executives()
    
    print("\n--- EXECUTIVE EXTRACTION COMPLETE ---")
    if not extracted_df.empty:
        print(extracted_df.head(2)) # Prints just the top 2 rows to confirm it works