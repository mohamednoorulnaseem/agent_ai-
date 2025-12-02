import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from typing import List, Dict, Any

from llm.base import LLM


class Ollama(LLM):
    def __init__(self, model: str, api_base: str, temperature: float = 0.0, top_p: float = 1.0):
        self.model = model
        self.api_base = api_base
        self.temperature = temperature
        self.top_p = top_p

    def completion(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        """
        Generate a completion using the Ollama API.
        """
        data = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
        }
        response = requests.post(f"{self.api_base}/chat", json=data)
        response.raise_for_status()
        return response.json()["message"]["content"]

