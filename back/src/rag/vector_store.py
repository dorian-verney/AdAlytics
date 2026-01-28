import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection(name="ad_knowledge")

def add_chunks(chunks, embeddings, metadata):
    for text, emb, meta in zip(chunks, embeddings, metadata):
        collection.add(
            documents=[text],
            embeddings=[emb],
            metadatas=[meta],
            ids=[meta["id"]]
        )