import json
import boto3
import os
from typing import Dict, Any
from .base import LLMProvider

class BedrockClient(LLMProvider):
    def __init__(self):
        region = os.getenv("AWS_REGION", "us-east-1")
        self.model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")

        # Boto3 uses standard credential resolution (env vars, IAM, config file)
        # We do not hardcode credentials here.
        self.client = boto3.client("bedrock-runtime", region_name=region)

    def generate_response(self, prompt: str, context: str) -> Dict[str, Any]:
        """
        Calls AWS Bedrock with Claude 3 Sonnet (or configured model) to generate an RCA JSON response.
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

        user_message = f"""
        Context:
        {context}

        Incident Question:
        {prompt}
        """

        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.0
        }

        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body),
                contentType="application/json",
                accept="application/json"
            )

            response_body = json.loads(response.get('body').read())
            completion = response_body.get('content', [])[0].get('text', '')

            # Clean completion in case the model wraps JSON in markdown blocks
            completion = completion.replace("```json", "").replace("```", "").strip()

            return json.loads(completion)

        except Exception as e:
            # Fallback or pass error to the backend
            return {
                "probable_root_cause": "Error calling Bedrock LLM.",
                "evidence": [str(e)],
                "remediation_steps": ["Check AWS credentials and model access."],
                "confidence": "None",
                "escalation_recommendation": "Cloud Admin"
            }
