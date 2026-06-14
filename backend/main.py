from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
import os
import shutil
from typing import Optional
from backend.rag.local_rag import rag_engine
from backend.tools.log_analyzer import log_analyzer
from backend.agent.rca_agent import rca_agent
from pydantic import BaseModel

app = FastAPI(title="Bedrock RCA Copilot API")

class RCAQuery(BaseModel):
    query: str
    log_filename: Optional[str] = None

MAX_FILE_SIZE = 100 * 1024 * 1024 # 100 MB
ALLOWED_DOC_EXTENSIONS = {'.pdf', '.docx', '.txt', '.md'}
ALLOWED_LOG_EXTENSIONS = {'.log'}

def validate_file(file: UploadFile, allowed_extensions: set):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {allowed_extensions}")

@app.post("/upload/doc")
async def upload_document(file: UploadFile = File(...)):
    validate_file(file, ALLOWED_DOC_EXTENSIONS)

    # Check size (reading directly to memory might be bad for 100MB, but acceptable for MVP)
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds 100MB limit.")

    filepath = os.path.join("sample_data/runbooks", file.filename)
    with open(filepath, "wb") as f:
        f.write(content)

    # Trigger RAG to reload chunks
    rag_engine._load_and_chunk_documents()

    return {"message": f"Document {file.filename} uploaded and indexed successfully."}

@app.post("/upload/log")
async def upload_log(file: UploadFile = File(...)):
    validate_file(file, ALLOWED_LOG_EXTENSIONS)

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds 100MB limit.")

    filepath = os.path.join("sample_data/incidents", file.filename)
    with open(filepath, "wb") as f:
        f.write(content)

    return {"message": f"Log file {file.filename} uploaded successfully."}

@app.get("/logs/analyze")
def analyze_log_endpoint(filename: str):
    """
    Returns the top recurring issues in the specified log file.
    """
    result = log_analyzer.analyze_logs(filename)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.post("/analyze/rca")
def generate_rca_endpoint(payload: RCAQuery):
    """
    Generates an RCA based on the query and an optional log file.
    """
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        response = rca_agent.generate_rca(query=payload.query, log_filename=payload.log_filename)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}
