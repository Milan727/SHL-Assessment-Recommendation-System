import os
import sys
import time
import pandas as pd
from tqdm import tqdm
from src.balancer import get_balanced_recommendations

DATASET_PATH = "data/Gen_AI Dataset.xlsx"
OUTPUT_PATH = "data/results.csv"

def evaluate_recall():
    if not os.path.exists(DATASET_PATH):
        print(f"Error: Target dataset {DATASET_PATH} not found.")
        sys.exit(1)
        
    print(f"Loading dataset from {DATASET_PATH}...")
    try:
        df = pd.read_excel(DATASET_PATH)
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        sys.exit(1)
        
    if "Query" not in df.columns or "Assessment_url" not in df.columns:
        print(f"Error: Dataset is missing required columns. Found: {df.columns.tolist()}")
        sys.exit(1)
        
    total_queries = len(df)
    hits = 0
    results = []
    
    print(f"Executing RAG pipeline evaluation across {total_queries} records...")
    
    # Iterate through the rows using tqdm for a progress bar
    for index, row in tqdm(df.iterrows(), total=total_queries, desc="Evaluating"):
        query = str(row["Query"])
        expected_url = str(row["Assessment_url"]).strip()
        
        try:
            # Fetch Top 10 RAG Recommendations
            recommendations = get_balanced_recommendations(query, k=10)
            recommended_urls = [rec.get("Assessment_url", "").strip() for rec in recommendations]
            
            # Check for a HIT (Recall@10)
            hit = expected_url in recommended_urls
            if hit:
                hits += 1
                
            # Log Result
            results.append({
                "Query": query,
                "Expected_URL": expected_url,
                "Hit": hit,
                "Predicted_URLs_List": " | ".join(recommended_urls)
            })
            
        except Exception as e:
            print(f"\nError processing query '{query}': {e}")
            results.append({
                "Query": query,
                "Expected_URL": expected_url,
                "Hit": False,
                "Predicted_URLs_List": f"ERROR: {str(e)}"
            })
                
        pass
            
    # Calculate Mean Recall@10
    recall = (hits / total_queries) * 100 if total_queries > 0 else 0
    
    # Save the output report
    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT_PATH, index=False)
    
    print("\n" + "="*50)
    print("EVALUATION RESULTS")
    print("="*50)
    print(f"Total Queries Evaluated: {total_queries}")
    print(f"Total Hits (Top 10):     {hits}")
    print(f"Mean Recall@10:          {recall:.2f}%")
    print("="*50)
    print(f"Detailed analytical report saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    evaluate_recall()
