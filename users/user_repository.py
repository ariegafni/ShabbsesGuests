from users.user_model import User, UserResponse
from storage.postgres_db import get_connection
from datetime import datetime
import json
import uuid


class UserRepository:
    def add(self, user: User) -> str:
        conn = get_connection()
        cur = conn.cursor()
        
        # Generate UUID for user ID
        user_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        cur.execute("""
            INSERT INTO users (
                id, first_name, last_name, email, password_hash, 
                phone, country, city, profile_image, bio, 
                social_links, is_verified, created_at, updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            RETURNING id;
        """, (
            user_id, user.first_name, user.last_name, user.email, user.password_hash,
            user.phone, user.country, user.city, user.profile_image, user.bio,
            json.dumps([link.model_dump() for link in user.social_links]) if user.social_links else None,
            user.is_verified, now, now
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        return user_id

    def get_by_id(self, user_id: str) -> UserResponse | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        
        if not row:
            cur.close()
            conn.close()
            return None
            
        columns = [desc[0] for desc in cur.description]
        user_dict = dict(zip(columns, row))
        
        # Parse social_links JSON
        if user_dict.get('social_links'):
            user_dict['social_links'] = json.loads(user_dict['social_links'])
        else:
            user_dict['social_links'] = []
        
        # Convert datetime objects to ISO format strings
        if user_dict.get('created_at'):
            user_dict['created_at'] = user_dict['created_at'].isoformat()
        if user_dict.get('updated_at'):
            user_dict['updated_at'] = user_dict['updated_at'].isoformat()
            
        cur.close()
        conn.close()
        
        return UserResponse(**user_dict)

    def get_by_email(self, email: str) -> UserResponse | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cur.fetchone()
        
        if not row:
            cur.close()
            conn.close()
            return None
            
        columns = [desc[0] for desc in cur.description]
        user_dict = dict(zip(columns, row))
        
        # Parse social_links JSON
        if user_dict.get('social_links'):
            user_dict['social_links'] = json.loads(user_dict['social_links'])
        else:
            user_dict['social_links'] = []
        
        # Convert datetime objects to ISO format strings
        if user_dict.get('created_at'):
            user_dict['created_at'] = user_dict['created_at'].isoformat()
        if user_dict.get('updated_at'):
            user_dict['updated_at'] = user_dict['updated_at'].isoformat()
            
        cur.close()
        conn.close()
        
        return UserResponse(**user_dict)

    def get_by_email_with_password(self, email: str) -> User | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cur.fetchone()
        
        if not row:
            cur.close()
            conn.close()
            return None
            
        columns = [desc[0] for desc in cur.description]
        user_dict = dict(zip(columns, row))
        
        # Parse social_links JSON
        if user_dict.get('social_links'):
            user_dict['social_links'] = json.loads(user_dict['social_links'])
        else:
            user_dict['social_links'] = []
            
        cur.close()
        conn.close()
        
        return User(**user_dict)

    def update(self, user_id: str, data: dict):
        conn = get_connection()
        cur = conn.cursor()
        
        # Add updated_at timestamp
        data['updated_at'] = datetime.utcnow()
        
        # Handle social_links JSON serialization
        if 'social_links' in data and data['social_links']:
            data['social_links'] = json.dumps([link.model_dump() if hasattr(link, 'model_dump') else link for link in data['social_links']])
        
        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        values = list(data.values()) + [user_id]
        
        cur.execute(f"UPDATE users SET {set_clause} WHERE id = %s", values)
        conn.commit()
        cur.close()
        conn.close()

    def delete(self, user_id: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cur.close()
        conn.close()

    def email_exists(self, email: str) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count > 0

    def set_profile_image_url(self, user_id: str, url: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
               UPDATE users
               SET profile_image = %s, updated_at = NOW()
               WHERE id = %s;
           """, (url, user_id))
        conn.commit()
        cur.close()
        conn.close()