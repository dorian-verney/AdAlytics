def chunk_text(text: str, size: int = 20, overlap: int = 10) -> list[str]:
    words = text.split()
    chunks = []

    for i in range(0, len(words), size - overlap):
        chunk = " ".join(words[i:i+size])
        chunks.append(chunk)

    return chunks


