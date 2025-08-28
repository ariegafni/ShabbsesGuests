from typing import List, Optional
import requests
from dal.repository.host_repository import HostRepository
from models.host import CreateHostRequest, HostResponse, Host, UpdateHostRequest, UploadPhotoResponse


class HostService:
    def __init__(self):
        self.repo = HostRepository()

    def _ensure_country_exists(self, country_place_id: str) -> None:
        """Ensure country exists in the countries list, add if it doesn't"""
        try:
            # Check if country exists
            response = requests.get(f"http://localhost:5000/api/locations/countries/{country_place_id}")
            if response.status_code == 404:
                # Country doesn't exist, add it
                add_response = requests.post(
                    "http://localhost:5000/api/locations/countries",
                    json={"place_id": country_place_id}
                )
                if add_response.status_code != 201:
                    print(f"Warning: Failed to add country {country_place_id}")
        except Exception as e:
            print(f"Warning: Failed to ensure country exists: {e}")
            # Don't fail the host creation if this fails

    def create_host(self, user_id: str, host_data: CreateHostRequest) -> HostResponse:
        # Ensure country exists before creating host
        self._ensure_country_exists(host_data.country_place_id)
        
        # Check if user already has a host profile
        if self.repo.user_has_host_profile(user_id):
            raise ValueError("User already has a host profile")
        
        # Create host object
        host = Host(
            user_id=user_id,
            country_place_id=host_data.country_place_id,
            city_place_id=host_data.city_place_id,
            area=host_data.area,
            address=host_data.address,
            description=host_data.description,
            bio=host_data.bio,
            max_guests=host_data.max_guests,
            hosting_type=host_data.hosting_type,
            kashrut_level=host_data.kashrut_level,
            languages=host_data.languages,
            total_hostings=host_data.total_hostings or 0,
            is_always_available=host_data.is_always_available or False,
            available=host_data.available,
            photo_url=host_data.photo_url
        )
        
        # Save to database
        host_id = self.repo.add(host)
        
        # Get the created host
        host_response = self.repo.get_by_id(host_id)
        if not host_response:
            raise Exception("Failed to create host profile")
        
        return host_response

    def get_host_by_id(self, host_id: str) -> Optional[HostResponse]:
        return self.repo.get_by_id(host_id)

    def get_host_by_user_id(self, user_id: str) -> Optional[HostResponse]:
        return self.repo.get_by_user_id(user_id)

    def get_all_hosts(self) -> List[HostResponse]:
        return self.repo.get_all()

    def get_hosts_by_country(self, country_place_id: str) -> List[HostResponse]:
        return self.repo.get_by_country(country_place_id)

    def update_host(self, host_id: str, user_id: str, data: UpdateHostRequest) -> HostResponse:
        # Verify the host belongs to the user
        host = self.repo.get_by_id(host_id)
        if not host:
            raise ValueError("Host not found")
        
        if host.user_id != user_id:
            raise ValueError("Not authorized to update this host profile")
        
        # Convert to dict, removing None values
        update_data = {}
        for field, value in data.dict().items():
            if value is not None:
                update_data[field] = value
        
        if not update_data:
            raise ValueError("No valid fields to update")
        
        # Update in database
        self.repo.update(host_id, update_data)
        
        # Get updated host
        updated_host = self.repo.get_by_id(host_id)
        if not updated_host:
            raise Exception("Failed to update host profile")
        
        return updated_host

    def delete_host(self, host_id: str, user_id: str):
        # Verify the host belongs to the user
        host = self.repo.get_by_id(host_id)
        if not host:
            raise ValueError("Host not found")
        
        if host.user_id != user_id:
            raise ValueError("Not authorized to delete this host profile")
        
        self.repo.delete(host_id)

    def upload_photo(self, user_id: str) -> UploadPhotoResponse:
        # For now, return a mock photo URL
        # In a real implementation, you would:
        # 1. Save the file to storage (S3, local filesystem, etc.)
        # 2. Return the actual URL
        photo_url = f"https://example.com/photos/{user_id}/host_photo.jpg"
        
        return UploadPhotoResponse(photo_url=photo_url)
