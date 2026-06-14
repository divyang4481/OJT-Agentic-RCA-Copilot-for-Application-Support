import json

eval_data = [
    {
        "query": "Why is service X showing high CPU and 5xx errors?",
        "log_filename": "service_x_incident.log",
        "expected_keywords_in_rca": ["memory", "leak", "exhaustion", "spike"],
        "expected_remediation": ["restart", "scale"],
        "expected_escalation": "L3 Backend Engineering Team"
    },
    {
        "query": "What are the recurring database issues?",
        "log_filename": "service_x_incident.log",
        "expected_keywords_in_rca": ["ConnectionTimeoutError", "db_pool"],
        "expected_remediation": [],
        "expected_escalation": ""
    }
]

with open("evals/rca_eval_dataset.json", "w") as f:
    json.dump(eval_data, f, indent=4)
