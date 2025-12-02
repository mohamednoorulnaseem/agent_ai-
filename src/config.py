import yaml
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm.base import LLM
from llm.ollama import Ollama
from llm.openai_like import OpenAILike
from llm.mock import MockLLM


def load_config_and_llm(config_file: str = "agent.config.yaml") -> tuple[dict, LLM]:
    """
    Load the configuration from the given file and initialize the LLM.
    """
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    llm_config = config.get("llm", {})
    provider = llm_config.get("provider")

    if provider == "ollama":
        llm = Ollama(
            model=llm_config.get("model"),
            api_base=llm_config.get("api_base"),
            temperature=llm_config.get("temperature", 0.0),
            top_p=llm_config.get("top_p", 1.0),
        )
    elif provider == "openai_like":
        llm = OpenAILike(
            model=llm_config.get("model"),
            api_base=llm_config.get("api_base"),
            api_key=llm_config.get("api_key"),
            temperature=llm_config.get("temperature", 0.0),
            top_p=llm_config.get("top_p", 1.0),
        )
    elif provider == "mock":
        llm = MockLLM()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    return config, llm
