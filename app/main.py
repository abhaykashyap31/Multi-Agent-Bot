from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
import concurrent.futures
from jsonschema import validate, ValidationError

from agents.classifier import classify_input
from agents.email_agent import process_email
from agents.json_agent import process_json
from agents.pdf_agent import process_pdf
from router.action_router import route_action
from memory.memory_store import store_entry, get_all_entries

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return PlainTextResponse(str(exc), status_code=500)

@app.post("/process/email")
async def process_email_route(request: Request):
    body = await request.json()
    source = "email_upload"
    content = body.get("content", "")

    classification_result = classify_input(content)
    classification = classification_result.get("classification", {})
    anomaly_flagged = classification_result.get("anomaly_flagged", False)
    risk_triggered = classification_result.get("risk_triggered", False)
    raw_response = classification_result.get("raw_response", "")

    agent_data = process_email(content)
    actions = route_action(agent_data, classification)
    store_entry(source, classification_result, agent_data, actions)

    return {
        "classification": classification,
        "anomaly_flagged": anomaly_flagged,
        "risk_triggered": risk_triggered,
        "agent_data": agent_data,
        "agent_trace": agent_data.get("decision_trace", []),
        "action_router": actions,
        "action_trace": actions.get("decision_trace", [])
    }

EXPECTED_FIELDS = ["event_id", "timestamp", "user_id"]

@app.post("/process/json")
async def process_json_route(request: Request):
    print("Received /process/json request")
    body = await request.json()
    source = "json_webhook"
    content = body

    if not isinstance(content, dict):
        print("Input is not a dict")
        return {"error": "Input is not a valid JSON object."}

    missing_fields = [f for f in EXPECTED_FIELDS if f not in content]
    print(f"Missing fields: {missing_fields}")

    if not missing_fields:
        def classify_with_timeout():
            print("Calling classifier...")
            return classify_input(json.dumps(content))
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(classify_with_timeout)
            try:
                classification_result = future.result(timeout=10)
                print("Classifier result:", classification_result)
            except concurrent.futures.TimeoutError:
                print("Classifier timed out")
                return {"error": "Classifier timed out."}
            except Exception as e:
                print("Classifier error:", e)
                return {"error": f"Classifier error: {str(e)}"}
        classification = classification_result.get("classification", {})
        anomaly_flagged = classification_result.get("anomaly_flagged", False)
        risk_triggered = classification_result.get("risk_triggered", False)
        raw_response = classification_result.get("raw_response", "")
    else:
        classification = {"format": "json", "intent": "unknown", "tone": "neutral"}
        anomaly_flagged = True
        risk_triggered = False
        raw_response = f"Missing fields: {missing_fields}"

    print("Running JSON agent...")
    agent_data = process_json(content)
    print("Agent data:", agent_data)

    print("Routing actions...")
    actions = route_action(agent_data, classification)
    print("Actions:", actions)

    print("Storing entry in memory...")
    store_entry(source, {
        "classification": classification,
        "anomaly_flagged": anomaly_flagged,
        "risk_triggered": risk_triggered,
        "raw_response": raw_response
    }, agent_data, actions)

    print("Returning response")
    return {
        "classification": classification,
        "anomaly_flagged": anomaly_flagged,
        "risk_triggered": risk_triggered,
        "agent_data": agent_data,
        "agent_trace": agent_data.get("decision_trace", []),
        "action_router": actions,
        "action_trace": actions.get("decision_trace", [])
    }

@app.post("/process/pdf")
async def process_pdf_route(file: UploadFile = File(...)):
    source = "pdf_upload"
    content = await file.read()

    classification_result = classify_input(content)
    classification = classification_result.get("classification", {})
    anomaly_flagged = classification_result.get("anomaly_flagged", False)
    risk_triggered = classification_result.get("risk_triggered", False)
    raw_response = classification_result.get("raw_response", "")

    agent_data = process_pdf(content)
    actions = route_action(agent_data, classification)
    store_entry(source, classification_result, agent_data, actions)

    return {
        "classification": classification,
        "anomaly_flagged": anomaly_flagged,
        "risk_triggered": risk_triggered,
        "agent_data": agent_data,
        "agent_trace": agent_data.get("decision_trace", []),
        "action_router": actions,
        "action_trace": actions.get("decision_trace", [])
    }

@app.get("/memory")
def get_memory():
    raw_entries = get_all_entries()
    
    cleaned_entries = []
    for entry in raw_entries:
        cleaned_entry = list(entry)  # convert tuple to list if needed
        try:
            cleaned_entry[3] = json.loads(cleaned_entry[3])
        except (json.JSONDecodeError, TypeError):
            pass
        try:
            cleaned_entry[4] = json.loads(cleaned_entry[4])
        except (json.JSONDecodeError, TypeError):
            pass
        try:
            cleaned_entry[5] = json.loads(cleaned_entry[5])
        except (json.JSONDecodeError, TypeError):
            pass
        cleaned_entries.append(cleaned_entry)
    
    return JSONResponse(content=cleaned_entries)

@app.post("/crm/escalate")
def escalate_crm(payload: dict):
    print("CRM escalation simulated:", payload)
    return {"status": "CRM escalation triggered"}

@app.post("/risk_alert")
def risk_alert(payload: dict):
    print("Compliance risk simulated:", payload)
    return {"status": "Risk alert triggered"}

@app.post("/log")
def log_alert(payload: dict):
    print("Log alert simulated:", payload)
    return {"status": "Alert logged"}

if __name__ == "__main__":
    import uvicorn
    Port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=Port, reload=True)
