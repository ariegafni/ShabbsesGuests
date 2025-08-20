from pydantic import BaseModel
from typing import Optional, List


class SocialLink(BaseModel):
    platform: str
    url: str


class User(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    email: str
    password: str
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    social_links: Optional[List[SocialLink]] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
