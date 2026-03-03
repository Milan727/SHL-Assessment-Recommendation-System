import os
import json
import re
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Paths
DATA_PATH = "data/shl_catalog.json"
CHROMA_PATH = "data/chroma_db"

def extract_keywords_from_url(url):
    """Extract searchable keywords from URL slug."""
    slug = url.rstrip("/").split("/")[-1]
    # Replace hyphens with spaces and clean up
    keywords = slug.replace("-", " ")
    # Remove common suffixes
    keywords = re.sub(r'\b(new|solution|sift out|report)\b', '', keywords, flags=re.IGNORECASE).strip()
    return keywords

def build_rich_content(item):
    """Build enriched page_content for better semantic matching."""
    title = item["title"]
    test_type = item["test_type"]
    description = item.get("description", title)
    
    content = f"Assessment: {title}\nCategory: {test_type}\nDescription: {description}"
    
    return content

def main():
    print(f"Loading data from {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} does not exist. Run the scraper first.")
        return

    with open(DATA_PATH, "r") as f:
        catalog = json.load(f)

    # Convert to LangChain Document objects with enriched content
    documents = []
    for item in catalog:
        page_content = build_rich_content(item)
        
        doc = Document(
            page_content=page_content,
            metadata={
                "title": item["title"],
                "url": item["url"],
                "test_type": item["test_type"]
            }
        )
        documents.append(doc)
        
    print(f"Created {len(documents)} enriched Document objects.")
    print(f"Sample content:\n{documents[0].page_content}\n")

    print("Initializing HuggingFace Embeddings (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print(f"Building Chroma vector store at {CHROMA_PATH}...")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    
    print(f"Vector store successfully persisted to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()
