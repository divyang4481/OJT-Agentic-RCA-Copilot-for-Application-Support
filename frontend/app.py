import streamlit as st
import requests
import os

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Bedrock RCA Copilot", layout="wide")

st.title("Bedrock RCA Copilot 🚀")
st.markdown("""
This enterprise AI assistant helps Support Engineers perform Root Cause Analysis (RCA).
Upload **Runbooks** (PDF, DOCX, TXT, MD) and **Logs** (.log), then ask questions about incidents.
""")

st.sidebar.header("Data Ingestion")

# Document Upload
st.sidebar.subheader("1. Upload Runbooks/SOPs")
doc_file = st.sidebar.file_uploader("Upload Document (Max 100MB)", type=["pdf", "docx", "txt", "md"])
if st.sidebar.button("Upload Document"):
    if doc_file:
        with st.spinner("Uploading document..."):
            files = {"file": (doc_file.name, doc_file, doc_file.type)}
            response = requests.post(f"{API_BASE_URL}/upload/doc", files=files)
            if response.status_code == 200:
                st.sidebar.success(response.json()["message"])
            else:
                st.sidebar.error(f"Upload failed: {response.text}")
    else:
        st.sidebar.warning("Please select a document first.")

st.sidebar.divider()

# Log Upload
st.sidebar.subheader("2. Upload Application Logs")
log_file = st.sidebar.file_uploader("Upload Log File (Max 100MB)", type=["log"])
if st.sidebar.button("Upload Log"):
    if log_file:
        with st.spinner("Uploading log file..."):
            files = {"file": (log_file.name, log_file, log_file.type)}
            response = requests.post(f"{API_BASE_URL}/upload/log", files=files)
            if response.status_code == 200:
                st.sidebar.success(response.json()["message"])
                # Store the uploaded log filename in session state for analysis
                st.session_state["uploaded_log"] = log_file.name
            else:
                st.sidebar.error(f"Upload failed: {response.text}")
    else:
        st.sidebar.warning("Please select a log file first.")

st.sidebar.divider()

# Log Analysis View
if "uploaded_log" in st.session_state:
    st.sidebar.subheader(f"Log Analyzer: {st.session_state['uploaded_log']}")
    if st.sidebar.button("Analyze Log for Top Issues"):
        with st.spinner("Analyzing logs..."):
            res = requests.get(f"{API_BASE_URL}/logs/analyze", params={"filename": st.session_state["uploaded_log"]})
            if res.status_code == 200:
                data = res.json()
                st.sidebar.info(data.get("summary", ""))
                for issue in data.get("top_issues", []):
                    st.sidebar.markdown(f"- **{issue['issue']}** (Count: {issue['count']})")
            else:
                st.sidebar.error("Failed to analyze logs.")

# Main Chat / Query Interface
st.header("Root Cause Analysis")

query = st.text_area("Incident Query:", placeholder="e.g., Why is service X showing high CPU and 5xx errors?")
log_filename_input = st.text_input("Associated Log File (optional):", value=st.session_state.get("uploaded_log", ""), help="Name of the log file to include in context.")

if st.button("Analyze Incident", type="primary"):
    if not query.strip():
        st.warning("Please enter an incident query.")
    else:
        with st.spinner("Agent is retrieving context and analyzing root cause..."):
            payload = {
                "query": query,
                "log_filename": log_filename_input if log_filename_input.strip() else None
            }
            res = requests.post(f"{API_BASE_URL}/analyze/rca", json=payload)

            if res.status_code == 200:
                rca_data = res.json()

                # Display Results
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.subheader("🛠️ Probable Root Cause")
                    st.info(rca_data.get("probable_root_cause", "N/A"))

                    st.subheader("🩺 Remediation Steps")
                    remediation = rca_data.get("remediation_steps", [])
                    if isinstance(remediation, list):
                        for step in remediation:
                            st.write(f"- {step}")
                    else:
                        st.write(remediation)

                    st.subheader("🔍 Evidence")
                    evidence = rca_data.get("evidence", [])
                    if isinstance(evidence, list):
                        for ev in evidence:
                            st.write(f"- {ev}")
                    else:
                        st.write(evidence)

                with col2:
                    st.subheader("📊 Meta")
                    st.metric("Confidence Score", rca_data.get("confidence", "N/A"))

                    st.write("**Escalation Recommendation:**")
                    st.warning(rca_data.get("escalation_recommendation", "N/A"))

                    st.write("**📚 Citations:**")
                    citations = rca_data.get("citations", [])
                    if citations:
                        for cit in citations:
                            st.caption(f"- {cit}")
                    else:
                        st.caption("No citations provided.")
            else:
                st.error(f"Error generating RCA: {res.text}")

st.markdown("---")
st.caption("AWS Bedrock OJT Solution - By Jules")
