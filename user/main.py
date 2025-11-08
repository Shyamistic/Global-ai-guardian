from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional
import hashlib
import secrets
import jwt

app = FastAPI()

# Secret key for JWT (in production, use environment variable)
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# In-memory user database (replace with MongoDB in production)
users_db = {}
sessions_db = {}

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    location: Optional[str] = None
    language: str = "en"
    role: str = "farmer"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    language: Optional[str] = None

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "user",
        "version": "2.0",
        "features": ["registration", "authentication", "profile_management"]
    }

@app.post("/register")
async def register_user(user: UserRegister):
    """Register a new user"""
    # Check if user exists
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user_id = secrets.token_urlsafe(16)
    users_db[user.email] = {
        "user_id": user_id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "password_hash": hash_password(user.password),
        "location": user.location,
        "language": user.language,
        "role": user.role,
        "created_at": datetime.utcnow().isoformat(),
        "is_active": True
    }
    
    # Create access token
    access_token = create_access_token({"sub": user.email, "user_id": user_id})
    
    return {
        "success": True,
        "message": "User registered successfully",
        "user_id": user_id,
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/login")
async def login_user(credentials: UserLogin):
    """User login"""
    # Check if user exists
    if credentials.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = users_db[credentials.email]
    
    # Verify password
    if user["password_hash"] != hash_password(credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check if user is active
    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="Account deactivated")
    
    # Create access token
    access_token = create_access_token({
        "sub": credentials.email,
        "user_id": user["user_id"]
    })
    
    # Store session
    sessions_db[access_token] = {
        "user_id": user["user_id"],
        "email": credentials.email,
        "login_time": datetime.utcnow().isoformat()
    }
    
    return {
        "success": True,
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user["user_id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }

@app.get("/profile/{email}")
async def get_profile(email: str):
    """Get user profile"""
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[email]
    
    # Return user profile (without password)
    return {
        "success": True,
        "profile": {
            "user_id": user["user_id"],
            "name": user["name"],
            "email": user["email"],
            "phone": user["phone"],
            "location": user.get("location"),
            "language": user["language"],
            "role": user["role"],
            "created_at": user["created_at"]
        }
    }

@app.put("/profile/{email}")
async def update_profile(email: str, profile: UserProfile):
    """Update user profile"""
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[email]
    
    # Update fields
    if profile.name:
        user["name"] = profile.name
    if profile.phone:
        user["phone"] = profile.phone
    if profile.location:
        user["location"] = profile.location
    if profile.language:
        user["language"] = profile.language
    
    user["updated_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "message": "Profile updated successfully",
        "profile": {
            "name": user["name"],
            "phone": user["phone"],
            "location": user.get("location"),
            "language": user["language"]
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "user",
        "total_users": len(users_db),
        "active_sessions": len(sessions_db)
    }
