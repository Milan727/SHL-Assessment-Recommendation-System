---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Project Environment & Data Ingestion Setup

## Objective
Set up the Python environment and build a web scraper to extract SHL assessment details from their dynamic product catalog, storing the output as structured data for the RAG engine.

## Context
- .gsd/SPEC.md
- .gsd/ROADMAP.md
- URL: `https://www.shl.com/solutions/products/product-catalog/`

## Tasks

<task type="auto">
  <name>Setup Python Environment & Dependencies</name>
  <files>requirements.txt, .gitignore</files>
  <action>
    - Create a `requirements.txt` with necessary libraries: `fastapi`, `uvicorn`, `playwright`, `pandas`, `langchain`, `langchain-google-genai`, `chromadb`, `sentence-transformers`, `python-dotenv`.
    - Create a standard Python `.gitignore`.
    - Note: Do NOT install them globally, let the executor create the venv.
  </action>
  <verify>cat requirements.txt && cat .gitignore</verify>
  <done>Files exist with the correct target dependencies and exclusion rules.</done>
</task>

<task type="auto">
  <name>Build SHL Catalog Scraper</name>
  <files>src/scraper.py, src/run_scraper.py</files>
  <action>
    - Ensure Playwright is used since the SHL catalog is dynamically rendered (evidenced by "Outdated browser detected" on standard GET requests).
    - Write a script to navigate the SHL product catalog URL.
    - Extract assessment Title, URL, and (crucially) the Test Type (e.g., Knowledge & Skills, Personality & Behavior) by navigating through pagination or scrolling as needed.
    - Save the extracted data reliably into `data/shl_catalog.json` or `csv`.
  </action>
  <verify>python -m playwright install && python src/run_scraper.py --test-mode</verify>
  <done>A script successfully navigates the URL and produces a populated JSON/CSV file containing structured assessment data.</done>
</task>

## Success Criteria
- [ ] Dependencies are cleanly managed.
- [ ] The scraper successfully extracts assessment data without being blocked by basic bot-protection.
- [ ] Output data contains Title, URL, and Test Type for multi-domain queries.
