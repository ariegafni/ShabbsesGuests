from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class SocialLink(BaseModel):
    platform: str
    url: str


class User(BaseModel):
    id: Optional[str] = None  # שינוי ל-string כמו ב-UI
    first_name: str
    last_name: str
    email: EmailStr
    password_hash: str
    phone: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    social_links: Optional[List[SocialLink]] = []
    is_verified: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    social_links: Optional[List[SocialLink]] = []
    is_verified: bool
    created_at: str
    updated_at: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    profile_image: Optional[str] = None


class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class VerifyEmailRequest(BaseModel):
    token: str
