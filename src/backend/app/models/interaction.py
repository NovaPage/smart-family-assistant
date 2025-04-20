# File: src/backend/app/models/interaction.py

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, timezone


class Interaction(BaseModel):
    user_id: UUID
    message: str
    response: str
    timestamp: datetime
