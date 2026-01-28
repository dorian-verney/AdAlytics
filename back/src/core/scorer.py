from back.src.utils import  process_generated_text
from llama_cpp import Llama
from typing import Generator
from back.src.prompts.prompts import score_prompt

def score_ad(llm: Llama, ad_text: str, context: str) -> Generator[str, int]:
    prompt = score_prompt(context, ad_text)
    
    print("longueur du prompt = ", len(prompt))
    max_tokens = 200
    output = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=0.2,
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
        
        yield None, progress  
    
    # When complete, parse and return the parsed JSON
    parsed_result = process_generated_text(generated_text, prompt)
    yield parsed_result, 100  # Final result with 100% progress