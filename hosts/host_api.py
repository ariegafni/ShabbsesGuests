from flask import Blueprint, request, jsonify, g

from hosts.host_service import HostService
from hosts.host_model import CreateHostRequest, UpdateHostRequest
from utils.auth import require_auth

host_api = Blueprint('host_api', __name__)
host_service = HostService()


@host_api.route("/hosts", methods=["GET"])
def get_all_hosts():
    """Get all hosts (public)"""
    try:
        hosts = host_service.get_all_hosts()
        return jsonify([host.model_dump() for host in hosts])
    except Exception as e:
        return jsonify({"error": "Failed to fetch hosts"}), 500


@host_api.route("/hosts/country/<country_place_id>", methods=["GET"])
def get_hosts_by_country(country_place_id):
    """Get hosts by country (public)"""
    try:
        hosts = host_service.get_hosts_by_country(country_place_id)
        return jsonify([host.model_dump() for host in hosts])
    except Exception as e:
        return jsonify({"error": "Failed to fetch hosts by country"}), 500


@host_api.route("/hosts/<host_id>", methods=["GET"])
def get_host_by_id(host_id):
    """Get host by ID (public)"""
    try:
        host = host_service.get_host_by_id(host_id)
        if not host:
            return jsonify({"error": "Host not found"}), 404
        return jsonify(host.model_dump())
    except Exception as e:
        return jsonify({"error": "Failed to fetch host"}), 500


@host_api.route("/hosts/me", methods=["GET"])
@require_auth
def get_my_host_profile():
    """Get current user's host profile (protected)"""
    try:
        host = host_service.get_host_by_user_id(str(g.current_user_id))
        if not host:
            return jsonify({"error": "Host profile not found"}), 404
        return jsonify(host.model_dump())
    except Exception as e:
        return jsonify({"error": "Failed to fetch host profile"}), 500


@host_api.route("/hosts", methods=["POST"])
@require_auth
def create_host():
    """Create host profile for current user (protected)"""
    try:
        data = request.json or {}
        host_data = CreateHostRequest(**data)
        
        host = host_service.create_host(str(g.current_user_id), host_data)
        return jsonify(host.model_dump()), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to create host profile"}), 500


@host_api.route("/hosts/<host_id>", methods=["PUT"])
@require_auth
def update_host(host_id):
    """Update host profile (protected)"""
    try:
        data = request.json or {}
        host_data = UpdateHostRequest(**data)
        
        host = host_service.update_host(host_id, str(g.current_user_id), host_data)
        return jsonify(host.model_dump())
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to update host profile"}), 500


@host_api.route("/hosts/<host_id>", methods=["DELETE"])
@require_auth
def delete_host(host_id):
    """Delete host profile (protected)"""
    try:
        host_service.delete_host(host_id, str(g.current_user_id))
        return jsonify({"message": "Host profile deleted successfully"})
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to delete host profile"}), 500


@host_api.route("/hosts/upload-photo", methods=["POST"])
@require_auth
def upload_host_photo():
    """Upload host photo (protected)"""
    try:
        # Check if file was uploaded
        if 'photo' not in request.files:
            return jsonify({"error": "No photo file provided"}), 400
        
        file = request.files['photo']
        if file.filename == '':
            return jsonify({"error": "No photo file selected"}), 400
        
        # For now, just return a mock response
        # In a real implementation, you would save the file
        response = host_service.upload_photo(str(g.current_user_id))
        return jsonify(response.model_dump())
        
    except Exception as e:
        return jsonify({"error": "Failed to upload photo"}), 500
