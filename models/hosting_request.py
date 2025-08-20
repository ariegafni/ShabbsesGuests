from pydantic import BaseModel
from typing import Optional
from datetime import date

class HostingRequest(BaseModel):
    id: Optional[int] = None
    host_id: int
    guest_id: int
    requested_date: date
    status: str  # values: pending / accepted / declined / canceled
    message: Optional[str] = None
    