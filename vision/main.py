from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io
import numpy as np
from datetime import datetime

app = FastAPI()

# For MVP, we'll use a simple rule-based system
# In production, you'd load a trained model here
DISEASE_KEYWORDS = {
    "leaf_spot": ["brown spots", "circular lesions"],
    "blight": ["wilting", "dark patches"],
    "rust": ["orange pustules", "yellow spots"],
    "healthy": ["green", "no spots"]
}

def analyze_image_simple(image_data):
    """Simple image analysis - replace with real ML model"""
    # Placeholder logic
    return {
        "disease_detected": "early_blight",
        "confidence": 0.75,
        "recommendations": [
            "Remove affected leaves",
            "Apply copper-based fungicide",
            "Improve air circulation"
        ],
        "severity": "moderate"
    }

@app.get("/")
def root():
    return {"status": "ok, vision service up", "version": "1.0"}

@app.post("/detect")
async def detect_disease(file: UploadFile = File(...)):
    try:
        # Read and validate image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Analyze image
        result = analyze_image_simple(contents)
        
        return {
            "success": True,
            "filename": file.filename,
            "timestamp": datetime.utcnow().isoformat(),
            "analysis": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing failed: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "vision"}
