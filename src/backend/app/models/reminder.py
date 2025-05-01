# File: src/backend/app/models/reminder.py

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, Literal


class ReminderStatus:
    PENDING = "pending"
    SENT = "sent"


class Reminder(BaseModel):
    id: UUID
    user_id: UUID
    text: str
    hour: str  # Expected format: "HH:MM"
    reminder_date: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    sent_at: Optional[datetime] = None
    status: Literal["pending", "sent"] = ReminderStatus.PENDING
    channel: Literal["telegram", "web"]
    chat_id: Optional[int] = None
