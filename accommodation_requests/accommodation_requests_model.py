from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum


class RequestStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class AccommodationRequest(BaseModel):
    id: Optional[str] = None
    guest_id: str
    host_id: str
    request_date: date
    message: Optional[str] = None
    status: RequestStatus = RequestStatus.PENDING
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AccommodationRequestResponse(BaseModel):
    id: str
    guest_id: str
    host_id: str
    requested_date: str  # ISO format date string (matching UI format)
    message: Optional[str] = None
    status: str
    created_at: str  # ISO format datetime string
    updated_at: str  # ISO format datetime string


class CreateAccommodationRequestRequest(BaseModel):
    host_id: str
    request_date: date
    message: Optional[str] = None


class UpdateAccommodationRequestStatusRequest(BaseModel):
    status: RequestStatus


class AccommodationRequestWithDetails(BaseModel):
    id: str
    guest_id: str
    host_id: str
    requested_date: str  # Matching UI format
    message: Optional[str] = None
    status: str
    created_at: str
    updated_at: str
    # Guest details
    guest_first_name: str
    guest_last_name: str
    guest_email: str
    guest_phone: Optional[str] = None
    guest_profile_image: Optional[str] = None
    # Host details
    host_user_id: str
    host_country_place_id: str
    host_city_place_id: str
    host_area: Optional[str] = None
    host_address: Optional[str] = None
    host_description: Optional[str] = None
    host_bio: Optional[str] = None
    host_max_guests: int
    host_photo_url: Optional[str] = None
