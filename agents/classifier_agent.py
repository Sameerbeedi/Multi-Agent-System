# agents/classifier_agent.py

from utils.file_parser import detect_format, read_file
from utils.intent_classifier import classify_intent
from utils.information_extractor import extract_information
from utils.client import query_nvidia
from memory.memory_store import MemoryStore
from datetime import datetime
import json

def classify_and_route(filename: str, content: str):
    try:
        # Parse the file content
        parsed_content = read_file(filename, content)

        # Validate parsed content
        if not parsed_content:
            raise ValueError("No content parsed from file")

        # Get format and classify
        file_format = detect_format(filename)
        intent = classify_intent(parsed_content)

        # Try AI-powered extraction
        try:
            extraction_prompt = f"""
            Extract key information from this document:
            {parsed_content[:2000]}
            
            Return a JSON object with these fields:
            - sender: who sent/created the document
            - recipients: who received the document
            - dates: any dates found
            - emails: any email addresses
            - amounts: any monetary amounts
            - key_details: other important information
            
            Format the response as valid JSON only.
            """
            
            ai_result = query_nvidia(extraction_prompt)
            result = json.loads(ai_result)
            
        except Exception as ai_error:
            result = extract_information(parsed_content)

        # Validate extracted data
        if not isinstance(result, dict):
            result = {"error": "Invalid extraction result", "raw_content": str(result)[:100]}

        # Add metadata to result
        result.update({
            "file_format": file_format,
            "extraction_method": "nvidia_ai" if "ai_error" not in locals() else "regex",
            "processed_at": datetime.now().isoformat()
        })

        # Convert result dict to JSON string for database storage
        try:
            result_str = json.dumps(result)
        except TypeError:
            result_str = json.dumps({"error": "Failed to serialize result"})

        # Add to database with validation
        try:
            memory_store = MemoryStore()
            # Validate required fields
            if not all([filename, file_format, intent]):
                raise ValueError("Missing required fields for database entry")

            memory_store.log(
                source=str(filename)[:255],
                filetype=str(file_format)[:50],
                intent=str(intent)[:100],
                extracted=result_str
            )
        except Exception as db_error:
            raise Exception(f"Failed to save to database: {str(db_error)}")
        finally:
            if hasattr(memory_store, 'conn') and memory_store.conn:
                memory_store.conn.close()

        return file_format, intent, result

    except Exception as e:
        raise
