from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
from typing import Generator
from llama_cpp import Llama

from rag.ingest.embedder import embed
from rag.rag_core.retriever import retrieve
from rag.rag_core.prompt_builder import build_context
from rag.rag_core.vector_store import collection
from rag.models.scorer import score_ad
from rag.models.critic import improve_ad
from rag.ingest.populate_db import populate_vector_store

from config.config import MODEL_CONFIG

llm = Llama(**MODEL_CONFIG)

server = FastAPI()

# Add CORS middleware
# CORS (Cross-Origin Resource Sharing) allows the frontend (running on different port/domain)
# to make requests to this API. Without it, browsers block cross-origin requests.
server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Allows ALL origins - OK for dev, but SECURITY RISK in production!
    allow_methods=["*"],     # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],     # Allows all request headers
)


class AdRequest(BaseModel):
    main_text: str
    additional_context: str = ""


def ensure_vector_store_populated():
    """
    Check if collection is empty and populate it with ad.pdf if needed
    """
    count = collection.count()
    if count == 0:
        populate_vector_store()
        print(f"Added chunks to vector store.")
    else:
        print(f"Vector store already populated with {count} documents.")


@server.on_event("startup")
async def startup_event():
    ensure_vector_store_populated()


@server.get("/api")
def root():
    return {"message": "Hello, everything is working!"}


def evaluate_ad(request: AdRequest) -> dict:
    """
    Evaluate the ad and return the scores and feedback
    """
    main_text = request.main_text
    additional_context = request.additional_context # TODO incorporate into context
    query_emb = embed([main_text])[0].tolist()
    results = retrieve(collection, query_emb)
    context = build_context(results)
    scores = score_ad(llm, main_text, context)
    feedback = improve_ad(llm, main_text, scores, context)
    return {"scores": scores, "feedback": feedback}


def get_context(main_text: str) -> str:
    """
    Get the context for the ad
    """
    query_emb = embed([main_text])[0].tolist()
    results = retrieve(collection, query_emb)
    context = build_context(results)
    return context


async def token_progress_stream(llm: Llama, main_text: str, context: str) -> Generator[str, int]:
    """
    Token and progress stream that handles the scoring and feedback
    First phase, the scorer yield scores and progress
    Then the critic yields suggestions and progress
    """
    # PHASE 1: The Scorer (generates scores and justification) ---
    scores_result = None
    for result, progress in score_ad(llm, main_text, context):
        if result is None:
            # This is just a progress update
            yield json.dumps({"stage": "scorer", "progress": progress})
        else:
            # This is the final parsed result
            scores_result = result
            yield json.dumps({"stage": "scorer", "result": result, "progress": 100})
        # Yield control to event loop so websocket sends happen immediately
        await asyncio.sleep(0)

    # PHASE 2: The Critic (generates suggestions and new_ad) ---
    # Convert scores_result dict to string for the prompt
    scores_str = json.dumps(scores_result) if scores_result else "{}"
    for result, progress in improve_ad(llm, main_text, scores_str, context):
        if result is None:
            # This is just a progress update
            yield json.dumps({"stage": "critic", "progress": progress})
        else:
            # This is the final parsed result
            yield json.dumps({"stage": "critic", "result": result, "progress": 100})
        # Yield control to event loop so websocket sends happen immediately
        await asyncio.sleep(0)


@server.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that handles bidirectional communication.
    Clients send messages and receive predictions on the same connection.
    """
    await websocket.accept()
    print("WebSocket client connected")

    try:
        while True:
            try:
                # Wait for messages from this client
                data = await websocket.receive_text()
                message = json.loads(data)

                main_text = message.get("main_text", "")
                additional_context = message.get("additional_context", "")

                context = get_context(main_text)

                async for data in token_progress_stream(llm, main_text, context):
                    await websocket.send_text(data)
            
            except Exception as e:
                print(f"Error processing message: {e}")
                import traceback
                traceback.print_exc()
                # Send error back to client but keep connection open
                await websocket.send_text(json.dumps({
                    "error": "Error processing request",
                    "details": str(e)
                }))
    except WebSocketDisconnect:
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"WebSocket connection error: {e}")
        import traceback
        traceback.print_exc()
        try:
            await websocket.close()
        except:
            pass

