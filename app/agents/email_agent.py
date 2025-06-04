import os
import re
import datetime
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

CRM_ENDPOINT = "http://localhost:8000/crm/escalate"

def call_gemini_chat(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()

def extract_sender(email_text: str) -> str:
    match = re.search(r"From:\s*(.+)", email_text)
    return match.group(1).strip() if match else "unknown"

def extract_urgency(email_text: str) -> str:
    urgency_keywords = ['urgent', 'immediate', 'asap', 'high priority']
    return "high" if any(word in email_text.lower() for word in urgency_keywords) else "normal"

def extract_issue(email_text: str) -> str:
    # Try to extract the main request/issue from the body (after Subject or Body:)
    match = re.search(r"Body:\s*(.+)", email_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Fallback: try to find the first line after Subject
    match = re.search(r"Subject:.*\n(.+)", email_text)
    if match:
        return match.group(1).strip()
    # Fallback: return the whole text
    return email_text.strip()

def detect_tone(email_text: str) -> str:
    prompt = f"""
Detect the tone of this email. Choose one from:
[polite, angry, escalated, neutral, threatening]

Email: "{email_text[:1000]}"
Return ONLY one word.
"""
    tone = call_gemini_chat(prompt).lower()
    return tone if tone in ["polite", "angry", "escalated", "neutral", "threatening"] else "neutral"

def process_email(email_text: str) -> dict:
    sender = extract_sender(email_text)
    urgency = extract_urgency(email_text)
    issue = extract_issue(email_text)
    tone = detect_tone(email_text)

    action_taken = "logged"
    if tone in ["angry", "escalated", "threatening"] and urgency == "high":
        try:
            requests.post(CRM_ENDPOINT, json={"sender": sender, "issue": issue}, timeout=3)
            action_taken = "escalated"
        except requests.RequestException:
            action_taken = "error"

    return {
        "agent": "email_agent",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "sender": sender,
        "urgency": urgency,
        "issue": issue,
        "tone": tone,
        "action": action_taken
    }
