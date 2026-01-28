from typing import Dict, Type
from .base_llm import BaseModel


_REGISTRY: Dict[str, Type[BaseModel]] = {}

def register_model(model_id: str):
    def decorator(cls: Type[BaseModel]):
        _REGISTRY[model_id] = cls
        return cls
    return decorator

def create_model(model_id: str, **kwargs) -> BaseModel:
    if model_id not in _REGISTRY:
        raise KeyError(f"Unknown model: {model_id}")
    return _REGISTRY[model_id](**kwargs)

