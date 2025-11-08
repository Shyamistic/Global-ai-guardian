from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import re

app = FastAPI()

class ScamReport(BaseModel):
    text: str
    source: str = "unknown"  # sms, call, web, etc.
    reporter_id: str = None

# Simple keyword-based scam detection
SCAM_PATTERNS = [
    r'(?i)congratulations.*won.*prize',
    r'(?i)urgent.*account.*suspended',
    r'(?i)click.*link.*verify',
    r'(?i)send.*money.*immediately',
    r'(?i)tax.*refund.*pending',
    r'(?i)lottery.*winner',
]

@app.get("/")
def root():
    return {"status": "ok, safety service up", "version": "1.0"}

@app.post("/report_scam")
async def report_scam(report: ScamReport):
    scam_score = 0
    detected_patterns = []
    
    for pattern in SCAM_PATTERNS:
        if re.search(pattern, report.text):
            scam_score += 1
            detected_patterns.append(pattern)
    
    is_scam = scam_score > 0
    risk_level = "high" if scam_score >= 2 else ("medium" if scam_score == 1 else "low")
    
    return {
        "is_scam": is_scam,
        "risk_level": risk_level,
        "confidence": min(scam_score * 0.3, 0.9),
        "detected_patterns": len(detected_patterns),
        "recommendation": "Do not respond or share personal information" if is_scam else "Appears safe",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "safety"}
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "SERVICE_NAME", "timestamp": datetime.utcnow().isoformat()}
