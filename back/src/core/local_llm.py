from .base_llm import BaseModel
from llama_cpp import Llama
from .model_factory import register_model
from back.src.prompts.prompts import score_prompt
from back.src.utils import process_generated_text


@register_model("scorer_v1")
class ScorerV1(BaseModel):
    model_id = "scorer_v1"
    def __init__(self, model_path: str, n_ctx: int = 4096):
        self._llm = None
        self._path, self._n_ctx = model_path, n_ctx
        self.max_tokens = 200

    def load(self):
        self._llm = Llama(self._path, n_ctx=self._n_ctx)

    def is_loaded(self):
        return self._llm is not None

    def predict(self, ad_text: str, context: str, **kwargs):
        self.prompt = score_prompt(context, ad_text)
        stream = True
        output = self._llm(
            self.prompt,
            max_tokens=self.max_tokens,
            temperature=0.2,
            stream=stream      # Enable streaming to track progress
        )
        if stream:
            yield from output
        else:
            return process_generated_text(output, self.prompt)

    def stream(self, ad_text: str, context: str, **kwargs):
        # Buffer all tokens and track progress
        generated_text = ""
        token_count = 0
        for token in self.predict(ad_text, context, **kwargs):
            print(token)
            token_text = token["choices"][0]["text"]
            generated_text += token_text
            token_count += 1

            progress = min(int((token_count / self.max_tokens) * 100), 99)  
            
            yield None, progress  
        
        # When complete, parse and return the parsed JSON
        parsed_result = process_generated_text(generated_text, self.prompt)
        yield parsed_result, 100  # Final result with 100% progress


@register_model("critic_v1")
class CriticV1(BaseModel):
    model_id = "critic_v1"
    def __init__(self, model_path: str, n_ctx: int = 4096):
        self._llm = None
        self._path, self._n_ctx = model_path, n_ctx
        self.max_tokens = 500

    def load(self):
        self._llm = Llama(self._path, n_ctx=self._n_ctx)

    def is_loaded(self):
        return self._llm is not None

    def predict(self, ad_text: str, scores: str, context: str, **kwargs):
        self.prompt = score_prompt(context, ad_text)
        stream = True
        output = self._llm(
            self.prompt,
            max_tokens=self.max_tokens,
            temperature=0.3,
            stream=stream      # Enable streaming to track progress
        )
        if stream:
            yield from output
        else:
            return process_generated_text(output, self.prompt)


    def stream(self, ad_text: str, scores: str, context: str, **kwargs):
        # Buffer all tokens and track progress
        generated_text = ""
        token_count = 0
        
        for token in self.predict(ad_text, scores, context, **kwargs):
            token_text = token["choices"][0]["text"]
            generated_text += token_text
            token_count += 1
        
            progress = min(int((token_count / self.max_tokens) * 100), 99) 
            # Yield progress updates
            yield None, progress  
        
        # When complete, parse and return the parsed JSON
        parsed_result = process_generated_text(generated_text, self.prompt)
        yield parsed_result, 100  # Final result with 100% progress


