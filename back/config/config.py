from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATA_PATH = Path(__file__).parent.parent / "data"

# Model configuration from environment variables
MODEL_CONFIG = {
    "model_path": os.getenv("MODEL_PATH"),
    "n_ctx": 4096,
    "n_threads": 8
}
