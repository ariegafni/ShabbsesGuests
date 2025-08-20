from flask import Blueprint, jsonify, request
from models.user import User
from bl.user_service import UserService
from utils.auth import create_access_and_refresh_tokens, decode_token

auth_api = Blueprint("auth_api", __name__)
user_service = UserService()


@auth_api.route("/auth/register", methods=["POST"])
def register():
    data = request.json or {}
    required_fields = ["first_name", "last_name", "email", "password"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    # In a real app, hash the password and save to DB. For infrastructure setup, skip DB persist.
    user = User(**data)
    user_id = 1
    access_token, refresh_token = create_access_and_refresh_tokens(
        user_id,
        {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
    )
    return (
        jsonify(
            {
                "user": {"id": user_id, "email": user.email, "first_name": user.first_name, "last_name": user.last_name},
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
            }
        ),
        201,
    )


@auth_api.route("/auth/login", methods=["POST"])
def login():
    data = request.json or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    # Replace with real credential validation
    if not user_service.login(email, password):
        return jsonify({"error": "Invalid credentials"}), 401
    # Demo: get a user to bind token. Here we just fake user id 1
    user = user_service.get_user(1) or User(id=1, first_name="Demo", last_name="User", email=email, password="")
    access_token, refresh_token = create_access_and_refresh_tokens(
        int(user.id),
        {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
    )
    return jsonify(
        {
            "user": {"id": user.id, "email": user.email, "first_name": user.first_name, "last_name": user.last_name},
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }
    )


@auth_api.route("/auth/refresh", methods=["POST"])
def refresh():
    data = request.json or {}
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        return jsonify({"error": "refresh_token is required"}), 400
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        return jsonify({"error": "Invalid token"}), 401
    user_id = int(payload.get("sub"))
    from utils.auth import create_access_and_refresh_tokens

    access_token, new_refresh_token = create_access_and_refresh_tokens(user_id)
    return jsonify(
        {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "Bearer",
        }
    )


@auth_api.route("/auth/logout", methods=["POST"])
def logout():
    # Stateless JWT: nothing to do server-side for logout in this simple setup
    return jsonify({"message": "Logged out"})


