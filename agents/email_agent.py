# agents/email_agent.py

from utils.client import query_nvidia

def email(email_content: str) -> str:
    prompt = f"""
You are an intelligent email processor.
Given this email, extract the following:
- Sender (if mentioned)
- Intent (Invoice, RFQ, Complaint, Regulation, Other)
- Urgency (Low, Medium, High)
- Summary (1-2 lines)

Email:
\"\"\"
{email_content}
\"\"\"
"""
    return query_nvidia(prompt)
