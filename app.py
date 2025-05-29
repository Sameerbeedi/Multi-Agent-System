# app.py

import streamlit as st
from agents.classifier_agent import classify_and_route
from memory.memory_store import MemoryStore
from dotenv import load_dotenv
import json

load_dotenv()

st.set_page_config(page_title="Multi-Agent AI Classifier", layout="wide")
st.title("📂 Multi-Agent AI Classifier")

st.sidebar.header("Upload or Paste Data")

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "json", "txt", "eml"])
raw_text = st.sidebar.text_area("Or paste raw Email/JSON content")
submit_button = st.sidebar.button("Process")

def is_json_file(filename, content):
    """Validate if the content is valid JSON"""
    if filename.lower().endswith(".json"):
        try:
            # Handle both string and bytes content
            if isinstance(content, bytes):
                content = content.decode("utf-8", errors="ignore")
            # Try to parse the JSON content
            json.loads(content)
            return True
        except json.JSONDecodeError as e:
            st.error(f"JSON Validation Error: {str(e)}")
            return False
        except Exception as e:
            st.error(f"Unexpected error while validating JSON: {str(e)}")
            return False
    return False

# Replace the processing section with this updated code
if submit_button:
    is_valid_json = False
    content = None

    try:
        if uploaded_file:
            file_name = uploaded_file.name
            if file_name.lower().endswith(".pdf"):
                content = uploaded_file.read()
            elif file_name.lower().endswith(".json"):
                raw_content = uploaded_file.read()
                # Validate JSON before processing
                if not is_json_file(file_name, raw_content):
                    st.error("The uploaded JSON file is not valid. Please check the file content.")
                    st.stop()
                content = raw_content.decode("utf-8", errors="ignore")
                is_valid_json = True
            else:
                content = uploaded_file.read().decode("utf-8", errors="ignore")
        elif raw_text.strip():
            content = raw_text
            file_name = "manual_input.txt"
        else:
            st.warning("Please upload a file or paste some content.")
            st.stop()

        # Validate content before processing
        if content is None:
            st.error("No content to process")
            st.stop()

        # Process file
        with st.spinner("Classifying and Routing..."):
            try:
                file_format, intent, result = classify_and_route(file_name, content)
                st.success(f"{file_format} file processed successfully.")
                
                # Display results
                st.subheader("📌 Results")
                st.markdown(f"- **Format**: `{file_format}`")
                st.markdown(f"- **Intent**: `{intent}`")
                st.subheader("🧠 Extracted Information")
                st.code(result, language="markdown")
                
            except Exception as e:
                st.error(f"Error during classification: {str(e)}")
                st.stop()

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.stop()

# --- Memory Log Section ---
st.markdown("---")
st.header("📝 Memory Log")

memory_store = MemoryStore()

# Only allow these intents for filtering
allowed_intents = ["Invoice", "RFQ", "Complaint", "Regulation", "Other"]
intents_in_db = memory_store.fetch_intents()
# Filter only allowed intents and add "All"
intents = ["All"] + [i for i in allowed_intents if i in intents_in_db]
selected_intent = st.selectbox("Filter by Intent", intents)

# Fetch logs based on allowed intent
logs = memory_store.fetch_logs(intent_filter=selected_intent, limit=10)

if st.button("Delete All Logs"):
    memory_store.delete_all_logs()
    st.success("All logs deleted. Please refresh the page.")

if logs:
    for entry in logs:
        log_id, source, filetype, intent, extracted, timestamp = entry
        # Only show logs with allowed intents
        if intent in allowed_intents:
            with st.expander(f"ID: {log_id} | {intent} | {source} | {timestamp}"):
                st.markdown(f"**Type:** {filetype}")
                st.markdown(f"**Intent:** {intent}")
                st.markdown(f"**Extracted:**\n```\n{extracted}\n```")
                st.markdown(f"**Timestamp:** {timestamp}")
                if st.button(f"Delete Log {log_id}", key=f"delete_{log_id}"):
                    memory_store.delete_log(log_id)
                    st.success(f"Log {log_id} deleted. Please refresh the page.")
else:
    st.info("No logs found for the selected intent.")

memory_store.conn.close()
