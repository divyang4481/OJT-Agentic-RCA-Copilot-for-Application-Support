import json
import sys
import os

# Ensure backend can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.agent.rca_agent import rca_agent

def run_evaluations():
    with open("evals/rca_eval_dataset.json", "r") as f:
        dataset = json.load(f)

    total_score = 0
    max_score = len(dataset) * 3  # 3 checks per question: citation, remediation, confidence

    print("Starting Evaluation Run...\n" + "="*40)

    for i, item in enumerate(dataset):
        print(f"Evaluating Question {i+1}: {item['query']}")

        try:
            response = rca_agent.generate_rca(query=item['query'], log_filename=item.get('log_filename'))

            score = 0
            # Check 1: Citations exist
            citations = response.get("citations", [])
            if len(citations) > 0:
                score += 1

            # Check 2: Remediation exists
            remediation = response.get("remediation_steps", [])
            if remediation and len(remediation) > 0:
                score += 1

            # Check 3: Confidence exists
            confidence = response.get("confidence", "")
            if confidence in ["High", "Medium", "Low"]:
                score += 1

            total_score += score
            print(f"Score: {score}/3")
            print(f"Probable Cause snippet: {response.get('probable_root_cause', '')[:100]}...\n")
        except Exception as e:
            print(f"Error evaluating question {i+1}: {e}\n")

    print("="*40)
    print(f"Final Evaluation Score: {total_score}/{max_score}")

if __name__ == "__main__":
    run_evaluations()
