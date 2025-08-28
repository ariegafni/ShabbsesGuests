from typing import List, Dict, Any
from dal.repository.countries_repository import CountriesRepository
from dal.repository.host_repository import HostRepository

class CountryService:
    def __init__(self, countries_repo: CountriesRepository | None = None, hosts_repo: HostRepository | None = None):
        self.countries_repo = countries_repo or CountriesRepository()
        self.hosts_repo = hosts_repo or HostRepository()

    def get_top5_hosts_per_country(self) -> List[Dict[str, Any]]:
        grouped = self.countries_repo.get_top5_hosts_per_country()
        return [
            {
                "country_place_id": country,
                "hosts": [h.dict() for h in hosts]
            }
            for country, hosts in grouped.items()
        ]
    def get_all_countries(self) -> List[Dict[str, Any]]:
        return self.countries_repo.get_all()

    def ensure_country_exists(self, country_place_id: str) -> None:
        self.countries_repo.ensure_exists(country_place_id)

    def get_hosts_by_country(self, country_place_id: str) -> List[Dict[str, Any]]:
        hosts = self.hosts_repo.get_by_country(country_place_id)
        return [h.dict() for h in hosts]
    