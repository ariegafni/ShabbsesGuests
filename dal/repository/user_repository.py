
from models.user import User
from utils.db import get_connection

class UserRepository:
    def add(self, user: User):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (name, email, phone, photo_url, social_links)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """, (user.name, user.email, user.phone, user.photo_url, user.social_links))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return user_id

    def get_by_id(self, user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        user = User(**dict(zip([d[0] for d in cur.description], row))) if row else None
        cur.close()
        conn.close()
        return user

    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        users = [User(**dict(zip([d[0] for d in cur.description], row))) for row in rows]
        cur.close()
        conn.close()
        return users

    def update(self, user_id, data):
        conn = get_connection()
        cur = conn.cursor()
        for key, value in data.items():
            cur.execute(f"UPDATE users SET {key} = %s WHERE id = %s", (value, user_id))
        conn.commit()
        cur.close()
        conn.close()

    def delete(self, user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cur.close()
        conn.close()