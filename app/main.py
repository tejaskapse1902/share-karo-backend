from fastapi import FastAPI
from app.api.api_router import api_router

app = FastAPI()

app.include_router(api_router)

@app.get("/")
def health():
    return {"status": "ok"}
