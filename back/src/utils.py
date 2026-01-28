import re
import json


def process_generated_text(generated_text: str, prompt: str) -> str:
    # Remove the prompt from the beginning, return only the generated part
    if generated_text.startswith(prompt):
        generated_text = generated_text[len(prompt):].strip()
    
    # # Clean up the text - remove markdown code blocks if present
    cleaned_text = generated_text.strip()
    if cleaned_text.startswith('```'):
        cleaned_text = re.sub(r'```(?:json)?\s*', '', cleaned_text, count=1)
        cleaned_text = re.sub(r'```\s*$', '', cleaned_text)
    
    # Try to find and extract JSON object
    # Find the first opening brace
    start_idx = cleaned_text.find('{')
    if start_idx == -1:
        return {"error": "No JSON found in output", "raw_output": generated_text}
    
    # Try to parse from the first brace, expanding until we get valid JSON
    for end_idx in range(len(cleaned_text), start_idx, -1):
        try:
            json_str = cleaned_text[start_idx:end_idx]
            return json.loads(json_str)
        except json.JSONDecodeError:
            continue
    
    # If all attempts fail, return error
    return {"error": "Failed to parse JSON", "raw_output": generated_text}