
from flask import Blueprint, request, jsonify
from bl.thank_you_note_service import ThankYouNoteService
from models.thank_you_note import ThankYouNote

thank_you_note_api = Blueprint("thank_you_note_api", __name__)
thank_you_note_service = ThankYouNoteService()

@thank_you_note_api.route("/thankyou", methods=["POST"])
def add_note():
    note = ThankYouNote(**request.json)
    note_id = thank_you_note_service.add_note(note)
    return jsonify({"id": note_id}), 201

@thank_you_note_api.route("/thankyou/host/<int:host_id>", methods=["GET"])
def get_notes_for_host(host_id):
    notes = thank_you_note_service.get_notes_for_host(host_id)
    return jsonify([n.dict() for n in notes])

@thank_you_note_api.route("/thankyou/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.json
    thank_you_note_service.update_note(note_id, data["content"])
    return jsonify({"message": "Note updated"})

@thank_you_note_api.route("/thankyou/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    thank_you_note_service.delete_note(note_id)
    return jsonify({"message": "Note deleted"})
