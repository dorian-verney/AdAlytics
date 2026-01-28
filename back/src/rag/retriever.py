
def retrieve(collection, query_embedding: list[float], k: int = 4) -> dict:
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["distances", "documents", "metadatas"]
    )
    return results