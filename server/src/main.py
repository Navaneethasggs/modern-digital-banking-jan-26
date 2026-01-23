from fastapi import FastAPI

app = FastAPI(title="NeoVault API")

@app.get("/health")
def health():
    return {"status": "ok"}
