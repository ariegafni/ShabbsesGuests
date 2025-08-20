from flask import Blueprint, request, jsonify
from bl.guest_service import GuestService
from models.guest import Guest

guest_api = Blueprint("guest_api", __name__)
guest_service = GuestService()

@guest_api.route("/guests", methods=["POST"])
def add_guest():
    guest = Guest(**request.json)
    guest_id = guest_service.add_guest(guest)
    return jsonify({"id": guest_id}), 201

@guest_api.route("/guests/<int:guest_id>", methods=["GET"])
def get_guest(guest_id):
    guest = guest_service.get_guest(guest_id)
    return jsonify(guest.dict()) if guest else (jsonify({"error": "Guest not found"}), 404)

@guest_api.route("/guests/<int:guest_id>", methods=["PUT"])
def update_guest(guest_id):
    data = request.json
    guest_service.update_guest(guest_id, data)
    return jsonify({"message": "Guest updated"})

@guest_api.route("/guests/<int:guest_id>", methods=["DELETE"])
def delete_guest(guest_id):
    guest_service.delete_guest(guest_id)
    return jsonify({"message": "Guest deleted"})