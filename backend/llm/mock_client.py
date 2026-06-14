from typing import Dict, Any
from .base import LLMProvider

class MockClient(LLMProvider):
    def __init__(self):
        pass

    def generate_response(self, prompt: str, context: str) -> Dict[str, Any]:
        """
        Mock response generator for local execution without AWS credentials.
        """
        is_cpu_issue = "cpu" in prompt.lower() or "5xx" in prompt.lower()
        is_log_issue = "recurring" in prompt.lower() or "log" in prompt.lower()

        if is_cpu_issue:
            return {
                "probable_root_cause": "Service is experiencing high CPU utilization likely due to a memory leak or sudden traffic spike, leading to 5xx HTTP errors.",
                "evidence": [
                    "User reported High CPU and 5xx errors.",
                    "Context indicates possible resource exhaustion."
                ],
                "remediation_steps": [
                    "Restart the affected service instances.",
                    "Scale up the compute resources in the autoscaling group.",
                    "Investigate recent deployments for memory leaks."
                ],
                "confidence": "High",
                "escalation_recommendation": "L3 Backend Engineering Team"
            }
        elif is_log_issue:
             return {
                "probable_root_cause": "Database connection timeouts and API rate limiting are the top recurring errors.",
                "evidence": [
                    "Logs show repeated 'ConnectionTimeoutError' at db_pool.",
                    "Logs show repeated '429 Too Many Requests' from external API."
                ],
                "remediation_steps": [
                    "Increase database connection pool size.",
                    "Implement exponential backoff for external API calls."
                ],
                "confidence": "Medium",
                "escalation_recommendation": "DBA Team"
            }
        else:
            return {
                "probable_root_cause": "Generic issue detected based on user query.",
                "evidence": ["Query: " + prompt],
                "remediation_steps": ["Review system health dashboards.", "Check application logs."],
                "confidence": "Low",
                "escalation_recommendation": "L2 Support"
            }
