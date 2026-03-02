# SPEC.md — Project Specification

> **Status**: `FINALIZED`

## Vision
Build an intelligent, LLM-powered Retrieval-Augmented Generation (RAG) system that recommends the most relevant SHL assessments based on a user's Job Description (JD) or natural language query. It acts as an API service.

## Goals
1. Implement a robust Data Ingestion Pipeline to scrape/retrieve SHL assessment details from their product catalog.
2. Build a recommendation engine using RAG techniques (e.g. LangChain/LlamaIndex, Gemini LLM, Vector Embeddings) to accurately match queries to assessments.
3. Serve the engine via a scalable Python HTTP API (FastAPI) with `/health` and `/recommend` endpoints matching the strict output schema.
4. Intelligently balance recommendations when a query spans multiple domains (e.g., tech skills vs behavioral traits).
5. Generate an evaluation CSV output (`Query`, `Assessment_url`) maximizing Mean Recall@10 on the provided dataset.

## Non-Goals (Out of Scope)
- Developing a graphical user interface (GUI) or full-stack web application beyond the API endpoints (unless requested).
- Pre-calculating or hardcoding results without an actual dynamic RAG engine.

## Users
Recruiters, Hiring Managers, and HR platforms needing automated screening assessment recommendations based on job descriptions.

## Constraints
- **Technical**: Must use Python, HTTP API framework (FastAPI), JSON responses, and proper status codes. Free-tier friendly cloud services and LLMs (e.g., Gemini Free API).
- **Compliance**: Must strictly follow the output schema provided in the assignment for automated scoring.
- **Scraping**: Solutions without a clear scraping/retrieval mechanism of the SHL catalog will be rejected. 

## Success Criteria
- [ ] Endpoints `/health` and `/recommend` are fully functional and adhere exactly to the required API spec.
- [ ] The engine parses catalog information, creating rich embeddings for accurate semantic search.
- [ ] Multi-domain queries return a balanced mix of "Knowledge & Skills" and "Personality & Behavior" tests.
- [ ] Mean Recall@10 on the test set is highly optimized.
- [ ] Pipeline runs correctly over the test set format.
