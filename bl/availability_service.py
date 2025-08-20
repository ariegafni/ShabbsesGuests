
from dal.repository.availability_repository import AvailabilityRepository
from models.availability import Availability

class AvailabilityService:
    def __init__(self):
        self.repo = AvailabilityRepository()

    def add_availability(self, availability: Availability) -> int:
        return self.repo.add(availability)

    def get_by_host(self, host_id: int) -> list[Availability]:
        return self.repo.get_by_host(host_id)

    def update_availability(self, availability_id: int, data: dict):
        self.repo.update(availability_id, data)

    def delete_availability(self, availability_id: int):
        self.repo.delete(availability_id)
