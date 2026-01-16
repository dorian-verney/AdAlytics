# app/routers/inference.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from functools import lru_cache
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification
import asyncio

router = APIRouter()

class InferenceRequest(BaseModel):
    task: str
    text: str

# You can dynamically load models by name
AVAILABLE_MODELS = {
    # "summarization": ("summarization", "facebook/bart-large-cnn"),
    "text-generation": ("text-generation", "openai-community/gpt2"),
    "sentiment": ("text-classification", "tabularisai/multilingual-sentiment-analysis"),
}

TASKS_ARGS = {
    "text-generation": {
        "max_new_tokens": 50,
        "do_sample": True,
        "temperature": 0.7
    },
    "sentiment": {
        "return_all_scores": True
    },
}

@lru_cache(maxsize=3)
def get_pipeline(task: str):
    task_name, model_id = AVAILABLE_MODELS[task]

    # Load tokenizer from cache only
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        local_files_only=True
    )
    match task:
        case "text-generation":
            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                local_files_only=True
            )
        case "sentiment":
            model = AutoModelForSequenceClassification.from_pretrained(
                model_id,
                local_files_only=True
            )
        case _:
            raise ValueError(f"Unknown task: {task}")

    # Create pipeline with pre-loaded model and tokenizer
    pipe = pipeline(
        task_name,
        model=model,
        tokenizer=tokenizer
    )
    
    return pipe



async def predict(request: InferenceRequest):
    """Run all tasks in parallel and yield results as each finishes."""
    
    async def run_task(task: str):
        pipe = get_pipeline(task)
        print(f"Running inference for {task} ...")
        # run HF pipeline in thread because it's blocking
        result = await asyncio.to_thread(pipe, request.text, **TASKS_ARGS[task])
        return task, result

    # schedule all tasks concurrently
    tasks = [asyncio.create_task(run_task(task)) for task in AVAILABLE_MODELS]

    # as tasks finish, yield their results
    for finished_task in asyncio.as_completed(tasks):
        task_name, result = await finished_task
        yield task_name, result
