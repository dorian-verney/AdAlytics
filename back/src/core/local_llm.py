from .base_llm import BaseModel
from .scorer import score_ad
from llama_cpp import Llama
from .model_factory import register_model
from typing import Optional



class LazyScorer(BaseModel):
    def __init__(self, model_path: str):
        self._path = model_path
        self._llm: Optional[Llama] = None

    def load(self):
        if self._llm is None:
            self._llm = Llama(self._path, n_ctx=4096)

    def is_loaded(self):
        return self._llm is not None

    def predict(self, ad_text: str, context: str, **kwargs):
        self.load()
        return next(score_ad(self._llm, ad_text, context))[0]


@register_model("scorer_v1")
class ScorerV1(BaseModel):
    model_id = "scorer_v1"
    def __init__(self, model_path: str, n_ctx: int = 4096):
        self._llm = None
        self._path, self._n_ctx = model_path, n_ctx

    def load(self):
        self._llm = Llama(self._path, n_ctx=self._n_ctx)

    def is_loaded(self):
        return self._llm is not None

    def predict(self, ad_text: str, context: str, **kwargs):
        return next(score_ad(self._llm, ad_text, context))[0]