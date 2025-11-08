from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
import hashlib
import os

app = FastAPI()

# In-memory storage for MVP (replace with MongoDB in production)
users_db = {}

class UserRegistration(BaseModel):
    name: str
    email: EmailStr
    phone: str
    location: str
    user_type: str = "farmer"  # farmer, health_worker, admin

class UserLogin(BaseModel):
    email: EmailStr
    password: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.get("/")
def root():
    return {"status": "ok, user service up", "version": "1.0"}

@app.post("/register")
async def register(user: UserRegistration):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user_id = f"user_{len(users_db) + 1}"
    users_db[user.email] = {
        "user_id": user_id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "location": user.location,
        "user_type": user.user_type,
        "created_at": datetime.utcnow().isoformat(),
        "active": True
    }
    
    return {
        "success": True,
        "user_id": user_id,
        "message": "Registration successful"
    }

@app.post("/login")
async def login(credentials: UserLogin):
    if credentials.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = users_db[credentials.email]
    return {
        "success": True,
        "user_id": user["user_id"],
        "name": user["name"],
        "token": f"demo_token_{user['user_id']}"
    }

@app.get("/profile/{user_id}")
async def get_profile(user_id: str):
    for email, user in users_db.items():
        if user["user_id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "user", "users_count": len(users_db)}
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "SERVICE_NAME", "timestamp": datetime.utcnow().isoformat()}
