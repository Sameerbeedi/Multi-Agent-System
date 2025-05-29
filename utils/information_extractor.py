from datetime import datetime
import logging
import re
import traceback
from typing import Dict, Any

logger = logging.getLogger(__name__)

def extract_information(content: str) -> Dict[str, Any]:
    """
    Extract structured information from the content based on patterns
    Args:
        content: The parsed text content to analyze
    Returns:
        dict: Extracted structured information
    """
    try:
        # Initialize extracted info dictionary
        info = {
            "timestamp": datetime.now().isoformat(),
            "content_length": len(content),
            "extracted_text": content[:500],  # First 500 chars as preview
            "key_details": {}
        }

        # Extract email addresses if present
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', content)
        if emails:
            info["key_details"]["emails"] = emails

        # Extract dates if present
        dates = re.findall(r'\d{2}[/-]\d{2}[/-]\d{4}', content)
        if dates:
            info["key_details"]["dates"] = dates

        # Extract any amounts/prices
        amounts = re.findall(r'[\$£€]?\d+(?:,\d{3})*(?:\.\d{2})?', content)
        if amounts:
            info["key_details"]["amounts"] = amounts

        # Add new extractions here
        # Extract phone numbers
        phones = re.findall(r'\+?\d{1,3}[-.]?\d{3}[-.]?\d{4}', content)
        if phones:
            info["key_details"]["phone_numbers"] = phones

        # Extract URLs
        urls = re.findall(r'https?://(?:[\w-]+\.)+[\w-]+(?:/[\w-./?%&=]*)?', content)
        if urls:
            info["key_details"]["urls"] = urls

        # Extract potential company names (basic)
        companies = re.findall(r'(?:[A-Z][a-z]+ )*(?:Inc\.|Ltd\.|LLC|Corp\.)', content)
        if companies:
            info["key_details"]["companies"] = companies

        logger.info("Successfully extracted information from content")
        return info

    except Exception as e:
        logger.error(f"Error extracting information: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "raw_content": content[:100]  # First 100 chars for debugging
        }