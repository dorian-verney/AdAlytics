# from celery import Celery
# import os
# import ollama
# from pydantic import BaseModel
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Create Ollama client with Docker service host
# ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
# ollama_client = ollama.Client(host=ollama_host)
# logger.info(f"Ollama client configured with host: {ollama_host}")

# app = Celery(
#     'get_movie_info_llama', 
#     broker=os.getenv("CELERY_BROKER_URL"), 
#     backend=os.getenv("CELERY_BROKER_URL")
# )
# class Movie(BaseModel):
#     title: str
#     description: str
#     rating: float
#     year: int
#     genre: list[str]

# @app.task
# def get_movie_info_llama(prompt):
#     logger.info(f"Processing prompt: {prompt}")
    
#     stream = ollama_client.chat(
#         model="llama3.2:1b",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant that answers questions about movies. Respond with JSON only."},
#             {"role": "user", "content": f"{prompt} summarize the movie in 20 words or less"}
#         ],
#         stream=True,
#         options={
#             "num_predict": 150,  # Limit max tokens (faster generation)
#             "temperature": 0.7,  # Lower = faster, more deterministic
#             "num_ctx": 512,  # Smaller context window = faster
#             "num_thread": 4,  # Use more CPU threads
#         }
#     )
    
#     # Accumulate the full response from stream
#     full_content = ""
#     for chunk in stream:
#         if "message" in chunk and "content" in chunk["message"]:
#             content = chunk["message"]["content"]
#             full_content += content
    
#     logger.info(f"Response received ({full_content} chars)")
    
#     # Extract JSON if wrapped in text
#     import re
#     json_match = re.search(r'\{.*\}', full_content, re.DOTALL)
#     if json_match:
#         full_content = json_match.group(0)

#     return full_content
#     # Parse JSON response
#     movie = Movie.model_validate_json(full_content)
#     logger.info(f"Parsed movie: {movie}")
#     return movie.model_dump_json()