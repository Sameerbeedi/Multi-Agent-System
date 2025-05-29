from typing import Dict, Any

def clean_json_string(json_str: str) -> str:
    """Remove comments and clean JSON string for parsing"""
    import re
    
    # Remove single-line comments
    json_str = re.sub(r'//.*$', '', json_str, flags=re.MULTILINE)
    
    # Remove multi-line comments
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
    
    return json_str

def extract_information(content: str) -> Dict[str, Any]:
    from datetime import datetime
    from .client import query_nvidia
    import json

    def create_error_response(error_msg: str, ai_result: str = None) -> Dict[str, Any]:
        response = {
            "error": error_msg,
            "timestamp": datetime.now().isoformat(),
            "raw_content": content[:100] if content else "",
            "status": "error"
        }
        if ai_result:
            response["ai_result"] = ai_result
        return response

    if not content:
        return create_error_response("Empty content provided")

    try:
        # First determine if input is JSON
        try:
            json_content = json.loads(content)
            extraction_prompt = f"""
            Analyze this JSON document and extract key information into a clean JSON structure.
            Format requirements:
            - All strings must use double quotes
            - No comments in the JSON
            - No trailing commas
            - No control characters

            Required fields:
            - sender: Extract from From/Sender fields or main content
            - recipients: Array of recipient email addresses
            - subject: Message or document subject
            - body: Main message content
            - dates: Array of all dates found
            - emails: Array of all email addresses
            - key_details: Object containing any important transaction/business details

            Source JSON:
            {json.dumps(json_content, indent=2)}
            """
        except json.JSONDecodeError:
            # Check if it might be PDF content
            if isinstance(content, bytes) or content.startswith('%PDF'):
                extraction_prompt = f"""
                Extract key information from this PDF content.
                Return a clean JSON object with these fields:
                - sender: Author or sender information
                - recipients: Array of intended recipients
                - subject: Document title or subject
                - body: Main document content (summarized if long)
                - dates: Array of dates found
                - emails: Array of email addresses
                - key_details: Object with key document information

                Note: Return valid JSON with double quotes, no comments, no trailing commas.
                """
            else:
                # Plain text prompt
                extraction_prompt = f"""
                Extract information from this text content.
                Return a clean JSON object with these fields:
                - sender: Who sent or authored this
                - recipients: Array of recipients
                - subject: Message or document subject
                - body: Main content (summarized if needed)
                - dates: Array of any dates found
                - emails: Array of email addresses found
                - key_details: Object with important details

                Return valid JSON:
                - Use double quotes for strings
                - No comments
                - No trailing commas
                - Arrays for multiple values
                - Null for missing fields

                Content:
                {content[:2000]}
                """

        ai_result = query_nvidia(extraction_prompt)
        
        if not ai_result:
            return create_error_response("AI returned empty response")
            
        if not isinstance(ai_result, str):
            return create_error_response(f"AI returned invalid type: {type(ai_result)}")
            
        ai_result = ai_result.strip()
        
        # Look for JSON content within markdown or other formatting
        json_start = ai_result.find('{')
        json_end = ai_result.rfind('}')
        
        if json_start >= 0 and json_end > json_start:
            try:
                ai_result = ai_result[json_start:json_end + 1]
                # Clean the JSON string before parsing
                cleaned_json = clean_json_string(ai_result)
                parsed_result = json.loads(cleaned_json)
            except json.JSONDecodeError as e:
                return create_error_response(f"Failed to parse AI JSON: {str(e)}", ai_result)
        else:
            return create_error_response("No JSON object found in AI response", ai_result)

        # Add metadata
        parsed_result.update({
            "timestamp": datetime.now().isoformat(),
            "content_length": len(content),
            "extraction_method": "nvidia_ai",
            "content_type": "json" if "json_content" in locals() else "text",
            "status": "success"
        })
        return parsed_result

    except Exception as e:
        return create_error_response(f"Unexpected error: {str(e)}")