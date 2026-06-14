import json
from typing import Dict, Any, List, Optional
from backend.llm.factory import get_llm_provider
from backend.rag.local_rag import rag_engine
from backend.tools.log_analyzer import log_analyzer

class RCAAgent:
    def __init__(self):
        self.llm = get_llm_provider()

    def generate_rca(self, query: str, log_filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Orchestrates the RCA generation process:
        1. Retrieve relevant context from RAG (Runbooks).
        2. Analyze log file if provided.
        3. Construct prompt.
        4. Call LLM to generate structured output.
        """
        context_parts = []
        citations = []

        # 1. RAG Retrieval
        retrieved_docs = rag_engine.retrieve(query, top_k=3)
        if retrieved_docs:
            doc_context = "--- RUNBOOK / KNOWLEDGE BASE CONTEXT ---\n"
            for doc in retrieved_docs:
                doc_context += f"Source: {doc['source']} (Chunk {doc['chunk_id']})\nContent: {doc['text']}\n\n"
                citations.append(f"{doc['source']} [Chunk {doc['chunk_id']}]")
            context_parts.append(doc_context)
        else:
            context_parts.append("No runbook or SOP context found for the query.")

        # 2. Log Analysis
        if log_filename:
            log_analysis = log_analyzer.analyze_logs(log_filename)
            log_context = "--- LOG ANALYSIS CONTEXT ---\n"
            if "error" in log_analysis:
                log_context += f"Error analyzing log: {log_analysis['error']}\n"
            else:
                log_context += f"Summary: {log_analysis['summary']}\nTop Issues:\n"
                for issue in log_analysis.get('top_issues', []):
                    log_context += f"- {issue['issue']} (Count: {issue['count']})\n"
                citations.append(f"Log Analysis [{log_filename}]")
            context_parts.append(log_context)

        # 3. Combine Context
        full_context = "\n".join(context_parts)

        # 4. Generate Response
        llm_response = self.llm.generate_response(prompt=query, context=full_context)

        # Ensure citations are included in the final output
        # If the LLM generates its own citations, we merge them, otherwise use ours
        final_citations = llm_response.get("citations", [])
        if isinstance(final_citations, list):
            final_citations.extend(citations)
        else:
            final_citations = citations

        llm_response["citations"] = list(set(final_citations)) # deduplicate

        # Ensure all required keys exist
        default_keys = ["probable_root_cause", "evidence", "remediation_steps", "confidence", "escalation_recommendation"]
        for key in default_keys:
            if key not in llm_response:
                llm_response[key] = "Not provided by model."

        return llm_response

rca_agent = RCAAgent()
