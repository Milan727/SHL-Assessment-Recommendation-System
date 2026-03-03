# SHL Assessment Recommendation System

An intelligent recommendation engine designed to ingest SHL's product catalog and recommend the top 10 most relevant assessments based on natural language HR hiring queries or job descriptions.

**Deployed Architecture:**
- **Web UI (Streamlit):** [Live Demo](https://shl-assessment-recommendation-system-jcvjlgd3ojb8epveyhji7i.streamlit.app)
- **REST API (FastAPI):** [API Documentation](https://shl-assessment-recommendation-system-yl80.onrender.com/docs)

---

## 🏗️ Architecture & Tech Stack

This project implements a **Hybrid RAG (Retrieval-Augmented Generation)** pipeline.

- **Data Ingestion:** Playwright scraper to extract 518+ SHL assessments.
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2`
- **Vector Store:** ChromaDB
- **LLM Engine:** Gemini 1.5 Pro (for Intent Classification) + Local Synonym Expansion Engine
- **Search Strategy:** Hybrid Search combining Semantic Similarity, BM25 Keyword Matching, and Metadata Filtering across Round-Robin Interleaved pools.
- **Backend:** FastAPI
- **Frontend:** Streamlit

---

## 🚀 Local Setup & Installation

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API Key

### 2. Installation
Clone the repository and install the dependencies in a virtual environment:
```bash
git clone https://github.com/Milan727/SHL-Assessment-Recommendation-System.git
cd SHL-Assessment-Recommendation-System

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your Gemini API key:
```env
GOOGLE_API_KEY="your-gemini-api-key-here"
```

---

## 💻 Running the Application

### Option A: Run the Backend API (FastAPI)
```bash
export PYTHONPATH=.
uvicorn src.app:app --host 0.0.0.0 --port 8000
```
- The API will be available at `http://localhost:8000`
- Swagger UI Documentation: `http://localhost:8000/docs`

### Option B: Run the Frontend UI (Streamlit)
```bash
export PYTHONPATH=.
streamlit run src/app_ui.py
```
- The UI will open in your browser at `http://localhost:8501`

---

## 📈 Evaluation Results

The system was evaluated against a provided test dataset consisting of 65 query-to-assessment records.

- **Metric Evaluated:** Mean Recall@10
- **Score Achieved:** **100%** (All 65 expected URLs were successfully recommended within the Top 10 results).
- To reproduce the evaluation, run:
  ```bash
  python src/evaluate.py
  ```

---

## 📂 Project Structure

```
├── data/                  # Shl catalog json, vector database (ChromaDB), and resulting CSV outputs
├── src/
│   ├── app.py             # FastAPI entry point
│   ├── app_ui.py          # Streamlit user interface
│   ├── scraper.py         # Playwright script for SHL catalog extraction
│   ├── ingest.py          # Data enrichment and vectorization into ChromaDB 
│   ├── analyzer.py        # Gemini LLM intent routing & synonym keyword expansion
│   ├── balancer.py        # The core Hybrid Search algorithm and caching logic
│   ├── evaluate.py        # Script to test system accuracy against the Gen_AI Dataset
|   └── generate_test_predictions.py    # Script to predict on the unlabeled test set
├── requirements.txt       # Project dependencies
└── README.md              # You are here!
```

---
*Developed for the SHL AI Intern Generative AI assessment.*
