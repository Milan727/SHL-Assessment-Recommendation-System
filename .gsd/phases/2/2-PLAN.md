---
phase: 2
plan: 1
wave: 1
---

# Plan 2.1: Knowledge Base Ingestion & Retriever Setup

## Objective
Initialize a local ChromaDB instance, generate embeddings for the SHL catalog items, and connect the Gemini LLM via LangChain.

## Context
- `prd.json` (Stories RAG-1 to RAG-4)
- `.gsd/ROADMAP.md`
- URL: Scraped data in `data/shl_catalog.json`

## Tasks

<task type="auto">
  <name>Setup Vector Store and Embeddings</name>
  <files>src/ingest.py</files>
  <action>
    - Ensure `.env` is loaded.
    - Read `data/shl_catalog.json`.
    - Generate LangChain Document objects with `page_content` containing the title, URL, and test type to provide rich semantic search context.
    - Use `HuggingFaceEmbeddings` with the `all-MiniLM-L6-v2` model.
    - Store the data in a persistent local ChromaDB database at `data/chroma_db`.
  </action>
  <verify>source venv/bin/activate && python src/ingest.py && ls -la data/chroma_db</verify>
  <done>ChromaDB is populated securely and persistently on disk.</done>
</task>

<task type="auto">
  <name>Connect Gemini LLM and RAG Logic</name>
  <files>src/rag.py</files>
  <action>
    - Implement a simple RetrievalQA chain or a function using the updated LangChain APIs snippet.
    - Configure `ChatGoogleGenerativeAI` to use `gemini-1.5-flash` or similar.
    - Initialize the QA retriever to extract the top K chunks.
    - Test the retrieval chain by asking "What assessments are related to Account Managers?".
  </action>
  <verify>source venv/bin/activate && python src/rag.py</verify>
  <done>The LangChain RAG pipeline accurately links the prompt to the correct SHL catalog item using similarity search.</done>
</task>

## Success Criteria
- [ ] ChromaDB directory generated containing `.sqlite3` or parquet files.
- [ ] Gemini successfully answers a contextual query based *only* on the RAG context.
