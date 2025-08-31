from users.user_model import User, UserResponse, LoginRequest, RegisterRequest, AuthResponse
from users.user_repository import UserRepository
from utils.auth import hash_password, verify_password, create_access_and_refresh_tokens
from typing import Optional


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def register_user(self, user_data: RegisterRequest) -> AuthResponse:
        # Check if email already exists
        if self.repo.email_exists(user_data.email):
            raise ValueError("Email already exists")
        
        # Hash the password
        hashed_password = hash_password(user_data.password)
        
        # Create user object
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password_hash=hashed_password,
            phone=user_data.phone,
            country=user_data.country,
            city=user_data.city,
            profile_image=user_data.profile_image,
            is_verified=False
        )
        
        # Save to database
        user_id = self.repo.add(user)
        
        # Get the created user
        user_response = self.repo.get_by_id(user_id)
        if not user_response:
            raise Exception("Failed to create user")
        
        # Create tokens
        access_token, refresh_token = create_access_and_refresh_tokens(
            user_id,
            {
                "email": user_response.email,
                "first_name": user_response.first_name,
                "last_name": user_response.last_name,
            }
        )
        
        return AuthResponse(
            user=user_response,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )

    def login_user(self, login_data: LoginRequest) -> AuthResponse:
        # Get user with password
        user = self.repo.get_by_email_with_password(login_data.email)
        if not user:
            raise ValueError("Invalid credentials")
        
        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            raise ValueError("Invalid credentials")
        
        # Get user response (without password)
        user_response = self.repo.get_by_id(user.id)
        if not user_response:
            raise Exception("User not found")
        
        # Create tokens
        access_token, refresh_token = create_access_and_refresh_tokens(
            user.id,
            {
                "email": user_response.email,
                "first_name": user_response.first_name,
                "last_name": user_response.last_name,
            }
        )
        
        return AuthResponse(
            user=user_response,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )

    def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        return self.repo.get_by_id(user_id)

    def update_user(self, user_id: str, data: dict) -> UserResponse:
        self.repo.update(user_id, data)
        user = self.repo.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        return user

    def delete_user(self, user_id: str):
        self.repo.delete(user_id)

    def refresh_tokens(self, refresh_token: str) -> AuthResponse:
        from utils.auth import decode_token
        
        # Decode refresh token
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")
        
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Invalid token payload")
        
        # Get user
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Create new tokens
        access_token, new_refresh_token = create_access_and_refresh_tokens(
            user_id,
            {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )
        
        return AuthResponse(
            user=user,
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="Bearer"
        )

    def forgot_password(self, email: str) -> bool:
        # Check if user exists
        user = self.repo.get_by_email(email)
        if not user:
            # Don't reveal if email exists or not for security
            return True
        
        # TODO: Send email with reset token
        # For now, just return success
        return True

    def reset_password(self, token: str, new_password: str) -> bool:
        # TODO: Validate reset token and update password
        # For now, just return success
        return True

    def verify_email(self, token: str) -> bool:
        # TODO: Validate verification token and mark email as verified
        # For now, just return success
        return True
