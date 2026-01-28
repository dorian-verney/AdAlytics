def build_context(results: dict) -> str:
    context = ""
    for i, doc in enumerate(results["documents"][0]):
        source = results["metadatas"][0][i]["source"]
        context += f"[{i+1}] {doc}\n(Source: {source})\n\n"
    return context