# Phase 3: Recommendation & Balancing Logic Summary

## Work Completed
- **Task 3.1: Query Analyzer (`src/analyzer.py`)**
  - Integrated `langchain-google-genai` using structured output mode.
  - Generates a Pydantic `QueryIntent` object to programmatically flag if a JD demands Hard Skills, Soft Skills, or both.
- **Task 3.2: Balanced Retriever (`src/balancer.py`)**
  - Implemented metadata routing rules targeting ChromaDB vector embeddings.
  - Automatically queries the semantic engine for `test_type` partitions, combining `Knowledge` and `Personality` domains equally if joint skills are necessitated.
  - Ensured correct output schemas mapped iteratively as `[{"title": "...", "Assessment_url": "..."}]` enabling absolute compatibility with Phase 4 routing.
