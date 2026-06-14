import pytest
import os
from backend.rag.local_rag import LocalRAG
from backend.tools.log_analyzer import LogAnalyzer
from backend.agent.rca_agent import rca_agent

def test_log_analyzer():
    # Setup test log
    os.makedirs("tests/test_data", exist_ok=True)
    with open("tests/test_data/test.log", "w") as f:
        f.write("ERROR: timeout\nERROR: timeout\nERROR: 500 error\n")

    analyzer = LogAnalyzer(logs_dir="tests/test_data")
    result = analyzer.analyze_logs("test.log")

    assert "summary" in result
    assert len(result["top_issues"]) == 2
    assert result["top_issues"][0]["issue"] == "timeout"
    assert result["top_issues"][0]["count"] == 2

    # Cleanup
    os.remove("tests/test_data/test.log")

def test_local_rag():
    os.makedirs("tests/test_data/runbooks", exist_ok=True)
    with open("tests/test_data/runbooks/test.txt", "w") as f:
        f.write("This is a test runbook covering high cpu and memory leaks.\n\nEscalate to L3 if needed.")

    rag = LocalRAG(doc_dir="tests/test_data/runbooks")
    results = rag.retrieve("high cpu leak")

    assert len(results) > 0
    assert "test.txt" in results[0]["source"]

    os.remove("tests/test_data/runbooks/test.txt")

def test_rca_agent_mock():
    # Since LLM_PROVIDER=mock is default, this will use the mock
    response = rca_agent.generate_rca("high cpu and 5xx errors")

    assert "probable_root_cause" in response
    assert "confidence" in response
    assert "citations" in response
    assert "remediation_steps" in response
