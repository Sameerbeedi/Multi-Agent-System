# utils/file_parser.py
import os

def detect_format(file_path):
    _, ext = os.path.splitext(file_path.lower())
    if ext == '.pdf':
        return "PDF"
    elif ext == '.json':
        return "JSON"
    elif ext in ['.txt', '.eml']:
        return "Email"
    return "Unknown"

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def read_file(filename, content):
    # Add logic to handle PDF content from memory
    # For example, use PyPDF2 or pdfplumber to read from bytes
    pass  # Implement your PDF/content parsing logic here
