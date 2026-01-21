import os

from config.config import DATA_PATH
from .loader import load_pdf
from .chunker import chunk_text
from .embedder import embed
from rag.rag_core.vector_store import add_chunks


def populate_vector_store():
    pdf_name = "shampoo-ad.pdf"
    pages = load_pdf(os.path.join(DATA_PATH, pdf_name))
    full_text = "\n\n".join(pages)
    chunks = chunk_text(full_text)
    embeddings = embed(chunks).tolist()
    metadata = [{"id": f"chunk_{i}", "source": pdf_name} for i in range(len(chunks))]
    add_chunks(chunks, embeddings, metadata)