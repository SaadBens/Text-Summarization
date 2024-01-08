from fastapi import FastAPI, HTTPException, Depends
from starlette.responses import RedirectResponse
import uvicorn
from pydantic import BaseModel
import os
from celery import Celery
from textSummarization.pipeline.prediction import PredictionPipeline

app = FastAPI()
celery_app = Celery(broker='your_broker_url')

# Pydantic models for request and response
class PredictionRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    summary: str

@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train", responses={202: {"description": "Accepted: Training started"}})
async def training():
    task = celery_app.send_task('train_model')
    return {"task_id": task.id, "status": "Training started"}

@app.post("/predict", response_model=PredictionResponse)
async def predict_route(request: PredictionRequest):
    try:
        obj = PredictionPipeline()
        summary = obj.predict(request.text)
        return PredictionResponse(summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=int(os.getenv("PORT", 8080)))