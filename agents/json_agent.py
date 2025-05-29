# agents/json_agent.py

import json

TARGET_FIELDS = ["customer_name", "order_id", "items", "total_price"]

def handle_json(content: str) -> str:
    try:
        data = json.loads(content)
        missing = [field for field in TARGET_FIELDS if field not in data]

        result = {
            "parsed_data": {k: data.get(k, None) for k in TARGET_FIELDS},
            "missing_fields": missing,
            "status": "ok" if not missing else "incomplete"
        }

        return json.dumps(result, indent=2)
    except json.JSONDecodeError:
        return json.dumps({
            "status": "error",
            "message": "Invalid JSON format"
        }, indent=2)
