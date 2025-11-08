from fastapi import FastAPI
from datetime import datetime, timedelta
import random

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok, dashboard service up", "version": "1.0"}

@app.get("/stats")
async def get_stats():
    """Returns platform usage statistics"""
    return {
        "total_users": random.randint(1000, 5000),
        "active_today": random.randint(100, 500),
        "disease_detections": random.randint(50, 200),
        "climate_alerts": random.randint(10, 50),
        "scam_reports": random.randint(5, 20),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/activity")
async def get_activity():
    """Returns recent activity feed"""
    activities = []
    for i in range(10):
        activities.append({
            "id": f"act_{i}",
            "type": random.choice(["disease_detection", "climate_alert", "user_registration", "scam_report"]),
            "timestamp": (datetime.utcnow() - timedelta(minutes=i*15)).isoformat(),
            "location": random.choice(["Delhi", "Mumbai", "Bangalore", "Punjab", "Bihar"])
        })
    return {"activities": activities}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "dashboard"}
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "SERVICE_NAME", "timestamp": datetime.utcnow().isoformat()}
