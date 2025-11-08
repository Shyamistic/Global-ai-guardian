from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime

app = FastAPI(title="AI Guardian Gateway", version="1.0")

# CORS settings for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URLS = {
    "nlp": "http://nlp-qa:8000",
    "vision": "http://vision:8000",
    "climate": "http://climate:8000",
    "safety": "http://safety:8000",
    "user": "http://user:8000",
    "dashboard": "http://dashboard:8000",
}

@app.get("/")
async def root():
    return {
        "status": "ok, AI Guardian Gateway",
        "version": "1.0",
        "timestamp": datetime.utcnow().isoformat(),
        "services": list(BASE_URLS.keys())
    }

@app.get("/health")
async def health_check():
    health_status = {}
    async with httpx.AsyncClient(timeout=5.0) as client:
        for service, url in BASE_URLS.items():
            try:
                resp = await client.get(f"{url}/health")
                resp.raise_for_status()
                health_status[service] = resp.json()
            except Exception as e:
                health_status[service] = {"status": "unavailable", "error": str(e)}
    return health_status

# NLP/QA Route
@app.post("/ask")
async def ask(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{BASE_URLS['nlp']}/ask", json=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"NLP service error: {str(e)}")

# Vision Route
@app.post("/detect_disease")
async def detect_disease(file: UploadFile = File(...)):
    async with httpx.AsyncClient() as client:
        try:
            files = {"file": (file.filename, await file.read(), file.content_type)}
            resp = await client.post(f"{BASE_URLS['vision']}/detect", files=files)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Vision service error: {str(e)}")

# Climate Route
@app.post("/climate/alert")
async def climate_alert(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{BASE_URLS['climate']}/alert", json=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Climate service error: {str(e)}")

# Safety Route
@app.post("/safety/report")
async def report_scam(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{BASE_URLS['safety']}/report_scam", json=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Safety service error: {str(e)}")

# User Register Route
@app.post("/user/register")
async def register_user(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{BASE_URLS['user']}/register", json=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"User register error: {str(e)}")

# User Login Route
@app.post("/user/login")
async def login_user(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{BASE_URLS['user']}/login", json=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"User login error: {str(e)}")
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "SERVICE_NAME", "timestamp": datetime.utcnow().isoformat()}
