from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class GenerateBudgetRequest(BaseModel):
    save: bool = False

@app.post("/test-default")
def test_default(request: GenerateBudgetRequest = GenerateBudgetRequest()):
    return {"save": request.save}

@app.post("/test-nodefault")
def test_nodefault(request: GenerateBudgetRequest):
    return {"save": request.save}

client = TestClient(app)
print("Default with body:", client.post("/test-default", json={"save": True}).json())
print("No default with body:", client.post("/test-nodefault", json={"save": True}).json())
