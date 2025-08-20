from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Report(BaseModel):
    id: Optional[int] = None
    reporter_id: int
    reported_user_id: int
    reason: str
    details: Optional[str] = None
    status: str = "open"  # open / resolved / dismissed
    created_at: Optional[datetime] = None