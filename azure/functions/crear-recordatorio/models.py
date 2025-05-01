from datetime import datetime
from pydantic import BaseModel

class Reminder(BaseModel):
    user_id: str
    chat_id: int
    text: str
    hour: str
    channel: str
    status: str
    created_at: datetime
