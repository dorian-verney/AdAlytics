from abc import ABC, abstractmethod
from typing import Any, Generator
from back.src.utils import process_generated_text

class BaseModel(ABC):
    model_id: str  # e.g. "scorer_v1", "critic_v1", "embedder_minilm"
    streaming: bool = False
    @abstractmethod
    def load(self) -> None:
        """Load weights / init client. No-op if already loaded."""
        pass

    @abstractmethod
    def is_loaded(self) -> bool:
        pass

    @abstractmethod
    def predict(self, *args, **kwargs) -> Any:
        """Sync inference."""
        pass

    def stream(self, *args, **kwargs) -> Generator[Any, None, None]:
        """Optional; default to wrapping predict."""
        # Buffer all tokens and track progress
        generated_text = ""
        token_count = 0
        for token in self.predict(*args, **kwargs):
            print(token)
            token_text = token["choices"][0]["text"]
            generated_text += token_text
            token_count += 1

            progress = min(int((token_count / self.max_tokens) * 100), 99)  
            
            yield None, progress  
        
        # When complete, parse and return the parsed JSON
        parsed_result = process_generated_text(generated_text, self.prompt)
        yield parsed_result, 100  # Final result with 100% progress