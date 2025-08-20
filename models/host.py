from typing import Optional

from pydantic import BaseModel


class Host(BaseModel):
    id: Optional[int] = None
    user_id: int
    area: str
    max_guests: int
    accepts_sleepover: bool
    religious_level: str
    languages: list[str]
