from flask import Blueprint, request, jsonify, g
from users.user_service import UserService
from utils.auth import require_auth


user_api = Blueprint('user_api', __name__)
user_service = UserService()


@user_api.route("/users/me", methods=["GET"])
@require_auth
def get_my_profile():
    try:
        user = user_service.get_user_by_id(str(g.current_user_id))
        if user:
            return jsonify(user.model_dump())
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to fetch user profile"}), 500


@user_api.route("/users/me", methods=["PUT"])
@require_auth
def update_my_profile():
    try:
        data = request.json or {}
        # Remove sensitive fields that shouldn't be updated via this endpoint
        data.pop('password', None)
        data.pop('id', None)
        data.pop('email', None)  # Email should be updated via separate endpoint
        
        user = user_service.update_user(str(g.current_user_id), data)
        return jsonify(user.model_dump())
    except Exception as e:
        return jsonify({"error": "Failed to update user profile"}), 500


@user_api.route("/users/me", methods=["DELETE"])
@require_auth
def delete_my_account():
    try:
        user_service.delete_user(str(g.current_user_id))
        return jsonify({"message": "Account deleted successfully"})
    except Exception as e:
        return jsonify({"error": "Failed to delete account"}), 500


@user_api.route("/users/change-password", methods=["PUT"])
@require_auth
def change_password():
    try:
        data = request.json or {}
        current_password = data.get("current_password")
        new_password = data.get("new_password")
        
        if not current_password or not new_password:
            return jsonify({"error": "Current password and new password are required"}), 400
        
        # TODO: Implement password change logic
        # For now, just return success
        return jsonify({"message": "Password changed successfully"})
    except Exception as e:
        return jsonify({"error": "Failed to change password"}), 500


@user_api.route("/users/upload-profile-image", methods=["POST"])
@require_auth
def upload_profile_image():
    try:
        # TODO: Implement file upload logic
        # For now, just return success
        return jsonify({"profile_image": "https://example.com/profile.jpg"})
    except Exception as e:
        return jsonify({"error": "Failed to upload profile image"}), 500

