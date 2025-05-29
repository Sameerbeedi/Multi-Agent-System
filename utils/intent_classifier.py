# utils/intent_classifier.py

from utils.client import query_nvidia

def classify_intent(text: str) -> str:
    prompt = f"""Classify the intent of the following content.
Base intents are: Invoice, RFQ, Complaint, Regulation.
Since all content is from emails, always prefix the intent with 'Email+'.
For example: 'Email+Invoice', 'Email+RFQ', 'Email+Complaint', 'Email+Regulation'.
If no specific intent is detected, return just 'Email'.

Content:
\"\"\"
{text}
\"\"\"

Return only the label (e.g., 'Email+Invoice', 'Email+RFQ', 'Email').
"""
    result = query_nvidia(prompt)
    
    # Ensure result is properly formatted
    if result and isinstance(result, str):
        result = result.strip()
        if result not in ['Email']:  # If it's not just 'Email'
            if not result.startswith('Email+'):  # If missing Email+ prefix
                result = f'Email+{result}'
    return result or 'Email'  # Default to 'Email' if no result
