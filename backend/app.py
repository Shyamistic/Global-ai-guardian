from fastapi import FastAPI, File, UploadFile, Form
from transformers import pipeline
import requests
import os

app = FastAPI()
nlp_model = pipeline("question-answering", model="distilbert-base-uncased", tokenizer="distilbert-base-uncased")

@app.post("/ask")
async def ask(question: str = Form(...)):
    res = nlp_model({'question': question, 'context': "Weather, health, safety, crop info"})
    return {"answer": res["answer"]}

@app.post("/detect_disease")
async def detect_disease(img: UploadFile = File(...)):
    # You would load your YOLO/MobileNet model here, mock for MVP
    return {"disease": "No disease detected (demo)"}

@app.get("/weather_alerts")
async def get_alerts(location: str):
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    data = requests.get(url).json()
    alert = None
    if data["main"]["temp"] > 310:
        alert = "Extreme heat alert!"
    return {"location": location, "weather": data, "alert": alert }
