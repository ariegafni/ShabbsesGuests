from flask import Blueprint, request, jsonify
from bl.availability_service import AvailabilityService
from models.availability import Availability

availability_api = Blueprint("availability_api", __name__)
availability_service = AvailabilityService()

@availability_api.route("/availability", methods=["POST"])
def add_availability():
    availability = Availability(**request.json)
    availability_id = availability_service.add_availability(availability)
    return jsonify({"id": availability_id}), 201

@availability_api.route("/availability/host/<int:host_id>", methods=["GET"])
def get_availability_by_host(host_id):
    availability_list = availability_service.get_by_host(host_id)
    return jsonify([a.dict() for a in availability_list])

@availability_api.route("/availability/<int:availability_id>", methods=["PUT"])
def update_availability(availability_id):
    data = request.json
    availability_service.update_availability(availability_id, data)
    return jsonify({"message": "Availability updated"})

@availability_api.route("/availability/<int:availability_id>", methods=["DELETE"])
def delete_availability(availability_id):
    availability_service.delete_availability(availability_id)
    return jsonify({"message": "Availability deleted"})
