# app.py

import streamlit as st
from agents.classifier_agent import classify_and_route
from memory.memory_store import MemoryStore
from dotenv import load_dotenv
import json
import hashlib

load_dotenv()

st.set_page_config(page_title="Multi-Agent AI Classifier", layout="wide")
st.title("📂 Multi-Agent AI Classifier")

st.sidebar.header("Upload or Paste Data")

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "json", "txt", "eml"])
raw_text = st.sidebar.text_area("Add text content", help="Paste any text, email or JSON content here")
submit_button = st.sidebar.button("Process")

# Create a single MemoryStore instance
memory_store = MemoryStore()

def clean_content(content: str) -> str:
    """Clean and sanitize content before processing"""
    if isinstance(content, bytes):
        content = content.decode('utf-8', errors='ignore')
    # Remove null bytes and other control characters except newlines and tabs
    return ''.join(char for char in content if char >= ' ' or char in '\n\t')

def is_json_file(filename, content):
    """Validate if the content is valid JSON"""
    if filename.lower().endswith(".json"):
        try:
            cleaned_content = clean_content(content)
            json.loads(cleaned_content)
            return True
        except json.JSONDecodeError as e:
            st.error(f"JSON Validation Error: {str(e)}")
            return False
        except Exception as e:
            st.error(f"Unexpected error while validating JSON: {str(e)}")
            return False
    return False

# Replace the processing section
if submit_button:
    content = None
    file_name = "manual_input.txt"

    try:
        if uploaded_file:
            file_name = uploaded_file.name
            file_bytes = uploaded_file.read()
            # For PDFs, keep as bytes; for others, decode to string
            if file_name.lower().endswith(".pdf"):
                content = file_bytes
            else:
                try:
                    content = file_bytes.decode('utf-8', errors='ignore')
                except Exception:
                    content = file_bytes  # fallback to bytes if decode fails

            # If it's a JSON file, validate it
            if file_name.lower().endswith(".json"):
                try:
                    json.loads(content)
                except Exception:
                    st.error("Invalid JSON file format")
                    st.stop()

        elif raw_text.strip():
            content = clean_content(raw_text)
            file_name = "text_input.txt"
        else:
            st.warning("Please upload a file or add text content.")
            st.stop()

        # Deduplication: always hash bytes
        if isinstance(content, str):
            content_bytes = content.encode()
        else:
            content_bytes = content
        content_hash = hashlib.md5(content_bytes).hexdigest()
        file_identifier = f"{file_name}_{content_hash}"

        if content is None:
            st.error("No content to process")
            st.stop()

        # Process file
        with st.spinner("Classifying and Routing..."):
            try:
                file_format, intent, result = classify_and_route(file_name, content)
                st.success(f"{file_format} file processed successfully.")

                try:
                    memory_store.log(
                        source=file_name,
                        filetype=file_format,
                        intent=intent,
                        extracted=result
                    )
                    st.success("Results saved to database")
                except Exception as e:
                    st.error(f"Failed to save to database: {str(e)}")

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

# Use existing memory_store instance
intents_in_db = memory_store.fetch_intents()

# Only allow these intents for filtering
allowed_intents = [
    "Email",
    "Email+Invoice", 
    "Email+RFQ", 
    "Email+Complaint", 
    "Email+Regulation"
]
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

# At the very end of the file, close the connection
if __name__ == '__main__':
    # Close connection when app exits
    memory_store.conn.close()
