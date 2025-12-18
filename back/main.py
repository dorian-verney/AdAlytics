from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Set
import asyncio
import json
from routers import inference_v1


server = FastAPI()
server.include_router(inference_v1.router, prefix="/api", tags=["inference"])


# Store text inputs in memory
text_sentiment: List[dict] = []


class TextInputRequest(BaseModel):
    text: str
    additional_context: str = ""


@server.get("/api")
def root():
    return {"message": "Hello, World!"}






# Store queues for all connected SSE clients
sse_queues: Set[asyncio.Queue] = set()

@server.post("/api/stream")
async def receive_stream(request: TextInputRequest):
    # Use inference_v1 predict function to get prediction
    print("request", request)
    try:
        inference_request = inference_v1.InferenceRequest(
            task="sentiment",
            text=request.text
        )
        prediction_response = inference_v1.predict(inference_request)
        
        # Combine input data with prediction results
        new_data = {
            "text": request.text,
            "additional_context": request.additional_context,
            "prediction": prediction_response
        }
        print("yessssssss", new_data)
    except Exception as e:
        # Handle errors gracefully
        new_data = {
            "text": request.text,
            "additional_context": request.additional_context,
            "error": str(e)
        }
    
    print(new_data)
    text_sentiment.append(new_data)
    
    # Send event to all connected SSE clients
    for queue in sse_queues.copy():
        try:
            await queue.put(new_data)
        except Exception as e:
            # Remove dead connections
            sse_queues.discard(queue)
    
    return {
        "status": "success",
        "message": "Text received successfully"
    }


@server.get("/api/stream")
async def stream_main_input():
    async def event_generator():
        # Create a queue for this client
        queue = asyncio.Queue()
        sse_queues.add(queue)
        
        try:
            # Send initial data if available
            if text_sentiment:
                initial_data = text_sentiment[-1]
                yield f"data: {json.dumps(initial_data)}\n\n"
            
            # Keep connection open and send updates
            while True:
                try:
                    # Wait for new data with timeout
                    data = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield f"data: {json.dumps(data)}\n\n"
                except asyncio.TimeoutError:
                    # Send a keepalive comment
                    yield ": keepalive\n\n"
        finally:
            # Clean up when client disconnects
            sse_queues.discard(queue)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )