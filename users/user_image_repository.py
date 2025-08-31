from storage.postgres_db import get_connection


class UserImageRepository:
    def add_image(self, user_id: str, object_key: str, url: str, is_current_profile: bool = False) -> str:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO user_images (user_id, object_key, url, is_current_profile)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (user_id, object_key, url, is_current_profile))
        image_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return image_id

    def clear_current_profile_flags(self, user_id: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE user_images SET is_current_profile = FALSE WHERE user_id = %s;", (user_id,))
        conn.commit()
        cur.close()
        conn.close()
