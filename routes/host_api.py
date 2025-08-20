from flask import Blueprint, request, jsonify
from bl.host_service import HostService
from models.host import Host

host_api = Blueprint("host_api", __name__)
host_service = HostService()

@host_api.route("/hosts", methods=["POST"])
def add_host():
    host = Host(**request.json)
    host_id = host_service.add_host(host)
    return jsonify({"id": host_id}), 201

@host_api.route("/hosts/<int:host_id>", methods=["GET"])
def get_host(host_id):
    host = host_service.get_host(host_id)
    return jsonify(host.dict()) if host else (jsonify({"error": "Host not found"}), 404)

@host_api.route("/hosts/<int:host_id>", methods=["PUT"])
def update_host(host_id):
    data = request.json
    host_service.update_host(host_id, data)
    return jsonify({"message": "Host updated"})

@host_api.route("/hosts/<int:host_id>", methods=["DELETE"])
def delete_host(host_id):
    host_service.delete_host(host_id)
    return jsonify({"message": "Host deleted"})

@host_api.route("/hosts", methods=["GET"])
def search_hosts():
    filters = request.args.to_dict()
    hosts = host_service.search_hosts(filters)
    return jsonify([h.dict() for h in hosts])
