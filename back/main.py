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
                print("Received message: ", message)
                text = message.get("text", "")
                additional_context = message.get("additional_context", "")

                inference_request = inference_v1.InferenceRequest(
                    task="sentiment",
                    text=text + " " + additional_context # TODO: change for more realistic context
                )
                async for task_name, result in inference_v1.predict(inference_request):
                    print("Sending prediction to client IN ORDERRRRR", task_name)
                    await websocket.send_text(json.dumps({
                        "task": task_name,
                        "result": result
                    }))
                    print("Sent prediction to client ", task_name, result)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON message: {e}")
                await websocket.send_text(json.dumps({
                    "error": "Invalid JSON format",
                    "details": str(e)
                }))
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

