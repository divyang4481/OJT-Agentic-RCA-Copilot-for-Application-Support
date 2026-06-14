from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMProvider(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, context: str) -> Dict[str, Any]:
        """
        Generate a structured JSON response from the LLM based on prompt and context.
        """
        pass
