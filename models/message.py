from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Message(BaseModel):
    id: Optional[int] = None
    sender_id: int
    receiver_id: int
    thread_id: Optional[str] = None
    content: str
    timestamp: Optional[datetime] = None