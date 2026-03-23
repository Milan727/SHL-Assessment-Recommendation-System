from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from src.balancer import get_balanced_recommendations, init_db
import uvicorn
import threading

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SHL Assessment Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pre-load model in background thread (doesn't block health checks)
def _preload_model():
    try:
        print("Pre-loading ML model and ChromaDB...")
        init_db()
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Model pre-load error: {e}")

threading.Thread(target=_preload_model, daemon=True).start()

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/recommend")
def recommend_assessment(req: QueryRequest):
    try:
        recommendations = get_balanced_recommendations(req.query, k=10)
        
        # Map to exact assignment schema
        formatted = []
        for rec in recommendations:
            test_type_raw = rec.get("test_type", "")
            # Convert test_type string to array
            if isinstance(test_type_raw, str):
                test_type_list = [t.strip() for t in test_type_raw.split("/") if t.strip()]
            else:
                test_type_list = test_type_raw if test_type_raw else []
            
            formatted.append({
                "url": rec.get("url", rec.get("Assessment_url", "")),
                "name": rec.get("name", rec.get("title", "Unknown")),
                "adaptive_support": rec.get("adaptive_support", "No"),
                "description": rec.get("description", rec.get("title", "")),
                "duration": rec.get("duration", None),
                "remote_support": rec.get("remote_support", "No"),
                "test_type": test_type_list
            })
        
        return {"recommended_assessments": formatted}
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=traceback.format_exc())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
