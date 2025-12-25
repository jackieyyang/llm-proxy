from abc import ABC, abstractmethod


class BaseAdapter(ABC):

    _registry: dict[str, type["BaseAdapter"]] = {}

    def __init__(self, **config) -> None:
        pass

    @classmethod
    def register(cls, name: str):
        def decorator(adapter_cls: type["BaseAdapter"]):
            cls._registry[name] = adapter_cls
            return adapter_cls
        return decorator

    @classmethod
    def create(cls, provider: str, **config) -> "BaseAdapter":
        try:
            return cls._registry[provider](**config)
        except KeyError:
            raise ValueError(f"Unsupported provider: {provider}")

    @abstractmethod
    async def chat_completion(self, messages, **kwargs) -> dict:
        pass