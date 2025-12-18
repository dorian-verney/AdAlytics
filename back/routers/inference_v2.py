# app/routers/inference.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()

executor = ThreadPoolExecutor(max_workers=4)

AVAILABLE_MODELS = {
    "summarization": "your-username/summary-model",
    "ner": "your-username/ner-model"
}

class InferenceRequest(BaseModel):
    model_name: str
    text: str

pipelines = {}

def load_pipeline(model_name: str):
    if model_name not in pipelines:
        if model_name not in AVAILABLE_MODELS:
            raise ValueError(f"Model '{model_name}' not available.")
        pipelines[model_name] = pipeline(task=None, model=AVAILABLE_MODELS[model_name])
    return pipelines[model_name]

def run_inference(model_name: str, text: str):
    pipe = load_pipeline(model_name)
    return pipe(text)

@router.post("/predict")
async def predict(request: InferenceRequest):
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor, run_inference, request.model_name, request.text
        )
        return {"model": request.model_name, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
