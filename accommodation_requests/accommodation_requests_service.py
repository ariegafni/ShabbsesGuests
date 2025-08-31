from typing import List, Optional
from accommodation_requests.accommodation_requests_repository import AccommodationRequestsRepository
from accommodation_requests.accommodation_requests_model import (
    AccommodationRequest, 
    AccommodationRequestResponse, 
    AccommodationRequestWithDetails,
    CreateAccommodationRequestRequest,
    UpdateAccommodationRequestStatusRequest,
    RequestStatus
)
from hosts.host_repository import HostRepository


class AccommodationRequestsService:
    def __init__(self):
        self.repo = AccommodationRequestsRepository()
        self.host_repo = HostRepository()

    def create_request(self, guest_id: str, request_data: CreateAccommodationRequestRequest) -> AccommodationRequestResponse:
        # Verify host exists
        host = self.host_repo.get_by_id(request_data.host_id)
        if not host:
            raise ValueError("Host not found")
        
        # Check if user already has a pending request for this host
        existing_request = self.repo.get_by_guest_and_host(guest_id, request_data.host_id)
        if existing_request and existing_request.status == "pending":
            raise ValueError("You already have a pending request for this host")
        
        # Create request object
        request = AccommodationRequest(
            guest_id=guest_id,
            host_id=request_data.host_id,
            request_date=request_data.request_date,
            message=request_data.message,
            status=RequestStatus.PENDING
        )
        
        # Save to database
        request_id = self.repo.add(request)
        
        # Get the created request
        request_response = self.repo.get_by_id(request_id)
        if not request_response:
            raise Exception("Failed to create accommodation request")
        
        return request_response

    def get_request_by_id(self, request_id: str) -> Optional[AccommodationRequestResponse]:
        return self.repo.get_by_id(request_id)

    def get_requests_by_guest(self, guest_id: str) -> List[AccommodationRequestWithDetails]:
        return self.repo.get_by_guest_id(guest_id)

    def get_requests_by_host(self, host_id: str) -> List[AccommodationRequestWithDetails]:
        return self.repo.get_by_host_id(host_id)

    def update_request_status(self, request_id: str, user_id: str, status_data: UpdateAccommodationRequestStatusRequest) -> AccommodationRequestResponse:
        # Get the request
        request = self.repo.get_by_id(request_id)
        if not request:
            raise ValueError("Request not found")
        
        # Verify authorization based on status change
        if status_data.status == RequestStatus.ACCEPTED or status_data.status == RequestStatus.REJECTED:
            # Only the host can accept/reject
            host = self.host_repo.get_by_id(request.host_id)
            if not host or host.user_id != user_id:
                raise ValueError("Not authorized to update this request status")
        elif status_data.status == RequestStatus.CANCELLED:
            # Only the guest can cancel
            if request.guest_id != user_id:
                raise ValueError("Not authorized to cancel this request")
        else:
            raise ValueError("Invalid status change")
        
        # Update status
        self.repo.update_status(request_id, status_data.status.value)
        
        # Get updated request
        updated_request = self.repo.get_by_id(request_id)
        if not updated_request:
            raise Exception("Failed to update request status")
        
        return updated_request

    def delete_request(self, request_id: str, user_id: str):
        # Get the request
        request = self.repo.get_by_id(request_id)
        if not request:
            raise ValueError("Request not found")
        
        # Only the guest can delete their own request
        if request.guest_id != user_id:
            raise ValueError("Not authorized to delete this request")
        
        # Only pending requests can be deleted
        if request.status != "pending":
            raise ValueError("Only pending requests can be deleted")
        
        self.repo.delete(request_id)

    def _is_host_of_request(self, request_id: str, user_id: str) -> bool:
        """Helper method to check if user is the host of a specific request"""
        request = self.repo.get_by_id(request_id)
        if not request:
            return False
        
        host = self.host_repo.get_by_id(request.host_id)
        return host and host.user_id == user_id
