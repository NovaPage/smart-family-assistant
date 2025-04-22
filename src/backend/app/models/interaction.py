# File: src/backend/app/models/interaction.py

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Interaction(BaseModel):
    id: UUID
    user_id: UUID
    thread_id: UUID
    message: str
    response: str
    timestamp: datetime
