from twilio.rest import Client
from flask import Flask, request
import requests

app = Flask(__name__)

# Make sure to replace these with your actual environment variables (do not hardcode in production!)
TWILIO_ACCOUNT_SID = 'YOUR_TWILIO_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'YOUR_TWILIO_AUTH_TOKEN'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+YOUR_TWILIO_WHATSAPP_NUMBER'

TWILIO_CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    from_number = request.form.get("From")
    message = request.form.get("Body")
    # Call FastAPI endpoint (replace with your actual endpoint URL)
    fastapi_url = "http://localhost:8000/ask"
    try:
        response = requests.post(fastapi_url, json={"question": message})
        response.raise_for_status()
        answer = response.json().get("answer", "No answer received.")
    except Exception as e:
        answer = f"Error calling FastAPI: {e}"
    
    TWILIO_CLIENT.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=from_number,
        body=answer
    )
    return "OK", 200

