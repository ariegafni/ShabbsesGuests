from pydantic import BaseModel
from typing import Optional

class Guest(BaseModel):
    id: Optional[int] = None
    user_id: int
    notes: Optional[str] = None