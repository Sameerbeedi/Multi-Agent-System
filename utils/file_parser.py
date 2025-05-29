# utils/file_parser.py
import os
import io
import pdfplumber
import json
import logging
import warnings
import traceback
import logging.handlers

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create a file handler
file_handler = logging.handlers.RotatingFileHandler(
    'pdf_processing.log',
    maxBytes=1024*1024,
    backupCount=5
)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Configure PDF warnings
logging.getLogger("pdfminer").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning)

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
    logger.info(f"Processing file: {filename} with format: {file_format}")
    
    if file_format == "PDF":
        try:
            logger.debug(f"PDF content type: {type(content)}")
            logger.debug(f"PDF content size: {len(content)} bytes")
            
            # Handle PDF content with warning suppression
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with pdfplumber.open(io.BytesIO(content)) as pdf:
                    logger.info(f"Successfully opened PDF with {len(pdf.pages)} pages")
                    text = ""
                    for i, page in enumerate(pdf.pages, 1):
                        try:
                            extracted = page.extract_text()
                            if extracted:
                                text += extracted + "\n"
                                logger.debug(f"Successfully extracted text from page {i}")
                            else:
                                logger.warning(f"No text extracted from page {i}")
                        except Exception as page_error:
                            logger.error(f"Error processing page {i}: {str(page_error)}")
                    
                    if not text.strip():
                        logger.warning("No text content extracted from PDF")
                    return text.strip()
        except Exception as e:
            logger.error(f"PDF processing error: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
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
