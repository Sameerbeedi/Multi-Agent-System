from datetime import datetime
from .client import query_nvidia
import json
from typing import Dict, Any

def extract_information(content: str) -> Dict[str, Any]:
    """
    Extract structured information from the content using AI
    Args:
        content: The parsed text content to analyze
    Returns:
        dict: Extracted structured information
    """
    try:
        extraction_prompt = f"""
        Extract key information from this document:
        {content[:2000]}
        
        Return a valid JSON object with these fields:
        - sender: who sent/created the document
        - dates: any dates found
        - emails: any email addresses
        - key_details: other important details

        Ensure the response is properly formatted JSON.
        """
        
        ai_result = query_nvidia(extraction_prompt)
        parsed_result = json.loads(ai_result)
        
        # Add timestamp and metadata
        parsed_result.update({
            "timestamp": datetime.now().isoformat(),
            "content_length": len(content),
            "extraction_method": "nvidia_ai"
        })
        
        return parsed_result

    except Exception as e:
        return {
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "raw_content": content[:100]
        }