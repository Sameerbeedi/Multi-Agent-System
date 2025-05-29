# app.py

import streamlit as st
from agents.classifier_agent import classify_and_route
from memory.memory_store import MemoryStore
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Multi-Agent AI Classifier", layout="wide")
st.title("📂 Multi-Agent AI Classifier")

st.sidebar.header("Upload or Paste Data")

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "json", "txt", "eml"])
raw_text = st.sidebar.text_area("Or paste raw Email/JSON content")
submit_button = st.sidebar.button("Process")

if submit_button:
    if uploaded_file:
        if uploaded_file.name.lower().endswith(".pdf"):
            content = uploaded_file.read()  
        else:
            content = uploaded_file.read().decode("utf-8", errors="ignore")
        file_name = uploaded_file.name
    elif raw_text.strip():
        content = raw_text
        file_name = "manual_input.txt"
    else:
        st.warning("Please upload a file or paste some content.")
        st.stop()

    with st.spinner("Classifying and Routing..."):
        file_format, intent, result = classify_and_route(file_name, content)

    st.subheader("📌 Results")
    st.markdown(f"- **Format**: `{file_format}`")
    st.markdown(f"- **Intent**: `{intent}`")

    st.subheader("🧠 Extracted Information")
    st.code(result, language="markdown")

    st.subheader("📝 Memory Log (Last 5)")
    memory_store = MemoryStore()
    try:
        cursor = memory_store.conn.execute(
            "SELECT source, type, intent, extracted, timestamp FROM memory ORDER BY id DESC LIMIT 5"
        )
        rows = cursor.fetchall()
        for entry in rows:
            st.json({
                "source": entry[0],
                "type": entry[1],
                "intent": entry[2],
                "extracted": entry[3],
                "timestamp": entry[4]
            })
    finally:
        memory_store.conn.close()
