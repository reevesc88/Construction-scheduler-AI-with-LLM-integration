import streamlit as st
import requests
import pandas as pd
import json
import os

st.set_page_config(page_title="Construction AI Planner", layout="wide")
st.title("🏗️ Construction AI Planner")

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Check API health
try:
    health = requests.get(f"{API_URL}/health", timeout=2)
    if health.status_code == 200:
        st.success("✓ Backend Connected")
    else:
        st.error("✗ Backend Connection Failed")
except:
    st.error("✗ Cannot connect to backend. Is it running?")

# --- Section 1: Upload Document ---
st.header("1. Upload Specification")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    if st.button("Process Document"):
        with st.spinner("Processing PDF..."):
            try:
                files = {"file": uploaded_file}
                response = requests.post(f"{API_URL}/ingest/document", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✓ Ingested {result['filename']}")
                    st.json(result)
                else:
                    st.error(f"Upload failed: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# --- Section 2: Generate Plan ---
st.header("2. Generate Execution Plan")

col1, col2 = st.columns(2)
with col1:
    project_id = st.text_input("Project ID", value="DEMO-2025")
    location = st.text_input("Location", value="Seattle, WA")

with col2:
    notes = st.text_area("Special Notes", value="Standard project")

if st.button("Generate Plan"):
    with st.spinner("Running AI agents..."):
        try:
            payload = {
                "project_id": project_id,
                "location": location,
                "notes": notes
            }
            response = requests.post(f"{API_URL}/generate/plan", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    plan = data["plan"]
                    
                    # KPIs
                    k1, k2, k3 = st.columns(3)
                    k1.metric("Total Cost", f"${plan['total_estimated_cost']:,.2f}")
                    k2.metric("Duration", f"{plan['total_duration_days']} days")
                    k3.metric("Tasks", len(plan['tasks']))
                    
                    # Tasks Table
                    st.subheader("Tasks")
                    df_tasks = pd.DataFrame(plan['tasks'])
                    st.dataframe(df_tasks[['id', 'description', 'phase', 'duration_days', 'total_cost']])
                    
                    # Risks
                    st.subheader("Risks Identified")
                    for risk in plan['risks']:
                        with st.expander(f"{risk['risk_type']} ({risk['probability']})"):
                            st.write(risk['mitigation_strategy'])
                else:
                    st.error("Plan generation failed")
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.divider()
st.caption("Powered by OpenAI GPT-4 | Backend: FastAPI")