# utils/intent_classifier.py

from utils.client import query_nvidia

def classify_intent(text: str) -> str:
    prompt = f"""Classify the intent of the following content.
Pick one intent from: Invoice, RFQ, Complaint, Regulation, Other.

Content:
\"\"\"
{text}
\"\"\"

Return only the label.
"""
    return query_nvidia(prompt)
