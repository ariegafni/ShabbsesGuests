from pydantic import BaseModel
from typing import Optional
from datetime import date

class Availability(BaseModel):
    id: Optional[int] = None
    host_id: int
    date: date
    max_guests: int
    notes: Optional[str] = None