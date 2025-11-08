from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok, federated up"}

@app.post("/train_update")
async def update(request: Request):
    # Demo accept edge model diff
    data = await request.json()
    return {"status": "received", "diff": data}
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "SERVICE_NAME", "timestamp": datetime.utcnow().isoformat()}
