# utils/file_parser.py
import os
import io
import pdfplumber
import json
import warnings

def detect_format(file_path):
    _, ext = os.path.splitext(file_path.lower())
    if ext == '.pdf':
        return "PDF"
    elif ext == '.json':
        return "JSON"
    elif ext in ['.txt', '.eml']:
        return "Email"
    return "Unknown"

def read_file(filename, content):
    """
    Read and parse different file types from content
    Args:
        filename: Name of the file
        content: File content (can be bytes or string)
    Returns:
        str: Parsed content as text
    """
    file_format = detect_format(filename)
    
    if file_format == "PDF":
        try:
            # Handle PDF content with warning suppression
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with pdfplumber.open(io.BytesIO(content)) as pdf:
                    text = ""
                    for page in pdf.pages:
                        try:
                            extracted = page.extract_text()
                            if extracted:
                                text += extracted + "\n"
                        except Exception:
                            continue
                    return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
            
    elif file_format == "JSON":
        try:
            # Handle JSON content
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            return json.dumps(json.loads(content), indent=2)
        except Exception as e:
            raise Exception(f"Error parsing JSON: {str(e)}")
            
    else:
        # Handle text/email content
        if isinstance(content, bytes):
            return content.decode('utf-8', errors='ignore')
        return content
