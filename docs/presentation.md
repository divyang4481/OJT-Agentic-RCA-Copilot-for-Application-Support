# AWS Bedrock RCA Copilot: OJT Case Study Presentation

## 1. Executive Summary
The Bedrock RCA Copilot is an enterprise-style AI assistant built to drastically reduce the Mean Time To Resolution (MTTR) for application support teams. By unifying dual use cases—**TalkToAnyDoc** (RAG over Runbooks) and **Log Analyzer** (Log summarization)—this solution harnesses the power of Amazon Bedrock to autonomously perform Root Cause Analysis (RCA) and generate structured remediation steps with supporting evidence.

## 2. Problem Statement
Application support teams spend an excessive amount of time performing manual root cause analysis. During critical incidents (e.g., High CPU, 5xx errors), engineers must:
1. Sift through thousands of lines in raw log files.
2. Search disparate wikis or PDF runbooks for remediation steps.
3. Mentally correlate log anomalies with documented knowledge.
This manual process is slow, error-prone, and leads to extended downtime.

## 3. Solution / Approach
The Bedrock RCA Copilot automates the manual triage process using an Agentic AI workflow powered by Amazon Bedrock.
It enables support engineers to:
- Upload raw application logs (`.log`) to automatically identify the top recurring issues.
- Upload proprietary runbooks (`.pdf`, `.docx`, `.txt`, `.md`) to establish a Knowledge Base.
- Ask natural language questions (e.g., *"Why is service X showing high CPU?"*) and receive a structured RCA containing probable root cause, evidence, citations, remediation steps, and escalation recommendations.

## 4. Architecture
*(See `architecture.md` for visual diagrams)*
- **Frontend**: Streamlit for a responsive, interactive user interface.
- **Backend API**: Python FastAPI handling file validation, Log Analysis, and RAG operations.
- **LLM/Orchestration**: Amazon Bedrock (`Claude 3 Sonnet`) generates the RCA using prompt engineering and context injection.
- **Agentic Workflow**: Classifies the query, extracts log summaries via a tool, retrieves runbook chunks via local RAG, and synthesizes the findings.

## 5. Execution / Methods
- **Local First & Cloud Ready**: The application features a Mock LLM provider, allowing it to run completely offline without AWS credentials. By toggling the `LLM_PROVIDER` environment variable, it seamlessly connects to AWS Bedrock via `boto3`.
- **Validation**: Enforces strict file type constraints and a 100MB maximum file size to ensure stability and security.
- **Explainable AI**: The generated RCA includes direct citations (filenames and chunk references) to maintain trust and transparency.

## 6. Demo Flow
1. **Ingest Data**: Upload the sample `service_x_incident.log` and `service_x_runbook.md`.
2. **Log Analysis**: Click "Analyze Log for Top Issues" to extract the most frequent connection timeouts and rate limits.
3. **Ask the Agent**: Submit the incident query: *"Why is service X showing high CPU and 5xx errors?"*
4. **View RCA**: Observe the structured JSON-driven output displaying the root cause, remediation steps, and confidence score.

## 7. Results
- **Automated Triage**: What traditionally takes 15-30 minutes of log grepping is reduced to seconds.
- **Structured Outputs**: Support engineers receive actionable steps rather than generic conversational text.
- **High Evaluation Scores**: The evaluation script (`evals/run_eval.py`) verifies that answers contain citations, actionable remediation, and valid confidence scores (100% pass rate on sample datasets).

## 8. Unit Test Summary
- Comprehensive test coverage using `pytest` located in `tests/test_backend.py`.
- **Log Analyzer**: Verified correct extraction and counting of top recurring errors.
- **Local RAG**: Verified accurate document chunking and retrieval based on keyword overlap.
- **Agent Workflow**: Verified that the RCA Agent returns the expected structured schema (Probable Cause, Confidence, Remediation).

## 9. Conclusion
The Bedrock RCA Copilot effectively demonstrates deep knowledge of AWS Bedrock capabilities, RAG architectural patterns, and practical enterprise use cases. It transitions a traditionally reactive support process into a proactive, AI-assisted workflow.

## 10. Future Scope
- **Bedrock Knowledge Bases**: Replace the local RAG simulation with a fully managed Amazon Bedrock Knowledge Base and OpenSearch Serverless vector store.
- **Guardrails for Amazon Bedrock**: Implement custom guardrails to block PII/PHI in logs and enforce grounded responses.
- **Automated Ticketing**: Extend the agent action group to automatically create Jira or ServiceNow tickets.
