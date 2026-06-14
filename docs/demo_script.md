# Demo Script: Bedrock RCA Copilot

Use this script to record a video proof or perform a live demonstration for the OJT.

## Prerequisites
Ensure the application is running locally:
1. Terminal 1: `uvicorn backend.main:app --reload --port 8000`
2. Terminal 2: `streamlit run frontend/app.py`
3. Have the `sample_data/runbooks/service_x_runbook.md` and `sample_data/incidents/service_x_incident.log` files ready on your desktop.

## Step-by-Step Flow

### 1. Introduction (0:00 - 0:30)
- **Action**: Show the Streamlit home page.
- **Talking Point**: *"Hello, today I will demonstrate the Bedrock RCA Copilot. This tool merges two enterprise use cases: 'Talk To Any Doc' and 'Log Analyzer'. It is designed to help support engineers perform rapid Root Cause Analysis using Amazon Bedrock."*

### 2. Log Analysis (0:30 - 1:15)
- **Action**: Use the sidebar to upload `service_x_incident.log`.
- **Action**: Once uploaded, click the **"Analyze Log for Top Issues"** button in the sidebar.
- **Talking Point**: *"First, we upload an incident log. Instead of manually grepping through thousands of lines, the Log Analyzer extracts the top recurring issues—in this case, Connection Timeouts and Rate Limits."*

### 3. Knowledge Base Ingestion / RAG (1:15 - 1:45)
- **Action**: Use the sidebar to upload `service_x_runbook.md`.
- **Talking Point**: *"Next, we upload our proprietary SOPs or runbooks. The system ingests, chunks, and indexes these documents locally, simulating a Bedrock Knowledge Base."*

### 4. RCA Generation (1:45 - 2:30)
- **Action**: In the main chat interface, enter the query: **"Why is service X showing high CPU and 5xx errors?"**
- **Action**: Ensure `service_x_incident.log` is populated in the Associated Log File input.
- **Action**: Click **"Analyze Incident"**.
- **Talking Point**: *"Now we ask the agent to investigate the incident. Behind the scenes, the RCA Agent classifies the query, retrieves the relevant chunks from the runbook, summarizes the logs, and sends a comprehensive prompt to the LLM."*

### 5. Reviewing the Output (2:30 - 3:15)
- **Action**: Scroll through the generated RCA results.
- **Talking Point**: *"The output is highly structured. We get the Probable Root Cause, actionable Remediation Steps, and specific Evidence extracted from our data."*
- **Action**: Point to the right column (Citations & Confidence).
- **Talking Point**: *"Crucially for enterprise AI, the model provides a Confidence Score, an Escalation Recommendation, and exact Citations back to the source documents, ensuring trust and explainability."*

### 6. Conclusion (3:15 - 3:30)
- **Action**: Show the architecture diagram or briefly mention the backend code.
- **Talking Point**: *"The application is currently running in Mock mode for local testing, but seamlessly connects to AWS Bedrock by simply updating an environment variable. Thank you."*
