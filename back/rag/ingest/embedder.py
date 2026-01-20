from sentence_transformers import SentenceTransformer
from numpy import ndarray
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'

def embed(texts: list[str], model_name: str = MODEL_NAME) -> ndarray:
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts)
    return embeddings