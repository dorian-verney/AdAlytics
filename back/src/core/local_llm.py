from .base_llm import BaseModel
from llama_cpp import Llama
from .model_factory import register_model


@register_model("scorer_v1")
class ScorerV1(BaseModel):
    model_id = "scorer_v1"
    def __init__(self, model_path: str, n_ctx: int = 4096, n_threads: int = 4):
        self._llm = None
        self._path = model_path
        self._n_ctx = n_ctx
        self._n_threads = n_threads
        self.max_tokens = 200
        self.temperature = 0.2

    def load(self):
        self._llm = Llama(self._path, 
                          n_ctx=self._n_ctx, 
                          n_threads=self._n_threads)

    def is_loaded(self):
        return self._llm is not None

    def predict(self, prompt: str, **kwargs):
        output = self._llm(
            prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stream=self.streaming
        )
        if self.streaming:
            yield from output
        else:
            yield output



@register_model("critic_v1")
class CriticV1(BaseModel):
    model_id = "critic_v1"
    def __init__(self, model_path: str, n_ctx: int = 4096, n_threads: int = 4):
        self._llm = None
        self._path = model_path
        self._n_ctx = n_ctx
        self._n_threads = n_threads
        self.max_tokens = 200
        self.temperature = 0.3

    def load(self):
        self._llm = Llama(self._path, 
                          n_ctx=self._n_ctx, 
                          n_threads=self._n_threads)

    def is_loaded(self):
        return self._llm is not None

    def predict(self, prompt: str, **kwargs):
        output = self._llm(
            prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stream=self.streaming,
        )
        if self.streaming:
            yield from output
        else:
            yield output

