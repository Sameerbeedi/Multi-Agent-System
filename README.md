# 🧠 Multi-Agent AI Classification System

This project is a multi-agent AI pipeline powered by NVIDIA's Nemotron model, designed to automatically:

- Detect **file format** (PDF / JSON / Email)
- Classify **intent** (RFQ, Complaint, Invoice, etc.)
- Route input to the appropriate **AI agent**
- Maintain a shared **memory log**
- Display a user-friendly **Streamlit UI**

---

## 🏗️ Architecture

### 🔸 Agents

| Agent           | Purpose                                         |
|------------------|-------------------------------------------------|
| **Classifier Agent** | Identifies format and intent, routes input      |
| **JSON Agent**       | Extracts structured data, validates fields      |
| **Email Agent**      | Extracts sender, urgency, and CRM-style info   |

### 🔸 Shared Memory

- Logic can be found in `memory_store.py`
- Stores all parsed inputs, classification results, and timestamps

---

## 🚀 Features

- 🌐 LLM-based classification using **NVIDIA NIM API**
- 📤 Support for file upload and raw input via **Streamlit UI**
- 📄 Works with `PDF`, `JSON`, and raw/pasted `Email`
- 🧠 Maintains memory for traceability

---

## 🖼️ UI Preview

> Run `streamlit run app.py`

- Upload file or paste Email/JSON
- System detects format + intent
- Routed to the correct agent
- Displays extracted info and log

---

## 🧪 Example Flow

> A user uploads a JSON file:
{
"customer_name": "Acme Corp",
"order_id": "ORD-123",
"items": ["widget", "gadget"],
"total_price": 499.99
}


→ **Classifier Agent** detects JSON + Intent: Invoice  
→ Routed to **JSON Agent**  
→ Extracts structured info, checks for missing fields  
→ Logs result to memory and displays it in the frontend

---


## 📁 Project Structure
├── agents/
│ ├── classifier_agent.py
│ ├── email_agent.py
│ └── json_agent.py
├── utils/
│ ├── file_parser.py
│ ├── intent_classifier.py
│ └── nvidia_client.py
├── memory/
│ └── memory_store.py
├── app.py
├── requirements.txt
├── README.md



---

## 🛠️ Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/ai-multi-agent-classifier
cd ai-multi-agent-classifier

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set NVIDIA API Key/ any other api of your choice 
echo "NVIDIA_API_KEY=your-nvidia-api-key" > .env

# 4. Run the app
streamlit run app.py

