from rag.utils import process_generated_text
from llama_cpp import Llama
from typing import Generator

def improve_ad(llm: Llama, ad_text: str, scores: str, context: str) -> Generator[str, int]:
    prompt = f"""
                You are a marketing consultant.
                Use the context and scores to improve the ad:
                1. Suggest 3 improvements as suggestions
                2. Rewrite the ad as a new_ad
                Return JSON.

                Context:
                {context}

                Scores:
                {scores}

                Ad:
                {ad_text}

                Output format:
                {{
                    "suggestions": ["...", "...", "..."],
                    "new_ad": "..."
                }}
                

                """

    max_tokens = 500
    output = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=0.3,
        stream=True      # Enable streaming to track progress
    )
    
    # Buffer all tokens and track progress
    generated_text = ""
    token_count = 0
    
    for token in output:
        token_text = token["choices"][0]["text"]
        generated_text += token_text
        token_count += 1
       
        progress = min(int((token_count / max_tokens) * 100), 99) 
        # Yield progress updates
        yield None, progress  
    
    # When complete, parse and return the parsed JSON
    parsed_result = process_generated_text(generated_text, prompt)
    yield parsed_result, 100  # Final result with 100% progress