---
phase: 3
plan: 1
wave: 1
---

# Plan 3.1: Recommendation & Balancing Logic

## Objective
Implement the core search logic to handle multi-domain queries by identifying if a query requires hard skills, soft skills, or both, and balancing the ChromaDB retrieval results accordingly.

## Context
- `.gsd/SPEC.md`
- `SHL AI Intern RE Generative AI assignment.pdf` (Balancing requirements)
- `src/rag.py` (Current implementation)

## Tasks

<task type="auto">
  <name>Implement Query Analyzer</name>
  <files>src/analyzer.py</files>
  <action>
    - Create a new module `src/analyzer.py`.
    - Use `ChatGoogleGenerativeAI` with Structured Output (or JSON mode) to analyze a given JD/query.
    - The LLM should return a JSON object with boolean flags: `requires_hard_skills` and `requires_soft_skills`.
    - Example: "Need a Java developer good at collaborating" -> `{"requires_hard_skills": true, "requires_soft_skills": true}`.
  </action>
  <verify>source venv/bin/activate && python -c "from src.analyzer import analyze_query; print(analyze_query('Java dev team player'))"</verify>
  <done>Query analyzer accurately decomposes intent.</done>
</task>

<task type="auto">
  <name>Implement Balanced Retriever Pipeline</name>
  <files>src/balancer.py, src/rag.py</files>
  <action>
    - Refactor `src/rag.py` or create `src/balancer.py` to use the analyzer.
    - If a query needs BOTH skill types:
      - Query ChromaDB with a filter for `test_type` containing "Knowledge" (fetch top K/2).
      - Query ChromaDB with a filter for `test_type` containing "Personality" (fetch top K/2).
    - If only one is needed, fetch top K from that specific domain.
    - Combine the fetched documents and pass them to the RAG LLM to generate the final rationale and format the JSON.
    - Return a list of dictionaries containing `title` and `url`.
  </action>
  <verify>source venv/bin/activate && python -c "from src.balancer import get_balanced_recommendations; print(get_balanced_recommendations('Need a Python dev who communicates well'))"</verify>
  <done>Returns a balanced set of URL recommendations using metadata filtering.</done>
</task>

## Success Criteria
- [ ] Multi-domain queries pull correctly from both "Knowledge & Skills" and "Personality & Behavior" categories.
- [ ] The LLM correctly formats the output as a list of dictionaries matching the target assessment URLs.
