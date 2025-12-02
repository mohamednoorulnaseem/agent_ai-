from abc import ABC, abstractmethod
from typing import List, Dict


class LLM(ABC):
    @abstractmethod
    def completion(self, messages: List[Dict[str, str]]) -> str:
        pass

