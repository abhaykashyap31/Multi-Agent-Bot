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
    trace = []

    fmt = classification.get("format", "").strip().lower()

    try:
        # Email: escalation based on tone
        if fmt == "email":
            if agent_data.get("tone") in ["angry", "threatening", "escalated"]:
                requests.post(ACTION_ENDPOINTS["escalate"], json=agent_data)
                triggered_actions.append("escalate")
                trace.append("Escalation triggered for email (angry/threatening/escalated tone).")
            else:
                trace.append("No escalation needed for email.")

        # JSON: anomaly alert
        elif fmt == "json":
            if agent_data.get("anomaly_flagged"):
                try:
                    if 'payload' in agent_data:
                        log_data = {
                            "anomaly": True,
                            "details": agent_data.get("decision_trace", []),
                            "payload": agent_data["payload"]
                        }
                        requests.post(ACTION_ENDPOINTS["log"], json=log_data, timeout=3)
                    else:
                        requests.post(ACTION_ENDPOINTS["log"], json=agent_data, timeout=3)
                    triggered_actions.append("log_alert")
                    trace.append("Log alert triggered for JSON anomaly.")
                except Exception as e:
                    trace.append(f"Error posting to log endpoint: {e}")
            else:
                trace.append("No anomaly detected in JSON.")


        # PDF: flag high-value invoice or compliance
        elif fmt == "pdf":
            if agent_data.get("risk_triggered"):
                requests.post(ACTION_ENDPOINTS["risk_alert"], json=agent_data)
                triggered_actions.append("risk_alert")
                trace.append("Risk alert triggered for PDF (invoice > 10,000 or compliance term found).")
            else:
                trace.append("No risk triggered for PDF.")

    except requests.RequestException as e:
        triggered_actions.append(f"error: {str(e)}")
        trace.append(f"Error during action routing: {str(e)}")

    return {
        "agent": "action_router",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "actions_triggered": triggered_actions,
        "decision_trace": trace
    }
