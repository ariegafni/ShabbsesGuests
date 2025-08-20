from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Host(BaseModel):
    id: Optional[str] = None
    user_id: str
    country_place_id: str
    city_place_id: str
    area: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    bio: Optional[str] = None
    max_guests: int
    hosting_type: List[str] = []
    kashrut_level: Optional[str] = None
    languages: List[str] = []
    total_hostings: int = 0
    is_always_available: bool = False
    available: Optional[bool] = None
    photo_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HostResponse(BaseModel):
    id: str
    user_id: str
    country_place_id: str
    city_place_id: str
    area: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    bio: Optional[str] = None
    max_guests: int
    hosting_type: List[str] = []
    kashrut_level: Optional[str] = None
    languages: List[str] = []
    total_hostings: int
    is_always_available: bool
    available: Optional[bool] = None
    photo_url: Optional[str] = None
    created_at: str
    updated_at: str


class CreateHostRequest(BaseModel):
    country_place_id: str
    city_place_id: str
    area: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    bio: Optional[str] = None
    max_guests: int
    hosting_type: List[str] = []
    kashrut_level: Optional[str] = None
    languages: List[str] = []
    total_hostings: Optional[int] = 0
    is_always_available: Optional[bool] = False
    available: Optional[bool] = None
    photo_url: Optional[str] = None


class UpdateHostRequest(BaseModel):
    country_place_id: Optional[str] = None
    city_place_id: Optional[str] = None
    area: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    bio: Optional[str] = None
    max_guests: Optional[int] = None
    hosting_type: Optional[List[str]] = None
    kashrut_level: Optional[str] = None
    languages: Optional[List[str]] = None
    total_hostings: Optional[int] = None
    is_always_available: Optional[bool] = None
    available: Optional[bool] = None
    photo_url: Optional[str] = None


class UploadPhotoResponse(BaseModel):
    photo_url: str
