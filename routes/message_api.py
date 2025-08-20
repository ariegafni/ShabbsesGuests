
from flask import Blueprint, request, jsonify
from bl.message_service import MessageService
from models.message import Message

message_api = Blueprint("message_api", __name__)
message_service = MessageService()

@message_api.route("/messages", methods=["POST"])
def send_message():
    msg = Message(**request.json)
    msg_id = message_service.send_message(msg)
    return jsonify({"id": msg_id}), 201

@message_api.route("/messages/thread/<string:thread_id>", methods=["GET"])
def get_thread(thread_id):
    messages = message_service.get_thread(thread_id)
    return jsonify([m.dict() for m in messages])

@message_api.route("/messages/<int:message_id>", methods=["PUT"])
def update_message(message_id):
    data = request.json
    message_service.update_message(message_id, data["content"])
    return jsonify({"message": "Message updated"})

@message_api.route("/messages/<int:message_id>", methods=["DELETE"])
def delete_message(message_id):
    message_service.delete_message(message_id)
    return jsonify({"message": "Message deleted"})
