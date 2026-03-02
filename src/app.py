from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.balancer import get_balanced_recommendations
import uvicorn

app = FastAPI(title="SHL Assessment Recommendation API")

class QueryRequest(BaseModel):
    query: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/recommend")
def recommend_assessment(req: QueryRequest):
    try:
        recommendations = get_balanced_recommendations(req.query)
        return {
            "query": req.query,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
