import os

from back.config.config import DATA_PATH
from .loader import load_pdf
from back.src.preprocessing.chunker import chunk_text
from .embedder import embed
from .vector_store import add_chunks


def populate_vector_store():
    pdf_name = "shampoo-ad.pdf"
    pages = load_pdf(os.path.join(DATA_PATH, pdf_name))
    full_text = "\n\n".join(pages)
    chunks = chunk_text(full_text)
    embeddings = embed(chunks).tolist()
    metadata = [{"id": f"chunk_{i}", "source": pdf_name} for i in range(len(chunks))]
    add_chunks(chunks, embeddings, metadata)


def ensure_vector_store_populated(collection):
    """
    Check if collection is empty and populate it with ad.pdf if needed
    """
    count = collection.count()
    if count == 0:
        populate_vector_store()
        print(f"Added chunks to vector store.")
    else:
        print(f"Vector store already populated with {count} documents.")