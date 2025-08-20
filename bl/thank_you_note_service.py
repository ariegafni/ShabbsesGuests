
from dal.repository.thank_you_note_repository import ThankYouNoteRepository
from models.thank_you_note import ThankYouNote

class ThankYouNoteService:
    def __init__(self):
        self.repo = ThankYouNoteRepository()

    def add_note(self, note: ThankYouNote) -> int:
        return self.repo.add(note)

    def get_notes_for_host(self, host_id: int) -> list[ThankYouNote]:
        return self.repo.get_by_host(host_id)

    def update_note(self, note_id: int, content: str):
        self.repo.update(note_id, content)

    def delete_note(self, note_id: int):
        self.repo.delete(note_id)