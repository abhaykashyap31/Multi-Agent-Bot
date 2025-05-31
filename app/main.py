from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime

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
        "raw_response": raw_response,
        "actions": actions
    }

@app.post("/process/json")
async def process_json_route(request: Request):
    body = await request.json()
    source = "json_webhook"
    content = body

    classification_result = classify_input(json.dumps(content))
    classification = classification_result.get("classification", {})
    anomaly_flagged = classification_result.get("anomaly_flagged", False)
    risk_triggered = classification_result.get("risk_triggered", False)
    raw_response = classification_result.get("raw_response", "")

    agent_data = process_json(content)
    actions = route_action(agent_data, classification)
    store_entry(source, classification_result, agent_data, actions)

    return {
        "classification": classification,
        "anomaly_flagged": anomaly_flagged,
        "risk_triggered": risk_triggered,
        "raw_response": raw_response,
        "actions": actions
    }

@app.post("/process/pdf")
async def process_pdf_route(file: UploadFile = File(...)):
    source = "pdf_upload"
    content = await file.read()

    classification_result = classify_input(file.filename)
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
        "raw_response": raw_response,
        "actions": actions
    }

@app.get("/memory")
def get_memory():
    return get_all_entries()

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
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
