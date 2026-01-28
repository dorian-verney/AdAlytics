from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATA_PATH = Path(__file__).parent.parent / "data"

# Model configuration from environment variables
MODEL_CONFIG = {
    "model_path": os.getenv("MODEL_PATH"),
    "n_ctx": 4096
    # "n_threads": 8
}

MODEL_ROUTING = {
    "scorer": os.getenv("SCORER_MODEL", "scorer_v1"),
    "critic": os.getenv("CRITIC_MODEL", "critic_v1"),
    "embedder": os.getenv("EMBEDDER_MODEL", "embedder_minilm"),
}

# def get_model_for_role(role: str) -> BaseModel:
#     model_id = MODEL_ROUTING[role]
#     return get_model(model_id)