from abc import ABC, abstractmethod
from typing import Any, Generator

class BaseModel(ABC):
    model_id: str  # e.g. "scorer_v1", "critic_v1", "embedder_minilm"

    @abstractmethod
    def load(self) -> None:
        """Load weights / init client. No-op if already loaded."""
        pass

    @abstractmethod
    def is_loaded(self) -> bool:
        pass

    @abstractmethod
    def predict(self, **kwargs) -> Any:
        """Sync inference."""
        pass

    def stream(self, **kwargs) -> Generator[Any, None, None]:
        """Optional; default to wrapping predict."""
        raise NotImplementedError