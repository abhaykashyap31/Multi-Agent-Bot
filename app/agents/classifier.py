import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def classify_input(input_text: str) -> dict:
    prompt = f"""
You are an AI classifier. Given any input (email text, JSON, or file content/filename), do the following:
- Detect the format: one of ["email", "json", "pdf"]
- Detect the business intent: one of ["RFQ", "Complaint", "Invoice", "Regulation", "Fraud Risk"]
- Detect the tone: one of ["neutral", "angry", "happy", "threatening", "escalated"]

Return the following JSON:
{{
  "classification": {{
    "format": "...",
    "intent": "...",
    "tone": "..."
  }},
  "anomaly_flagged": true/false,
  "risk_triggered": true/false
}}

Input:
{input_text}
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
