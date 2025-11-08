from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import httpx
import os

app = FastAPI(title="AI Guardian Gateway", version="2.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs (update these with your Railway URLs)
BASE_URLS = {
    "nlp": os.getenv("NLP_SERVICE_URL", "http://nlp-qa:8000"),
    "vision": os.getenv("VISION_SERVICE_URL", "http://vision:8000"),
    "climate": os.getenv("CLIMATE_SERVICE_URL", "http://climate:8000"),
    "safety": os.getenv("SAFETY_SERVICE_URL", "http://safety:8000"),
    "user": os.getenv("USER_SERVICE_URL", "http://user:8000"),
    "dashboard": os.getenv("DASHBOARD_SERVICE_URL", "http://dashboard:8000"),
}

@app.get("/")
def root():
    return {
        "status": "ok, AI Guardian Gateway",
        "version": "2.0",
        "timestamp": datetime.utcnow().isoformat(),
        "services": list(BASE_URLS.keys())
    }

@app.get("/health")
async def health_check():
    """Check health of all services"""
    health_status = {}
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        for service_name, base_url in BASE_URLS.items():
            try:
                response = await client.get(f"{base_url}/health")
                health_status[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "response_time_ms": response.elapsed.total_seconds() * 1000
                }
            except:
                health_status[service_name] = {
                    "status": "unreachable",
                    "response_time_ms": None
                }
    
    return {
        "gateway": "healthy",
        "services": health_status,
        "timestamp": datetime.utcnow().isoformat()
    }

# Vision Service Routes
@app.post("/vision/detect")
async def detect_disease(file: UploadFile = File(...)):
    """Forward disease detection to vision service"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        files = {"file": (file.filename, await file.read(), file.content_type)}
        response = await client.post(f"{BASE_URLS['vision']}/detect", files=files)
        return response.json()

@app.get("/vision/diseases")
async def list_diseases():
    """List all detectable diseases"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{BASE_URLS['vision']}/diseases")
        return response.json()

# Climate Service Routes
@app.get("/climate/weather")
async def get_weather(location: str):
    """Get weather data"""
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(f"{BASE_URLS['climate']}/weather", params={"location": location})
        return response.json()

@app.get("/climate/alert")
async def get_climate_alert(location: str):
    """Get climate alerts"""
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(f"{BASE_URLS['climate']}/alert", params={"location": location})
        return response.json()

# Safety Service Routes
@app.post("/safety/check")
async def check_safety(request: Request):
    """Check for scams and phishing"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        data = await request.json()
        response = await client.post(f"{BASE_URLS['safety']}/check", json=data)
        return response.json()

# User Service Routes
@app.post("/user/register")
async def register_user(request: Request):
    """Register new user"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        data = await request.json()
        response = await client.post(f"{BASE_URLS['user']}/register", json=data)
        return response.json()

@app.post("/user/login")
async def login_user(request: Request):
    """User login"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        data = await request.json()
        response = await client.post(f"{BASE_URLS['user']}/login", json=data)
        return response.json()

@app.get("/user/profile/{email}")
async def get_user_profile(email: str):
    """Get user profile"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{BASE_URLS['user']}/profile/{email}")
        return response.json()
