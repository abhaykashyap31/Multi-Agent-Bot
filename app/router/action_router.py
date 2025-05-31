# app/agents/action_router.py

import requests
import datetime

ACTION_ENDPOINTS = {
    "escalate": "http://localhost:8000/crm/escalate",
    "risk_alert": "http://localhost:8000/risk_alert",
    "log": "http://localhost:8000/log"
}

def route_action(agent_data: dict, classification: dict) -> dict:
    triggered_actions = []

    fmt = classification.get("format", "").strip().lower()

    try:
        # Email: escalation based on tone
        if fmt == "email":
            if agent_data.get("tone") in ["angry", "threatening", "escalated"]:
                requests.post(ACTION_ENDPOINTS["escalate"], json=agent_data)
                triggered_actions.append("escalate")

        # JSON: anomaly alert
        elif fmt == "json" and agent_data.get("anomaly_flagged"):
            requests.post(ACTION_ENDPOINTS["log"], json=agent_data)
            triggered_actions.append("log_alert")

        # PDF: flag high-value invoice or compliance
        elif fmt == "pdf":
            if agent_data.get("risk_triggered"):
                requests.post(ACTION_ENDPOINTS["risk_alert"], json=agent_data)
                triggered_actions.append("risk_alert")

    except requests.RequestException as e:
        triggered_actions.append(f"error: {str(e)}")

    return {
        "agent": "action_router",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "actions_triggered": triggered_actions
    }
