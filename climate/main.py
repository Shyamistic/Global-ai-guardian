from fastapi import FastAPI, HTTPException
import requests
import os
from datetime import datetime

app = FastAPI()

# Use free weather API (OpenWeatherMap or WeatherAPI)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "demo_key")
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

@app.get("/")
def root():
    return {"status": "ok, climate service up", "version": "1.0"}

@app.post("/alert")
async def get_climate_alert(location: dict):
    try:
        loc = location.get("location", "Delhi")
        
        # For demo without API key
        if WEATHER_API_KEY == "demo_key":
            return generate_demo_alert(loc)
        
        # Real API call
        response = requests.get(
            WEATHER_API_URL,
            params={"key": WEATHER_API_KEY, "q": loc, "aqi": "yes"}
        )
        data = response.json()
        
        alerts = []
        temp_c = data["current"]["temp_c"]
        
        if temp_c > 40:
            alerts.append({
                "type": "extreme_heat",
                "severity": "high",
                "message": f"Extreme heat warning: {temp_c}°C. Avoid outdoor work during peak hours."
            })
        elif temp_c > 35:
            alerts.append({
                "type": "high_heat",
                "severity": "medium",
                "message": f"High temperature: {temp_c}°C. Stay hydrated."
            })
        
        # Check AQI
        aqi = data["current"].get("air_quality", {}).get("pm2_5", 0)
        if aqi > 150:
            alerts.append({
                "type": "air_quality",
                "severity": "high",
                "message": "Poor air quality. Wear mask if going outdoors."
            })
        
        return {
            "location": loc,
            "timestamp": datetime.utcnow().isoformat(),
            "current_weather": {
                "temp_c": temp_c,
                "condition": data["current"]["condition"]["text"],
                "humidity": data["current"]["humidity"]
            },
            "alerts": alerts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather API error: {str(e)}")

def generate_demo_alert(location):
    """Demo data when API key not available"""
    return {
        "location": location,
        "timestamp": datetime.utcnow().isoformat(),
        "current_weather": {
            "temp_c": 32,
            "condition": "Partly cloudy",
            "humidity": 65
        },
        "alerts": [
            {
                "type": "demo",
                "severity": "info",
                "message": "This is demo data. Set WEATHER_API_KEY for real alerts."
            }
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "climate"}
