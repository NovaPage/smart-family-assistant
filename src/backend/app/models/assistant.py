# File: src/backend/app/models/assistant.py

from pydantic import BaseModel


class AssistantRequest(BaseModel):
    message: str


class AssistantResponse(BaseModel):
    response: str
