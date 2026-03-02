# Phase 2: RAG Engine Development Summary

## Work Completed
- Built `src/ingest.py` to tokenize, generate embeddings (using `all-MiniLM-L6-v2`), and persist the scraped SHL catalog into a local ChromaDB database.
- Upgraded the project architecture to use LangChain Expression Language (LCEL) over deprecated standard Chains.
- Resolved dependency issues between LangChain, HuggingFace, and Transformers.
- Validated semantic accuracy by configuring Semantic Search `kwargs={"k": 3}` and routing queries directly to `gemini-2.5-flash` natively integrated via `langchain-google-genai`.
- Process passed integration tests successfully recognizing explicit "Account Manager Solution" query endpoints.
