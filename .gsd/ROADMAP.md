# ROADMAP.md

> **Current Phase**: Not started
> **Milestone**: v1.0

## Must-Haves (from SPEC)
- [ ] Data Ingestion & Web Scraping Pipeline
- [ ] Vector Database & Embeddings Setup
- [ ] LLM RAG recommendation logic with multi-domain balancing
- [ ] FastAPI Endpoints (`/health`, `/recommend`)
- [ ] Evaluation script for Mean Recall@10

## Phases

### Phase 1: Data Scraping & Catalog Ingestion
**Status**: ⬜ Not Started
**Objective**: Build a robust script (using Selenium/Playwright or BeautifulSoup if feasible) to extract all SHL assessment details from their product catalog and store them efficiently.

### Phase 2: Knowledge Base & RAG Engine
**Status**: ✅ Complete
**Objective**: Implement the embedding generation for the catalog items, set up a local Vector DB (e.g., ChromaDB or FAISS), and connect the Gemini LLM via LangChain/LlamaIndex.

### Phase 3: Recommendation & Balancing Logic
**Status**: ✅ Complete
**Objective**: Implement the core search logic that handles multi-domain queries (hard skills vs soft skills) and formats the output into the required structure.

### Phase 4: API Development
**Status**: ✅ Complete
**Objective**: Wrap the recommendation engine in a FastAPI application that implements the `/health` and `/recommend` endpoints according to the strict JSON schema.

### Phase 5: Evaluation & Accuracy Tuning
**Status**: ⬜ Not Started
**Objective**: Run the engine against the `Gen_AI Dataset.xlsx` training dataset, measure the Mean Recall@10, iteratively improve the prompts/search, and output the final test CSV script.
