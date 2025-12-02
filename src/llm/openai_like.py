import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Any

import openai

from llm.base import LLM


class OpenAILike(LLM):
    def __init__(self, model: str, api_base: str, api_key: str, temperature: float = 0.0, top_p: float = 1.0):
        self.model = model
        self.api_base = api_base
        self.api_key = api_key
        self.temperature = temperature
        self.top_p = top_p
        if not self.api_key:
            # get from env
            self.api_key = os.environ.get("OPENAI_API_KEY")

    def completion(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        """
        Generate a completion using the OpenAI-like API.
        """
        client = openai.OpenAI(api_key=self.api_key, base_url=self.api_base)
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p,
        )
        return response.choices[0].message.content

