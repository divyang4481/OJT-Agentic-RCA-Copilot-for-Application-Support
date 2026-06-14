import os
import json
import requests
from typing import Dict, Any
from .base import LLMProvider

class OllamaClient(LLMProvider):
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/api/generate")
        self.model_id = os.getenv("OLLAMA_MODEL_ID", "llama3")

    def generate_response(self, prompt: str, context: str) -> Dict[str, Any]:
        """
        Calls local Ollama model to generate an RCA JSON response.
        """
        system_prompt = """
        You are an expert Application Support Engineer performing a Root Cause Analysis (RCA).
        You will be provided with context from logs or runbooks and a user incident question.
        Analyze the provided context and respond strictly in valid JSON format with the following keys:
        - "probable_root_cause": string (the likely issue)
        - "evidence": list of strings (supporting details from the context)
        - "remediation_steps": list of strings (how to fix it)
        - "confidence": string (High, Medium, or Low)
        - "escalation_recommendation": string (who to escalate to, if necessary)
        """

        full_prompt = f"""{system_prompt}

Context:
{context}

Incident Question:
{prompt}
"""

        payload = {
            "model": self.model_id,
            "prompt": full_prompt,
            "format": "json",
            "stream": False,
            "options": {
                "temperature": 0.0
            }
        }

        try:
            response = requests.post(self.base_url, json=payload, timeout=60)
            response.raise_for_status()

            response_data = response.json()
            completion = response_data.get("response", "")

            # Clean completion in case the model wraps JSON in markdown blocks
            completion = completion.replace("```json", "").replace("```", "").strip()

            return json.loads(completion)

        except Exception as e:
            return {
                "probable_root_cause": "Error calling local Ollama LLM.",
                "evidence": [str(e)],
                "remediation_steps": ["Check if Ollama is running and the model is pulled."],
                "confidence": "None",
                "escalation_recommendation": "Local Dev"
            }
