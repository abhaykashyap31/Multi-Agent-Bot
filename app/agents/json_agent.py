import datetime
import requests
from jsonschema import validate, ValidationError

ALERT_ENDPOINT = "http://localhost:8000/log"

EXPECTED_SCHEMA = {
    "type": "object",
    "properties": {
        "event_id": {"type": "string"},
        "timestamp": {"type": "string"},
        "user_id": {"type": "string"},
        "amount": {"type": "number"}
    },
    "required": ["event_id", "timestamp", "user_id"]
}

def process_json(json_payload: dict) -> dict:
    status = "valid"
    alert = False

    try:
        validate(instance=json_payload, schema=EXPECTED_SCHEMA)
    except ValidationError as ve:
        status = "invalid"
        alert = True
        try:
            requests.post(ALERT_ENDPOINT, json={"error": str(ve), "data": json_payload}, timeout=3)
        except requests.RequestException:
            pass

    return {
        "agent": "json_agent",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "schema_status": status,
        "anomaly_flagged": alert,
        "payload": json_payload
    }
