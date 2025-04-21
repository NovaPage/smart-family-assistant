# File: src/backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import endpoints

app = FastAPI(
    title="Smart Family Assistant API",
    version="1.0.0",
    description="Backend for the intelligent family assistant MVP"
)

# Optional: CORS middleware if frontend runs separately
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Change in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(endpoints.router, prefix="/api/v1")

@app.get("/ping")
def ping():
    return {"message": "pong"}
