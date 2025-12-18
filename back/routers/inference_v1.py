# app/routers/inference.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from functools import lru_cache
from transformers import pipeline


router = APIRouter()

# You can dynamically load models by name
AVAILABLE_MODELS = {
    "sentiment": ("text-classification", "tabularisai/multilingual-sentiment-analysis"),
}

class InferenceRequest(BaseModel):
    task: str
    text: str

@lru_cache(maxsize=3)
def get_pipeline(task: str):
    if task not in AVAILABLE_MODELS:
        raise ValueError(f"Unknown task: {task}")
    print(f"Loading model for {task} ...")
    return pipeline(AVAILABLE_MODELS[task][0], model=AVAILABLE_MODELS[task][1])


def predict(request: InferenceRequest):
    """Predict using the specified task and text."""
    try:
        pipe = get_pipeline(request.task)
        result = pipe(request.text, return_all_scores=True)
        return {"task": request.task, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))