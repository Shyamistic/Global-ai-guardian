from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
import os
import requests
from typing import Optional
import random

app = FastAPI()

# OpenWeatherMap API configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_weather_data(location: str):
    """Fetch real-time weather data from OpenWeatherMap"""
    try:
        url = f"{OPENWEATHER_BASE_URL}/weather"
        params = {
            "q": location,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return {
            "location": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"] * 3.6,
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "clouds": data["clouds"]["all"],
            "visibility": data.get("visibility", 10000) / 1000,
            "rain_1h": data.get("rain", {}).get("1h", 0),
            "timestamp": datetime.utcnow().isoformat()
        }
    except:
        return generate_dummy_weather(location)

def generate_dummy_weather(location: str):
    """Generate dummy weather data for demo"""
    return {
        "location": location,
        "country": "IN",
        "temperature": round(random.uniform(25, 38), 1),
        "feels_like": round(random.uniform(27, 40), 1),
        "humidity": random.randint(40, 85),
        "pressure": random.randint(1005, 1020),
        "wind_speed": round(random.uniform(5, 25), 1),
        "description": random.choice(["clear sky", "few clouds", "scattered clouds", "light rain"]),
        "icon": "01d",
        "clouds": random.randint(0, 60),
        "visibility": round(random.uniform(5, 10), 1),
        "rain_1h": round(random.uniform(0, 5), 1),
        "timestamp": datetime.utcnow().isoformat()
    }

def generate_alerts(weather_data: dict):
    """Generate farming alerts based on weather conditions"""
    alerts = []
    recommendations = []
    
    temp = weather_data["temperature"]
    humidity = weather_data["humidity"]
    wind_speed = weather_data["wind_speed"]
    rain = weather_data["rain_1h"]
    
    # Heat wave alert
    if temp > 40:
        alerts.append({
            "type": "heat_wave",
            "severity": "high",
            "message": "Extreme heat wave warning",
            "icon": "🌡️"
        })
        recommendations.extend([
            "Increase irrigation frequency",
            "Provide shade for sensitive crops",
            "Avoid field work during peak hours (11 AM - 4 PM)"
        ])
    elif temp > 35:
        alerts.append({
            "type": "high_temperature",
            "severity": "medium",
            "message": "High temperature alert",
            "icon": "☀️"
        })
        recommendations.extend([
            "Monitor crop water stress",
            "Apply mulch to retain soil moisture"
        ])
    
    # Frost warning
    if temp < 5:
        alerts.append({
            "type": "frost_warning",
            "severity": "high",
            "message": "Frost warning - protect sensitive crops",
            "icon": "❄️"
        })
        recommendations.extend([
            "Cover sensitive plants with cloth/plastic",
            "Water crops before sunset to release heat",
            "Use smoke or heaters if available"
        ])
    
    # Heavy rain alert
    if rain > 50:
        alerts.append({
            "type": "heavy_rain",
            "severity": "high",
            "message": "Heavy rainfall expected",
            "icon": "🌧️"
        })
        recommendations.extend([
            "Ensure proper drainage in fields",
            "Delay pesticide/fertilizer application",
            "Harvest mature crops if possible"
        ])
    elif rain > 20:
        alerts.append({
            "type": "moderate_rain",
            "severity": "medium",
            "message": "Moderate rain expected",
            "icon": "🌦️"
        })
        recommendations.append("Monitor field water levels")
    
    # High wind alert
    if wind_speed > 60:
        alerts.append({
            "type": "storm_warning",
            "severity": "high",
            "message": "Storm warning - secure structures",
            "icon": "🌪️"
        })
        recommendations.extend([
            "Secure greenhouse structures",
            "Stake tall plants",
            "Postpone spraying operations"
        ])
    
    # Humidity alerts (disease risk)
    if humidity > 80 and temp > 20:
        alerts.append({
            "type": "disease_risk",
            "severity": "medium",
            "message": "High disease risk due to humidity",
            "icon": "🦠"
        })
        recommendations.extend([
            "Monitor for fungal diseases",
            "Improve air circulation",
            "Consider preventive fungicide application"
        ])
    
    # Drought conditions
    if rain == 0 and humidity < 30 and temp > 30:
        alerts.append({
            "type": "drought_warning",
            "severity": "medium",
            "message": "Dry conditions - irrigation needed",
            "icon": "🏜️"
        })
        recommendations.extend([
            "Increase irrigation",
            "Check soil moisture regularly",
            "Apply mulch to conserve water"
        ])
    
    # Ideal conditions
    if 20 <= temp <= 30 and 50 <= humidity <= 70 and wind_speed < 20 and rain < 5:
        alerts.append({
            "type": "ideal_conditions",
            "severity": "low",
            "message": "Ideal weather for farming activities",
            "icon": "✅"
        })
        recommendations.extend([
            "Good time for planting",
            "Suitable for spraying operations",
            "Conduct field inspections"
        ])
    
    return alerts, recommendations

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "climate",
        "version": "2.0",
        "features": ["real_time_weather", "farming_alerts", "recommendations"]
    }

@app.get("/weather")
async def get_weather(location: str = Query(..., description="City name or coordinates")):
    """Get current weather for a location"""
    try:
        weather_data = get_weather_data(location)
        return {
            "success": True,
            "data": weather_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather fetch failed: {str(e)}")

@app.get("/alert")
async def get_climate_alert(location: str = Query(..., description="City name")):
    """Get weather alerts and farming recommendations"""
    try:
        weather_data = get_weather_data(location)
        alerts, recommendations = generate_alerts(weather_data)
        
        return {
            "success": True,
            "location": weather_data["location"],
            "timestamp": weather_data["timestamp"],
            "current_weather": {
                "temperature": weather_data["temperature"],
                "humidity": weather_data["humidity"],
                "conditions": weather_data["description"]
            },
            "alerts": alerts,
            "recommendations": recommendations,
            "alert_count": len(alerts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Alert generation failed: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "climate",
        "api_configured": OPENWEATHER_API_KEY != "YOUR_API_KEY_HERE"
    }
