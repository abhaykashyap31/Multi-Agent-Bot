import fitz  # PyMuPDF
import datetime
import re
import requests
from io import BytesIO

RISK_ALERT_ENDPOINT = "http://localhost:8000/risk_alert"
COMPLIANCE_TERMS = ["GDPR", "FDA", "HIPAA"]

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=BytesIO(file_bytes), filetype="pdf")
        text = "".join([page.get_text() for page in doc])
        doc.close()
        return text
    except Exception:
        return ""

def extract_invoice_total(text: str) -> float:
    match = re.search(r'Total\s*[:\-]?\s*\$?([\d,]+\.\d{2})', text, re.IGNORECASE)
    return float(match.group(1).replace(",", "")) if match else 0.0

def detect_compliance_keywords(text: str) -> list:
    return [term for term in COMPLIANCE_TERMS if term in text.upper()]

def process_pdf(file_bytes: bytes) -> dict:
    text = extract_text_from_pdf(file_bytes)
    total = extract_invoice_total(text)
    compliance_flags = detect_compliance_keywords(text)

    triggered = total > 10000 or bool(compliance_flags)
    trace = [f"Extracted total: {total}", f"Compliance mentions: {compliance_flags}"]
    if total > 10000:
        trace.append("Invoice total exceeds 10,000. Risk triggered.")
    if compliance_flags:
        trace.append(f"Compliance terms found: {compliance_flags}. Risk triggered.")
    if triggered:
        try:
            requests.post(RISK_ALERT_ENDPOINT, json={
                "total": total,
                "compliance_flags": compliance_flags
            }, timeout=3)
            trace.append("Risk alert sent to endpoint.")
        except requests.RequestException:
            trace.append("Failed to send risk alert to endpoint.")

    return {
        "agent": "pdf_agent",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "invoice_total": total,
        "compliance_mentions": compliance_flags,
        "risk_triggered": triggered,
        "decision_trace": trace
    }
