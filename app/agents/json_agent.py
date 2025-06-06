import datetime
import threading
from utils.internal_actions import log_alert

REQUIRED_FIELDS = ["event_id", "timestamp", "user_id"]

def send_alert_async(payload):
    def _send():
        try:
            log_alert(payload)
        except Exception:
            pass
    threading.Thread(target=_send, daemon=True).start()

def process_json(json_payload: dict) -> dict:
    status = "valid"
    alert = False
    trace = []
    missing_fields = [f for f in REQUIRED_FIELDS if f not in json_payload]
    if missing_fields:
        status = "invalid"
        alert = True
        trace.append(f"Missing required fields: {missing_fields}")
        send_alert_async({"error": f"Missing fields: {missing_fields}", "data": json_payload})
    else:
        trace.append("All required fields present.")
    return {
        "agent": "json_agent",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "schema_status": status,
        "anomaly_flagged": alert,
        "payload": json_payload,
        "decision_trace": trace
    }
