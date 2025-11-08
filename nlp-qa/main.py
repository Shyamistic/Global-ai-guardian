from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok, nlp-qa up (stub)"}

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question", "")
    context = data.get("context", "")
    return {"answer": f"Stub reply to: {question} in context: {context}"}
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "SERVICE_NAME", "timestamp": datetime.utcnow().isoformat()}
