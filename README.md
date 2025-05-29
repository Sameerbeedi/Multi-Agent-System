# 🧠 Multi-Agent AI Classification System

This project is a multi-agent AI pipeline powered by NVIDIA's Nemotron model, designed to automatically:

- Detect **file format** (PDF / JSON / Email)
- Classify **intent** (RFQ, Complaint, Invoice, etc.)
- Route input to the appropriate **AI agent**
- Maintain a shared **memory log**
- Display a user-friendly **Streamlit UI**
---
## 🎬 Demo

👉 [Click here to watch the demo video](https://github.com/Sameerbeedi/Multi-Agent-System/releases/download/version1/d.mp4)

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

## 🖥️ Frontend Overview

The Streamlit UI provides an interactive interface for users to upload files, paste content, view classification results, and manage the memory log.

### Main Functionalities

1. **File Upload & Text Input**
   - Upload files (`PDF`, `JSON`, `TXT`, `EML`) via the sidebar.
   - Paste or type any text, email, or JSON content in the provided text area.

2. **Processing & Classification**
   - Click the **Process** button to classify and extract information from the uploaded or pasted content.
   - The system detects the file format and intent, then routes the input to the appropriate agent.

3. **Results Display**
   - Shows detected file format and intent.
   - Displays extracted information in a readable format.

4. **Memory Log**
   - View a log of all processed files and their extracted information.
   - Filter logs by intent (e.g., Email, Email+Invoice, etc.).
   - Expand each log entry to see details.
   - **Delete individual logs or all logs at once.**

5. **Error Handling**
   - Provides clear error messages for invalid files, unsupported formats, or processing issues.

---

### 🖼️ UI Flow Example

1. **Upload or Paste Content:**  
   Use the sidebar to upload a file or paste text.

2. **Process:**  
   Click the **Process** button.

3. **View Results:**  
   See the classification and extracted information in the main area.

4. **Review Memory Log:**  
   Browse, filter, and manage past results in the Memory Log section.

---



## 📁 Project Structure
├── agents/<br>
│ ├── classifier_agent.py<br>
│ ├── email_agent.py<br>
│ └── json_agent.py<br>
├── utils/<br>
│ ├── file_parser.py<br>
│ ├── intent_classifier.py<br>
│ ├── client.py<br>
| └──information_extractor<br>
├── memory/<br>
│ └── memory_store.py<br>
├── app.py<br>
├── requirements.txt<br>
├── README.md<br>



---

## 🛠️ Setup

```bash
# 1. Clone the repo
git clone https://github.com/Sameerbeedi/Multi-Agent-System
cd Multi-Agent-System

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set NVIDIA API Key/ any other api of your choice 
echo "NVIDIA_API_KEY=your-nvidia-api-key" > .env

# 4. Run the app
streamlit run app.py
```
### Note
**The current processing speed is constrained by available computational resources, but the workflow remains efficient and reliable within those limits.**

