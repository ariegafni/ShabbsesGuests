from pydantic import BaseModel
from typing import Optional
from datetime import date

class ThankYouNote(BaseModel):
    id: Optional[int] = None
    host_id: int
    guest_id: int
    content: str
    date_written: Optional[date] = None

