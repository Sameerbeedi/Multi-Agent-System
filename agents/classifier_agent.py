# agents/classifier_agent.py

from utils.file_parser import detect_format, read_file
from utils.intent_classifier import classify_intent
from utils.information_extractor import extract_information  
from memory.memory_store import MemoryStore
from datetime import datetime
import logging
import traceback
import json

logger = logging.getLogger(__name__)

def classify_and_route(filename: str, content: str):
    try:
        # Parse the file content
        parsed_content = read_file(filename, content)
        logger.info(f"Successfully parsed content from {filename}")

        # Validate parsed content
        if not parsed_content:
            raise ValueError("No content parsed from file")

        # Get format and classify
        file_format = detect_format(filename)
        intent = classify_intent(parsed_content)
        result = extract_information(parsed_content)

        # Validate extracted data
        if not isinstance(result, dict):
            logger.error(f"Invalid result type: {type(result)}")
            result = {"error": "Invalid extraction result", "raw_content": str(result)[:100]}

        # Convert result dict to JSON string for database storage
        try:
            result_str = json.dumps(result)
        except TypeError as json_error:
            logger.error(f"JSON serialization error: {str(json_error)}")
            result_str = json.dumps({"error": "Failed to serialize result"})

        # Add to database with validation
        try:
            memory_store = MemoryStore()
            # Validate required fields
            if not all([filename, file_format, intent]):
                raise ValueError("Missing required fields for database entry")

            # Use log() instead of add_log()
            memory_store.log(
                source=str(filename)[:255],  # Limit string length
                filetype=str(file_format)[:50],
                intent=str(intent)[:100],
                extracted=result_str
            )
            logger.info(f"Successfully added to database: {filename}")
        except Exception as db_error:
            logger.error(f"Database error: {str(db_error)}")
            logger.error(f"Database traceback: {traceback.format_exc()}")
            raise Exception(f"Failed to save to database: {str(db_error)}")
        finally:
            if hasattr(memory_store, 'conn') and memory_store.conn:
                memory_store.conn.close()

        return file_format, intent, result

    except Exception as e:
        logger.error(f"Classification error: {str(e)}")
        logger.error(f"Classification traceback: {traceback.format_exc()}")
        raise
