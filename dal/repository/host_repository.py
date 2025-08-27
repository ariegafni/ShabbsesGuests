
from models.host import Host, HostResponse
from utils.db import get_connection
from datetime import datetime
import json
import uuid
from typing import List


class HostRepository:
    def add(self, host: Host) -> str:
        conn = get_connection()
        try:
            with conn:  # טרנזקציה אטומית (commit/rollback אוטומטי)
                with conn.cursor() as cur:
                    host_id = str(uuid.uuid4())
                    now = datetime.utcnow()

                    # מבטיחים קיום מדינה בטבלת countries (אם קיימת – מתעלמים)
                    cur.execute("""
                        INSERT INTO countries (country_place_id, created_at, updated_at)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (country_place_id) DO NOTHING;
                    """, (host.country_place_id, now, now))

                    # הכנסת המארח
                    cur.execute("""
                        INSERT INTO hosts (
                            id, user_id, country_place_id, city_place_id, area, address,
                            description, bio, max_guests, hosting_type, kashrut_level,
                            languages, total_hostings, is_always_available, available,
                            photo_url, created_at, updated_at
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id;
                    """, (
                        host_id, host.user_id, host.country_place_id, host.city_place_id,
                        host.area, host.address, host.description, host.bio, host.max_guests,
                        host.hosting_type, host.kashrut_level, host.languages,
                        host.total_hostings, host.is_always_available, host.available,
                        host.photo_url, now, now
                    ))
                    return cur.fetchone()[0]
        finally:
            conn.close()


    def get_by_id(self, host_id: str) -> HostResponse | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM hosts WHERE id = %s", (host_id,))
        row = cur.fetchone()
        
        if not row:
            cur.close()
            conn.close()
            return None
            
        columns = [desc[0] for desc in cur.description]
        host_dict = dict(zip(columns, row))
        
        # Convert datetime objects to ISO format strings
        if host_dict.get('created_at'):
            host_dict['created_at'] = host_dict['created_at'].isoformat()
        if host_dict.get('updated_at'):
            host_dict['updated_at'] = host_dict['updated_at'].isoformat()
            
        cur.close()
        conn.close()
        
        return HostResponse(**host_dict)

    def get_by_user_id(self, user_id: str) -> HostResponse | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM hosts WHERE user_id = %s", (user_id,))
        row = cur.fetchone()
        
        if not row:
            cur.close()
            conn.close()
            return None
            
        columns = [desc[0] for desc in cur.description]
        host_dict = dict(zip(columns, row))
        
        # Convert datetime objects to ISO format strings
        if host_dict.get('created_at'):
            host_dict['created_at'] = host_dict['created_at'].isoformat()
        if host_dict.get('updated_at'):
            host_dict['updated_at'] = host_dict['updated_at'].isoformat()
            
        cur.close()
        conn.close()
        
        return HostResponse(**host_dict)

    def get_all(self) -> List[HostResponse]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM hosts ORDER BY created_at DESC")
        rows = cur.fetchall()
        
        hosts = []
        if rows:
            columns = [desc[0] for desc in cur.description]
            for row in rows:
                host_dict = dict(zip(columns, row))
                
                # Convert datetime objects to ISO format strings
                if host_dict.get('created_at'):
                    host_dict['created_at'] = host_dict['created_at'].isoformat()
                if host_dict.get('updated_at'):
                    host_dict['updated_at'] = host_dict['updated_at'].isoformat()
                
                hosts.append(HostResponse(**host_dict))
        
        cur.close()
        conn.close()
        return hosts

    def get_by_country(self, country_place_id: str) -> List[HostResponse]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM hosts WHERE country_place_id = %s ORDER BY created_at DESC", (country_place_id,))
        rows = cur.fetchall()
        
        hosts = []
        if rows:
            columns = [desc[0] for desc in cur.description]
            for row in rows:
                host_dict = dict(zip(columns, row))
                
                # Convert datetime objects to ISO format strings
                if host_dict.get('created_at'):
                    host_dict['created_at'] = host_dict['created_at'].isoformat()
                if host_dict.get('updated_at'):
                    host_dict['updated_at'] = host_dict['updated_at'].isoformat()
                
                hosts.append(HostResponse(**host_dict))
        
        cur.close()
        conn.close()
        return hosts

    def update(self, host_id: str, data: dict):
        conn = get_connection()
        cur = conn.cursor()
        
        # Add updated_at timestamp
        data['updated_at'] = datetime.utcnow()
        
        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        values = list(data.values()) + [host_id]
        
        cur.execute(f"UPDATE hosts SET {set_clause} WHERE id = %s", values)
        conn.commit()
        cur.close()
        conn.close()

    def delete(self, host_id: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM hosts WHERE id = %s", (host_id,))
        conn.commit()
        cur.close()
        conn.close()

    def user_has_host_profile(self, user_id: str) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM hosts WHERE user_id = %s", (user_id,))
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count > 0
