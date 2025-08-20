
from dal.repository.host_repository import HostRepository
from models.host import Host

class HostService:
    def __init__(self):
        self.repo = HostRepository()

    def add_host(self, host: Host) -> int:
        return self.repo.add(host)


    def get_host(self, host_id: int) -> Host | None:
        return self.repo.get_by_id(host_id)

    def update_host(self, host_id: int, data: dict):
        self.repo.update(host_id, data)

    def delete_host(self, host_id: int):
        self.repo.delete(host_id)

    def search_hosts(self, filters: dict) -> list[Host]:
        return self.repo.search(filters)
