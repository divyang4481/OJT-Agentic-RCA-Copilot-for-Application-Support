import os
from collections import Counter
import re
from typing import List, Dict, Any

class LogAnalyzer:
    def __init__(self, logs_dir: str = "sample_data/incidents"):
        self.logs_dir = logs_dir
        os.makedirs(self.logs_dir, exist_ok=True)

    def analyze_logs(self, filename: str) -> Dict[str, Any]:
        """
        Analyzes a given log file and returns the top 3 recurring issues/errors.
        """
        filepath = os.path.join(self.logs_dir, filename)
        if not os.path.exists(filepath):
            return {"error": f"Log file {filename} not found."}

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            return {"error": f"Error reading log file: {e}"}

        errors = []
        # Simple extraction logic looking for ERROR or Exception
        for line in lines:
            if "ERROR" in line or "Exception" in line or "500" in line or "timeout" in line.lower() or "5xx" in line:
                # Strip out timestamps or generic prefix for better counting (very naive approach)
                # e.g., "2023-10-27 10:00:00 ERROR: ConnectionTimeoutError in db_pool"
                match = re.search(r'(ERROR|Exception|500|timeout|5xx)[:\-]?\s*(.*)', line, re.IGNORECASE)
                if match:
                    errors.append(match.group(2).strip())
                else:
                    errors.append(line.strip())

        if not errors:
            return {
                "summary": "No explicit errors found in log file.",
                "top_issues": []
            }

        counter = Counter(errors)
        top_3 = counter.most_common(3)

        return {
            "summary": f"Found {len(errors)} error instances in {filename}.",
            "top_issues": [{"issue": issue, "count": count} for issue, count in top_3]
        }

log_analyzer = LogAnalyzer()
