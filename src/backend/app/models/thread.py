from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field

class ThreadStatus:
    OPEN = "open"
    CLOSED = "closed"

class ThreadSource:
    WEB = "web"
    TELEGRAM = "telegram"

class ThreadCreate(BaseModel):
    user_id: str
    source: Literal["web", "telegram"]
    summary: Optional[str] = None
    openai_thread_id: str

class ThreadInDB(BaseModel):
    id: str 
    user_id: str
    source: Literal["web", "telegram"]
    status: Literal["open", "closed"] = ThreadStatus.OPEN
    started_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    summary: Optional[str] = None
    openai_thread_id: Optional[str] = None

    class Config:
        from_attributes = True
