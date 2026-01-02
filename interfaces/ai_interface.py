from abc import ABC, abstractmethod

class AIServiceInterface(ABC):
    @abstractmethod
    def process_query(self, query: str, system_prompt: str):
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass
