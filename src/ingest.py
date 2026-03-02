import os
import json
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Paths
DATA_PATH = "data/shl_catalog.json"
CHROMA_PATH = "data/chroma_db"

def main():
    print(f"Loading data from {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} does not exist. Run the scraper first.")
        return

    with open(DATA_PATH, "r") as f:
        catalog = json.load(f)

    # Convert to LangChain Document objects
    documents = []
    for item in catalog:
        # We enrich the page_content to provide maximum context for semantic search
        page_content = f"Title: {item['title']}\nTest Type: {item['test_type']}"
        
        doc = Document(
            page_content=page_content,
            metadata={
                "title": item["title"],
                "url": item["url"],
                "test_type": item["test_type"]
            }
        )
        documents.append(doc)
        
    print(f"Created {len(documents)} Document objects.")

    print("Initializing HuggingFace Embeddings (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print(f"Building Chroma vector store at {CHROMA_PATH}...")
    # This will create or update the DB on disk
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    
    print(f"Vector store successfully persisted to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()
