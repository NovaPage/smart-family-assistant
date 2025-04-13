from fastapi import FastAPI
from app.api.v1.router import router as api_router
from app.core.config import load_env

app = FastAPI()

load_env()
app.include_router(api_router)
