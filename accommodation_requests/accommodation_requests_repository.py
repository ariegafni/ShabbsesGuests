from accommodation_requests.accommodation_requests_model import AccommodationRequest, AccommodationRequestResponse, AccommodationRequestWithDetails
from storage.postgres_db import get_connection
from datetime import datetime
import uuid
from typing import List


class AccommodationRequestsRepository:
    def add(self, request: AccommodationRequest) -> str:
        conn = get_connection()
        try:
            with conn:  # טרנזקציה אטומית (commit/rollback אוטומטי)
                with conn.cursor() as cur:
                    request_id = str(uuid.uuid4())
                    now = datetime.utcnow()

                    cur.execute("""
                        INSERT INTO accommodation_requests (
                            id, guest_id, host_id, request_date, message, status,
                            created_at, updated_at
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id;
                    """, (
                        request_id, request.guest_id, request.host_id,
                        request.request_date, request.message, request.status.value,
                        now, now
                    ))
                    return cur.fetchone()[0]
        finally:
            conn.close()

    def get_by_id(self, request_id: str) -> AccommodationRequestResponse | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM accommodation_requests WHERE id = %s", (request_id,))
        row = cur.fetchone()
        
        if not row:
            cur.close()
            conn.close()
            return None
            
        columns = [desc[0] for desc in cur.description]
        request_dict = dict(zip(columns, row))
        
        # Convert datetime objects to ISO format strings
        if request_dict.get('created_at'):
            request_dict['created_at'] = request_dict['created_at'].isoformat()
        if request_dict.get('updated_at'):
            request_dict['updated_at'] = request_dict['updated_at'].isoformat()
        if request_dict.get('request_date'):
            request_dict['requested_date'] = request_dict['request_date'].isoformat()
            del request_dict['request_date']  # Remove old field name
            
        cur.close()
        conn.close()
        
        return AccommodationRequestResponse(**request_dict)

    def get_by_guest_id(self, guest_id: str) -> List[AccommodationRequestWithDetails]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                ar.*,
                u.first_name as guest_first_name,
                u.last_name as guest_last_name,
                u.email as guest_email,
                u.phone as guest_phone,
                u.profile_image as guest_profile_image,
                h.user_id as host_user_id,
                h.country_place_id as host_country_place_id,
                h.city_place_id as host_city_place_id,
                h.area as host_area,
                h.address as host_address,
                h.description as host_description,
                h.bio as host_bio,
                h.max_guests as host_max_guests,
                h.photo_url as host_photo_url
            FROM accommodation_requests ar
            JOIN users u ON ar.guest_id = u.id
            JOIN hosts h ON ar.host_id = h.id
            WHERE ar.guest_id = %s
            ORDER BY ar.created_at DESC
        """, (guest_id,))
        rows = cur.fetchall()
        
        requests = []
        if rows:
            columns = [desc[0] for desc in cur.description]
            for row in rows:
                request_dict = dict(zip(columns, row))
                
                # Convert datetime objects to ISO format strings
                if request_dict.get('created_at'):
                    request_dict['created_at'] = request_dict['created_at'].isoformat()
                if request_dict.get('updated_at'):
                    request_dict['updated_at'] = request_dict['updated_at'].isoformat()
                if request_dict.get('request_date'):
                    request_dict['requested_date'] = request_dict['request_date'].isoformat()
                    del request_dict['request_date']  # Remove old field name
                
                requests.append(AccommodationRequestWithDetails(**request_dict))
        
        cur.close()
        conn.close()
        return requests

    def get_by_host_id(self, host_id: str) -> List[AccommodationRequestWithDetails]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                ar.*,
                u.first_name as guest_first_name,
                u.last_name as guest_last_name,
                u.email as guest_email,
                u.phone as guest_phone,
                u.profile_image as guest_profile_image,
                h.user_id as host_user_id,
                h.country_place_id as host_country_place_id,
                h.city_place_id as host_city_place_id,
                h.area as host_area,
                h.address as host_address,
                h.description as host_description,
                h.bio as host_bio,
                h.max_guests as host_max_guests,
                h.photo_url as host_photo_url
            FROM accommodation_requests ar
            JOIN users u ON ar.guest_id = u.id
            JOIN hosts h ON ar.host_id = h.id
            WHERE ar.host_id = %s
            ORDER BY ar.created_at DESC
        """, (host_id,))
        rows = cur.fetchall()
        
        requests = []
        if rows:
            columns = [desc[0] for desc in cur.description]
            for row in rows:
                request_dict = dict(zip(columns, row))
                
                # Convert datetime objects to ISO format strings
                if request_dict.get('created_at'):
                    request_dict['created_at'] = request_dict['created_at'].isoformat()
                if request_dict.get('updated_at'):
                    request_dict['updated_at'] = request_dict['updated_at'].isoformat()
                if request_dict.get('request_date'):
                    request_dict['requested_date'] = request_dict['request_date'].isoformat()
                    del request_dict['request_date']  # Remove old field name
                
                requests.append(AccommodationRequestWithDetails(**request_dict))
        
        cur.close()
        conn.close()
        return requests

    def update_status(self, request_id: str, status: str):
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE accommodation_requests 
            SET status = %s, updated_at = %s 
            WHERE id = %s
        """, (status, datetime.utcnow(), request_id))
        conn.commit()
        cur.close()
        conn.close()

    def delete(self, request_id: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM accommodation_requests WHERE id = %s", (request_id,))
        conn.commit()
        cur.close()
        conn.close()

    def get_by_guest_and_host(self, guest_id: str, host_id: str) -> AccommodationRequestResponse | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM accommodation_requests 
            WHERE guest_id = %s AND host_id = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (guest_id, host_id))
        row = cur.fetchone()
        
        if not row:
            cur.close()
            conn.close()
            return None
            
        columns = [desc[0] for desc in cur.description]
        request_dict = dict(zip(columns, row))
        
        # Convert datetime objects to ISO format strings
        if request_dict.get('created_at'):
            request_dict['created_at'] = request_dict['created_at'].isoformat()
        if request_dict.get('updated_at'):
            request_dict['updated_at'] = request_dict['updated_at'].isoformat()
        if request_dict.get('request_date'):
            request_dict['requested_date'] = request_dict['request_date'].isoformat()
            del request_dict['request_date']  # Remove old field name
            
        cur.close()
        conn.close()
        
        return AccommodationRequestResponse(**request_dict)
