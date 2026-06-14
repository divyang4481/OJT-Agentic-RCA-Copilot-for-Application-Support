import os
from .base import LLMProvider
from .bedrock_client import BedrockClient
from .mock_client import MockClient
from .ollama_client import OllamaClient

def get_llm_provider() -> LLMProvider:
    provider = os.getenv("LLM_PROVIDER", "mock").lower()

    if provider == "bedrock":
        return BedrockClient()
    elif provider == "ollama-local":
        return OllamaClient()
    return MockClient()
