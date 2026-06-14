# Bedrock RCA Copilot

Bedrock RCA Copilot is an enterprise-style AI assistant built for Application Support teams. It helps support engineers perform Root Cause Analysis (RCA) by combining document retrieval (RAG) and log analysis, powered by Amazon Bedrock.

This project unifies two important use cases into one cohesive agentic application:
1. **TalkToAnyDoc**: Ingests and answers questions over Runbooks, SOPs, and incident documents (PDF, DOCX, TXT, MD).
2. **Log Analyzer**: Analyzes system logs (`.log`) to surface the top recurring issues and provides contextual RCA.

## Features
- **File Upload Validation**: Strict file type (`.log`, `.pdf`, `.docx`, `.txt`, `.md`) and size validation (max 100MB).
- **Dual Mode RAG & Analysis**: Upload incident logs and runbooks, and ask questions.
- **Agentic Workflow**: Classifies queries, fetches log metrics, retrieves runbook context, and generates structured RCA.
- **Structured RCA Output**: Returns Probable Root Cause, Evidence, Remediation Steps, Confidence Score, Citations, and Escalation recommendations.
- **Mock Mode**: Out-of-the-box local execution without requiring AWS credentials (`LLM_PROVIDER=mock`).
- **Local Ollama Integration**: Use a local Ollama service for running open-source models offline (`LLM_PROVIDER=ollama-local`).
- **AWS Bedrock Integration**: Seamlessly switch to real AWS Bedrock by updating `.env` (`LLM_PROVIDER=bedrock`).

## Architecture
- **Frontend**: Streamlit
- **Backend**: Python FastAPI
- **LLM**: Amazon Bedrock / Mock Provider
- **RAG**: Local document parsing & BM25-style keyword search (Placeholder for Bedrock Knowledge Base)

For a deeper dive into the architecture, see [docs/architecture.md](docs/architecture.md) and the presentation in [docs/presentation.md](docs/presentation.md).

## Setup Instructions

1. **Clone the repository and install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   By default, `LLM_PROVIDER=mock` is set, allowing you to run the demo locally without AWS credentials.

3. **Run the Backend API**:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

4. **Run the Frontend UI** (in a new terminal):
   ```bash
   streamlit run frontend/app.py
   ```

## Demo & Testing
- Read [docs/demo_script.md](docs/demo_script.md) for a step-by-step guide to demoing the application.
- Run tests:
  ```bash
  pytest tests/
  ```
- Run evaluations:
  ```bash
  python evals/run_eval.py
  ```
