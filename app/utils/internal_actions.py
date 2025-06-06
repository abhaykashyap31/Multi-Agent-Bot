def escalate_crm(payload: dict):
    print("CRM escalation simulated:", payload)
    return {"status": "CRM escalation triggered"}

def risk_alert(payload: dict):
    print("Compliance risk simulated:", payload)
    return {"status": "Risk alert triggered"}

def log_alert(payload: dict):
    print("Log alert simulated:", payload)
    return {"status": "Alert logged"} 