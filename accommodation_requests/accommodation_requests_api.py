from flask import Blueprint, request, jsonify, g
from datetime import datetime
from accommodation_requests.accommodation_requests_service import AccommodationRequestsService
from accommodation_requests.accommodation_requests_model import (
    CreateAccommodationRequestRequest,
    UpdateAccommodationRequestStatusRequest
)
from utils.auth import require_auth

accommodation_requests_api = Blueprint('accommodation_requests_api', __name__)
accommodation_requests_service = AccommodationRequestsService()


@accommodation_requests_api.route("/hosting-requests", methods=["POST"])
@require_auth
def create_accommodation_request():
    """Create accommodation request (protected)"""
    try:
        data = request.json or {}
        # Convert from UI format to backend format
        request_data = CreateAccommodationRequestRequest(
            host_id=data.get("host"),
            request_date=datetime.strptime(data.get("requested_date"), "%Y-%m-%d").date(),
            message=data.get("message", "")
        )
        
        request_response = accommodation_requests_service.create_request(
            str(g.current_user_id), 
            request_data
        )
        return jsonify(request_response.model_dump()), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to create accommodation request"}), 500


@accommodation_requests_api.route("/hosting-requests/<request_id>", methods=["GET"])
@require_auth
def get_accommodation_request(request_id):
    """Get accommodation request by ID (protected)"""
    try:
        request_response = accommodation_requests_service.get_request_by_id(request_id)
        if not request_response:
            return jsonify({"error": "Request not found"}), 404
        
        # Check if user is authorized to view this request
        if (request_response.guest_id != str(g.current_user_id) and 
            not accommodation_requests_service._is_host_of_request(request_id, str(g.current_user_id))):
            return jsonify({"error": "Not authorized to view this request"}), 403
        
        return jsonify(request_response.model_dump())
    except Exception as e:
        return jsonify({"error": "Failed to fetch request"}), 500


@accommodation_requests_api.route("/hosting-requests/my-guest-requests", methods=["GET"])
@require_auth
def get_my_accommodation_requests():
    """Get current user's accommodation requests as guest (protected)"""
    try:
        requests = accommodation_requests_service.get_requests_by_guest(str(g.current_user_id))
        return jsonify([request.model_dump() for request in requests])
    except Exception as e:
        return jsonify({"error": "Failed to fetch accommodation requests"}), 500


@accommodation_requests_api.route("/hosting-requests/my-host-requests", methods=["GET"])
@require_auth
def get_host_accommodation_requests():
    """Get accommodation requests for current user as host (protected)"""
    try:
        # Get current user's host profile
        from hosts.host_repository import HostRepository
        host_repo = HostRepository()
        host = host_repo.get_by_user_id(str(g.current_user_id))
        if not host:
            return jsonify({"error": "Host profile not found"}), 404
        
        requests = accommodation_requests_service.get_requests_by_host(host.id)
        return jsonify([request.model_dump() for request in requests])
    except Exception as e:
        return jsonify({"error": "Failed to fetch accommodation requests"}), 500


@accommodation_requests_api.route("/hosting-requests/<request_id>/respond", methods=["PUT"])
@require_auth
def respond_to_hosting_request(request_id):
    """Respond to hosting request (accept/reject) (protected)"""
    try:
        data = request.json or {}
        status = data.get("status")
        if status not in ["accepted", "rejected"]:
            return jsonify({"error": "Invalid status. Must be 'accepted' or 'rejected'"}), 400
        
        status_data = UpdateAccommodationRequestStatusRequest(status=status)
        
        request_response = accommodation_requests_service.update_request_status(
            request_id, 
            str(g.current_user_id), 
            status_data
        )
        return jsonify(request_response.model_dump())
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to respond to hosting request"}), 500


@accommodation_requests_api.route("/hosting-requests/<request_id>/cancel", methods=["PUT"])
@require_auth
def cancel_hosting_request(request_id):
    """Cancel hosting request (protected)"""
    try:
        status_data = UpdateAccommodationRequestStatusRequest(status="cancelled")
        
        request_response = accommodation_requests_service.update_request_status(
            request_id, 
            str(g.current_user_id), 
            status_data
        )
        return jsonify(request_response.model_dump())
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to cancel hosting request"}), 500


@accommodation_requests_api.route("/hosting-requests/<request_id>", methods=["DELETE"])
@require_auth
def delete_accommodation_request(request_id):
    """Delete accommodation request (protected)"""
    try:
        accommodation_requests_service.delete_request(request_id, str(g.current_user_id))
        return jsonify({"message": "Accommodation request deleted successfully"})
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to delete accommodation request"}), 500


