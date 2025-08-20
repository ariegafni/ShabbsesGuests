
from dal.repository.hosting_request_repository import HostingRequestRepository
from models.hosting_request import HostingRequest

class HostingRequestService:
    def __init__(self):
        self.repo = HostingRequestRepository()

    def add_request(self, request: HostingRequest) -> int:
        return self.repo.add(request)

    def get_request(self, request_id: int) -> HostingRequest | None:
        return self.repo.get_by_id(request_id)

    def get_requests_by_guest(self, guest_id: int) -> list[HostingRequest]:
        return self.repo.get_by_guest(guest_id)

    def get_requests_by_host(self, host_id: int) -> list[HostingRequest]:
        return self.repo.get_by_host(host_id)

    def update_request(self, request_id: int, data: dict):
        self.repo.update(request_id, data)

    def delete_request(self, request_id: int):
        self.repo.delete(request_id)
