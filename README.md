# 🤖 Multi-Agent AI Processing System

Intelligent document processing with classification, risk assessment, and automated actions.

---

## 🚀 Overview

This project is a modular, multi-agent system for processing and analyzing documents (Emails, JSON payloads, and PDFs) using AI. It features:

- **Streamlit Frontend**: User-friendly web interface for uploading and analyzing documents.
- **FastAPI Backend**: Robust API for document classification, risk assessment, and action routing.
- **AI Agents**: Specialized agents for email, JSON, and PDF analysis, powered by Google Gemini.
- **Automated Actions**: Escalation, risk alerts, and logging based on intelligent classification.
- **Memory & Audit**: All processed entries are stored and viewable for audit and monitoring.

---

## 🗂️ Project Structure

```
.
├── app/
│   ├── main.py                # FastAPI backend
│   ├── streamlit_ui.py        # Streamlit frontend
│   ├── agents/                # AI agent modules (email, json, pdf, classifier)
│   ├── router/                # Action routing logic
│   ├── memory/                # Memory storage (SQLite)
│   ├── utils/                 # Internal actions (escalate, log, risk alert)
├── examples/
│   ├── emails/                # Sample email files
│   ├── json/                  # Sample JSON files
│   ├── pdfs/                  # Sample PDF files
├── requirements.txt           # Python dependencies
├── README.md                  # This file
```

---

## ✨ Features

- **📧 Email, 🔧 JSON, 📄 PDF Processing**: Upload or paste content for instant AI-powered analysis.
- **📊 Classification**: Detects format, intent, and tone.
- **🚨 Risk Assessment**: Flags anomalies and risks.
- **🤖 Agent Trace**: See how each agent processed your data.
- **⚡ Automated Actions**: Triggers escalation, risk alerts, and logs as needed.
- **🧠 System Memory**: View all processed entries and their risk status.
- **🔄 Auto-Refresh**: Optionally auto-refreshes memory view.
- **📝 Raw AI Response**: Inspect the raw output from the AI model.

---

## 🏗️ Architecture

- **Frontend**: `app/streamlit_ui.py` (Streamlit)
- **Backend**: `app/main.py` (FastAPI)
- **Agents**: `app/agents/` (Email, JSON, PDF, Classifier)
- **Action Router**: `app/router/action_router.py`
- **Memory**: `app/memory/memory_store.py` (SQLite)
- **Internal Actions**: `app/utils/internal_actions.py`

---

## 🏁 Quickstart

### 1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/multi-agent-system.git
cd multi-agent-system
```

### 2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 3. **Set Up Environment Variables**

- Create a `.env` file in the root directory.
- Add your Google Gemini API key:
  ```
  GEMINI_API_KEY=your-gemini-api-key
  ```

### 4. **Run the Backend (FastAPI)**

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --workers 4
```

### 5. **Run the Frontend (Streamlit)**

```bash
streamlit run app/streamlit_ui.py
```

- Open your browser to [http://localhost:8501](http://localhost:8501)

---

## 🧪 Usage

### **Email Example**

Paste or upload an email like:

```
From: john.smith@company.com
To: sales@vendor.com
Subject: Request for Quotation for Office Supplies

Dear Sales Team,

We are interested in purchasing office supplies including pens, notebooks, and printer paper. Kindly send us your best quotation for bulk orders.

Thank you,
John Smith
Procurement Manager
```

### **JSON Example**

Paste or upload a JSON payload like:

```json
{
  "request_type": "RFQ",
  "items": [
    {"item": "Laptop", "quantity": 10},
    {"item": "Monitor", "quantity": 15}
  ],
  "requested_by": "procurement_team",
  "priority": "normal"
}
```

### **PDF Example**

Upload a PDF document (e.g., an invoice or compliance document) for analysis.

---

## 🛠️ API Endpoints

| Endpoint                | Method | Description                        |
|-------------------------|--------|------------------------------------|
| `/process/email`        | POST   | Analyze email content              |
| `/process/json`         | POST   | Analyze JSON payload               |
| `/process/pdf`          | POST   | Analyze PDF document               |
| `/memory`               | GET    | View all processed entries         |
| `/crm/escalate`         | POST   | Simulate CRM escalation            |
| `/risk_alert`           | POST   | Simulate risk alert                |
| `/log`                  | POST   | Simulate logging                   |

---

## 🧩 Agents & Internal Actions

### **Agents**
- **Email Agent**: Extracts sender, urgency, issue, and tone.
- **JSON Agent**: Validates schema, flags anomalies.
- **PDF Agent**: Extracts text, totals, and compliance terms.
- **Classifier**: Uses Google Gemini for format, intent, and tone.

### **Action Router**
- Triggers escalation, risk alerts, and logs based on classification and agent data.
- Calls internal actions directly for efficiency (no internal HTTP calls).

### **Internal Actions**
- **escalate_crm**: Simulates CRM escalation.
- **risk_alert**: Simulates compliance/risk alert.
- **log_alert**: Simulates logging/audit trail.

---

## 🗄️ Memory & Audit

- All processed entries are stored in a local SQLite database (`memory.db`).
- View recent entries, risk status, and actions from the Streamlit UI.
- Memory can be refreshed or auto-refreshed from the UI.

---

## 📂 Examples

- See the `examples/` directory for sample emails, JSON, and PDFs to test the system.
  - `examples/emails/` — Example email files
  - `examples/json/` — Example JSON payloads
  - `examples/pdfs/` — Example PDF documents

---

## ⚙️ Configuration

- **API Base URL**: Set in the Streamlit sidebar.
- **Auto-Refresh**: Enable to auto-update memory view.
- **Show Raw AI Responses**: Toggle in the sidebar.
- **Google Gemini API Key**: Required for classification (set in `.env`).

---

## 🛡️ Security & Notes

- This project is for demonstration and prototyping. For production, secure API keys, use a production database, and add authentication.
- Google Gemini API key is required for classification.
- No internal HTTP calls are made for actions—everything is handled via direct function calls for reliability and speed.

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Gemini](https://ai.google.dev/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)

---

## 📬 Contact

For questions, suggestions, or contributions, open an issue or contact the maintainer.

---

**Enjoy your Multi-Agent AI Processing System! 🤖✨**
