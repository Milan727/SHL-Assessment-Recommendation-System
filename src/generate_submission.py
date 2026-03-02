"""
Generate Submission CSV in the exact format required by the assignment.
Format: Query | Assessment_url (one row per recommendation)
"""
import os
import sys
import pandas as pd
from tqdm import tqdm
from src.balancer import get_balanced_recommendations

DATASET_PATH = "data/Gen_AI Dataset.xlsx"
OUTPUT_PATH = "data/submission.csv"

def generate_submission():
    if not os.path.exists(DATASET_PATH):
        print(f"Error: Dataset {DATASET_PATH} not found.")
        sys.exit(1)
    
    df = pd.read_excel(DATASET_PATH)
    
    if "Query" not in df.columns:
        print(f"Error: 'Query' column not found. Columns: {df.columns.tolist()}")
        sys.exit(1)
    
    # Get unique queries
    unique_queries = df["Query"].dropna().unique()
    print(f"Processing {len(unique_queries)} unique queries...")
    
    rows = []
    
    for query in tqdm(unique_queries, desc="Generating recommendations"):
        query = str(query).strip()
        if not query:
            continue
            
        try:
            recs = get_balanced_recommendations(query, k=10)
            for rec in recs:
                url = rec.get("Assessment_url", rec.get("url", ""))
                rows.append({
                    "Query": query,
                    "Assessment_url": url
                })
        except Exception as e:
            print(f"\nError for query '{query[:50]}...': {e}")
    
    # Save submission CSV
    submission_df = pd.DataFrame(rows, columns=["Query", "Assessment_url"])
    submission_df.to_csv(OUTPUT_PATH, index=False)
    
    print(f"\n{'='*50}")
    print(f"Submission CSV generated!")
    print(f"Total rows: {len(submission_df)}")
    print(f"Unique queries: {len(unique_queries)}")
    print(f"Saved to: {OUTPUT_PATH}")
    print(f"{'='*50}")

if __name__ == "__main__":
    generate_submission()
