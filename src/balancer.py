import os
import json
from dotenv import load_dotenv

load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from src.analyzer import analyze_query

CHROMA_PATH = "data/chroma_db"

def get_balanced_recommendations(query: str, k: int = 10):
    # 1. Analyze Intent
    intent = analyze_query(query)
    
    # 2. Init Vector Store
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    docs = []
    
    try:
        if intent.requires_hard_skills and intent.requires_soft_skills:
            # Balance
            k_each = max(1, k // 2)
            hard_docs = vectorstore.similarity_search(query, k=k_each, filter={"test_type": {"$contains": "Knowledge"}})
            soft_docs = vectorstore.similarity_search(query, k=k_each, filter={"test_type": {"$contains": "Personality"}})
            docs.extend(hard_docs)
            docs.extend(soft_docs)
        elif intent.requires_hard_skills:
            docs = vectorstore.similarity_search(query, k=k, filter={"test_type": {"$contains": "Knowledge"}})
        elif intent.requires_soft_skills:
            docs = vectorstore.similarity_search(query, k=k, filter={"test_type": {"$contains": "Personality"}})
        else:
            # Fallback
            docs = vectorstore.similarity_search(query, k=k)
    except Exception as filtering_error:
        print(f"Filtering error (fallback to standard search): {filtering_error}")
        docs = vectorstore.similarity_search(query, k=k)
        
    # Standardize format
    recommendations = []
    seen_urls = set()
    
    for d in docs:
        url = d.metadata.get("url")
        if url and url not in seen_urls:
            seen_urls.add(url)
            recommendations.append({
                "title": d.metadata.get("title", "Unknown"),
                "Assessment_url": url
            })
            
    # If filtering returned too few results because we lack metadata in test dataset, fallback to general search
    if not recommendations:
        fallback_docs = vectorstore.similarity_search(query, k=k)
        for d in fallback_docs:
            url = d.metadata.get("url")
            if url and url not in seen_urls:
                seen_urls.add(url)
                recommendations.append({
                    "title": d.metadata.get("title", "Unknown"),
                    "Assessment_url": url
                })
                
    # Truncate to K max
    return recommendations[:k]

if __name__ == "__main__":
    test_q = "Need a Python dev who communicates well"
    res = get_balanced_recommendations(test_q)
    print(f"Results for: {test_q}")
    print(json.dumps(res, indent=2))
