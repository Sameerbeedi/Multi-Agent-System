# agents/classifier_agent.py

from utils.file_parser import detect_format, read_file  
from utils.intent_classifier import classify_intent
from agents.email_agent import email
from agents.json_agent import handle_json
from memory.memory_store import MemoryStore
from datetime import datetime

def classify_and_route(filename: str, content: str):
    file_format = detect_format(filename)
    intent = classify_intent(content)

    if file_format == "JSON":
        result = handle_json(content)
    elif file_format == "Email":
        result = email(content)
    elif file_format == "PDF":
        result = read_file(filename, content)  # Pass both filename and content
    else:
        result = "Unsupported format"

    memory_store = MemoryStore()
    memory_store.log(filename, file_format, intent, result)

    return file_format, intent, result
