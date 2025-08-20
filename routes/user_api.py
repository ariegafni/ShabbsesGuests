
from flask import Blueprint, request, jsonify, g
from models.user import User
from bl.user_service import UserService
from utils.auth import require_auth

user_api = Blueprint('user_api', __name__)
user_service = UserService()

@user_api.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(**data)
    user_id = user_service.add_user(user)
    return jsonify({"id": user_id}), 201

@user_api.route("/users/login", methods=["POST"])
def login():
    data = request.json
    result = user_service.login(data["email"], data["password"])
    if result:
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401

@user_api.route("/users/me", methods=["GET"])
@require_auth
def get_my_profile():
    user = user_service.get_user(int(g.current_user_id))
    if user:
        return jsonify(user.dict())
    # Fallback minimal identity from token if DB record missing
    payload = getattr(g, "token_payload", {})
    minimal = {
        "id": int(g.current_user_id),
        "first_name": payload.get("first_name", ""),
        "last_name": payload.get("last_name", ""),
        "email": payload.get("email", ""),
    }
    return jsonify(minimal)

@user_api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = user_service.get_user(user_id)
    return jsonify(user.dict()) if user else (jsonify({"error": "User not found"}), 404)

@user_api.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    user_service.update_user(user_id, data)
    return jsonify({"message": "User updated"})

@user_api.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user_service.delete_user(user_id)
    return jsonify({"message": "User deleted"})

@user_api.route("/auth/2fa/send", methods=["POST"])
def send_2fa():
    data = request.json
    result = user_service.send_2fa(data["user_id"])
    return jsonify({"message": "2FA code sent"})

@user_api.route("/auth/2fa/verify", methods=["POST"])
def verify_2fa():
    data = request.json
    success = user_service.verify_2fa(data["user_id"], data["code"])
    if success:
        return jsonify({"message": "2FA verified"})
    return jsonify({"error": "Invalid code"}), 400

