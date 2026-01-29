import json
import time

from back.src.rag.embedder import embed
from back.src.rag.retriever import retrieve
from back.src.rag.indexer import build_context
from back.src.rag.vector_store import collection
from back.src.utils import process_llm_output
from back.src.rag.populate_db import ensure_vector_store_populated
from back.src.prompts.prompts import score_prompt, improve_prompt

class Pipeline:
    def __init__(self, scorer_llm, critic_llm):
        self.scorer_llm = scorer_llm
        self.critic_llm = critic_llm
        self.main_text = None
        self.additional_context = None

        ensure_vector_store_populated(collection)

    def ingest(self, main_text: str, additional_context: str):
        self.main_text = main_text
        self.additional_context = additional_context


    def build_context(self):
        query_emb = embed([self.main_text])[0].tolist()
        results = retrieve(collection, query_emb)
        context = build_context(results)
        return context

    def run(self):
        context = self.build_context()
        # Scorer: predict (non-streaming) -> raw dict
        prompt_scorer = score_prompt(context, self.main_text)
        time_start = time.time()
        out = self.scorer_llm.predict(prompt_scorer)
        # Critic: predict (non-streaming)
        out = next(out)
        out = process_llm_output(out, prompt_scorer)
        yield json.dumps({"stage": "scorer", "result": out})

        prompt_critic = improve_prompt(context, self.main_text, out)
        out2 = self.critic_llm.predict(prompt_critic)
        out2 = next(out2)
        out2 = process_llm_output(out2, prompt_critic)
        yield json.dumps({"stage": "critic", "result": out2})
        time_end = time.time()
        print(f"Time taken: {time_end - time_start} seconds")
