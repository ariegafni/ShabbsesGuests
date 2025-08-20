from dal.repository.guest_repository import GuestRepository
from models.guest import Guest

class GuestService:
    def __init__(self):
        self.repo = GuestRepository()

    def add_guest(self, guest: Guest) -> int:
        return self.repo.add(guest)

    def get_guest(self, guest_id: int) -> Guest | None:
        return self.repo.get_by_id(guest_id)

    def update_guest(self, guest_id: int, data: dict):
        self.repo.update(guest_id, data)

    def delete_guest(self, guest_id: int):
        self.repo.delete(guest_id)

