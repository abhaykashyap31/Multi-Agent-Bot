import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

def classify_input(input_text: str) -> dict:
    prompt = f"""
You are an advanced AI classifier for a multi-agent system. Given any input (email text, JSON, or PDF content/filename), do the following:
- Detect the format: one of ["email", "json", "pdf"]
- Detect the business intent: one of ["RFQ", "Complaint", "Invoice", "Regulation", "Fraud Risk"]
- Detect the tone: one of ["neutral", "angry", "happy", "threatening", "escalated"]
- If input is JSON, use schema matching to help determine format and intent.
- If input is email, look for sender, request/issue, and tone.
- If input is PDF, look for invoice or compliance keywords.

Use these few-shot examples:

Example 1:
Input:
From: John Doe <john@example.com>\nSubject: Urgent Complaint\nBody: I am very upset with your service. Please resolve this ASAP.
Output:
{{
  "classification": {{
    "format": "email",
    "intent": "Complaint",
    "tone": "angry"
  }},
  "anomaly_flagged": false,
  "risk_triggered": false
}}

Example 2:
Input:
{{"event_id": "123", "timestamp": "2024-06-01T12:00:00Z", "user_id": "u456", "amount": 15000}}
Output:
{{
  "classification": {{
    "format": "json",
    "intent": "Invoice",
    "tone": "neutral"
  }},
  "anomaly_flagged": false,
  "risk_triggered": true
}}

Example 3:
Input:
PDF file containing: Invoice Total: $12,000\nPolicy: GDPR
Output:
{{
  "classification": {{
    "format": "pdf",
    "intent": "Invoice",
    "tone": "neutral"
  }},
  "anomaly_flagged": false,
  "risk_triggered": true
}}

Now classify this input:
{input_text}
Return ONLY the JSON object as shown above.
"""

    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Attempt to extract clean JSON from Gemini's response
    try:
        # Remove Markdown formatting if it exists
        if raw.startswith("```json"):
            raw = raw.lstrip("```json").rstrip("```").strip()
        elif raw.startswith("```"):
            raw = raw.lstrip("```").rstrip("```").strip()

        parsed = json.loads(raw)

        # Safely fill in defaults if fields are missing
        classification = parsed.get("classification", {})
        return {
            "classification": {
                "format": classification.get("format", "unknown") or "unknown",
                "intent": classification.get("intent", "unknown") or "unknown",
                "tone": classification.get("tone", "neutral") or "neutral",
            },
            "anomaly_flagged": parsed.get("anomaly_flagged", False),
            "risk_triggered": parsed.get("risk_triggered", False),
            "raw_response": raw  # optional for debugging/logging
        }

    except Exception as e:
        print(f"[Gemini] Failed to parse JSON: {e}")
        return {
            "classification": {
                "format": "unknown",
                "intent": "unknown",
                "tone": "neutral"
            },
            "anomaly_flagged": False,
            "risk_triggered": False,
            "raw_response": raw
        }
