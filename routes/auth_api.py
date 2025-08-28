from flask import Blueprint, jsonify, request

from bl.user_service import UserService
from models.user import RegisterRequest, LoginRequest, RefreshRequest, ForgotPasswordRequest, ResetPasswordRequest, \
    VerifyEmailRequest
from utils.auth import require_auth

auth_api = Blueprint("auth_api", __name__)
user_service = UserService()


@auth_api.route("/auth/register", methods=["POST"])
def register():
    try:
        data = request.json or {}
        register_data = RegisterRequest(**data)
        
        auth_response = user_service.register_user(register_data)
        return jsonify(auth_response.dict()), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Registration failed"}), 500


@auth_api.route("/auth/login", methods=["POST"])
def login():
    try:
        data = request.json or {}
        login_data = LoginRequest(**data)
        
        auth_response = user_service.login_user(login_data)
        return jsonify(auth_response.dict())
        
    except ValueError as e:
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": "Login failed"}), 500


@auth_api.route("/auth/refresh", methods=["POST"])
def refresh():
    try:
        data = request.json or {}
        refresh_data = RefreshRequest(**data)
        
        auth_response = user_service.refresh_tokens(refresh_data.refresh_token)
        return jsonify(auth_response.dict())
        
    except ValueError as e:
        return jsonify({"error": "Invalid refresh token"}), 401
    except Exception as e:
        return jsonify({"error": "Token refresh failed"}), 500


@auth_api.route("/auth/logout", methods=["POST"])
@require_auth
def logout():
    # Stateless JWT: nothing to do server-side for logout
    return jsonify({"message": "Logged out"})


@auth_api.route("/auth/forgot-password", methods=["POST"])
def forgot_password():
    try:
        data = request.json or {}
        forgot_data = ForgotPasswordRequest(**data)
        
        user_service.forgot_password(forgot_data.email)
        return jsonify({"message": "Password reset email sent"})
        
    except Exception as e:
        return jsonify({"error": "Failed to send reset email"}), 500


@auth_api.route("/auth/reset-password", methods=["POST"])
def reset_password():
    try:
        data = request.json or {}
        reset_data = ResetPasswordRequest(**data)
        
        user_service.reset_password(reset_data.token, reset_data.new_password)
        return jsonify({"message": "Password reset successfully"})
        
    except Exception as e:
        return jsonify({"error": "Password reset failed"}), 500


@auth_api.route("/auth/verify-email", methods=["POST"])
def verify_email():
    try:
        data = request.json or {}
        verify_data = VerifyEmailRequest(**data)
        
        user_service.verify_email(verify_data.token)
        return jsonify({"message": "Email verified successfully"})
        
    except Exception as e:
        return jsonify({"error": "Email verification failed"}), 500


@auth_api.route("/auth/google", methods=["POST"])
def login_with_google():
    try:
        data = request.json or {}
        code = data.get("code")
        
        if not code:
            return jsonify({"error": "Google authorization code required"}), 400
        
        # TODO: Implement Google OAuth
        return jsonify({"error": "Google login not implemented yet"}), 501
        
    except Exception as e:
        return jsonify({"error": "Google login failed"}), 500


@auth_api.route("/auth/facebook", methods=["POST"])
def login_with_facebook():
    try:
        data = request.json or {}
        code = data.get("code")
        
        if not code:
            return jsonify({"error": "Facebook authorization code required"}), 400
        
        # TODO: Implement Facebook OAuth
        return jsonify({"error": "Facebook login not implemented yet"}), 501
        
    except Exception as e:
        return jsonify({"error": "Facebook login failed"}), 500


