from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Set
import asyncio
import json
import uuid
from routers import inference_v1


server = FastAPI()
server.include_router(inference_v1.router, prefix="/api", tags=["inference"])

# Add CORS middleware
server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Store text inputs in memory
text_sentiment: List[dict] = []


class TextInputRequest(BaseModel):
    text: str
    additional_context: str = ""


@server.get("/api")
def root():
    return {"message": "Hello, World!"}


def predict(text: str):
    # Example: simple sentiment
    return {"sentiment": "positive" if "good" in text.lower() else "negative"}


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
            # Wait for messages from this client
            data = await websocket.receive_text()
            message = json.loads(data)
            print("Received message: ", message)
            text = message.get("text", "")
            additional_context = message.get("additional_context", "")

            inference_request = inference_v1.InferenceRequest(
                task="sentiment",
                text=text
            )
            prediction_response = inference_v1.predict(inference_request)

            
            # Send back prediction to the same client
            await websocket.send_text(json.dumps({
                "prediction": prediction_response
            }))
            print("Sent prediction to client ", prediction_response)
    except WebSocketDisconnect:
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass

