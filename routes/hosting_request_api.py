from flask import Blueprint, request, jsonify
from bl.hosting_request_service import HostingRequestService
from models.hosting_request import HostingRequest

hosting_request_api = Blueprint("hosting_request_api", __name__)
hosting_request_service = HostingRequestService()

@hosting_request_api.route("/requests", methods=["POST"])
def add_request():
    req = HostingRequest(**request.json)
    req_id = hosting_request_service.add_request(req)
    return jsonify({"id": req_id}), 201

@hosting_request_api.route("/requests/<int:request_id>", methods=["GET"])
def get_request(request_id):
    req = hosting_request_service.get_request(request_id)
    return jsonify(req.dict()) if req else (jsonify({"error": "Request not found"}), 404)

@hosting_request_api.route("/requests/guest/<int:guest_id>", methods=["GET"])
def get_requests_by_guest(guest_id):
    requests = hosting_request_service.get_requests_by_guest(guest_id)
    return jsonify([r.dict() for r in requests])

@hosting_request_api.route("/requests/host/<int:host_id>", methods=["GET"])
def get_requests_by_host(host_id):
    requests = hosting_request_service.get_requests_by_host(host_id)
    return jsonify([r.dict() for r in requests])

@hosting_request_api.route("/requests/<int:request_id>", methods=["PUT"])
def update_request(request_id):
    data = request.json
    hosting_request_service.update_request(request_id, data)
    return jsonify({"message": "Request updated"})

@hosting_request_api.route("/requests/<int:request_id>", methods=["DELETE"])
def delete_request(request_id):
    hosting_request_service.delete_request(request_id)
    return jsonify({"message": "Request deleted"})
