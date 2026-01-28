from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json

from .database.database import create_db_and_tables
from .routes import router

from back.config.config import MODEL_CONFIG
from llama_cpp import Llama

import asyncio

from back.src.rag.embedder import embed
from back.src.rag.retriever import retrieve
from back.src.rag.indexer import build_context
from back.src.rag.vector_store import collection
from back.src.core.scorer import score_ad
from back.src.core.critic import improve_ad


from typing import Generator

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)



llm = Llama(**MODEL_CONFIG)


def get_context(main_text: str) -> str:
    """
    Get the context for the ad by embedding the main text and 
    retrieving the most relevant chunks
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

@app.websocket("/api/ws")
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
                # TODO incorporate into context
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

if __name__ == "__main__":
    uvicorn.run("back.app.app:app", host="0.0.0.0", port=8000, reload=True)
