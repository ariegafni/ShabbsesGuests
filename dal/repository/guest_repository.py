from utils.db import get_connection
from models.guest import Guest

class GuestRepository:
    def add(self, guest: Guest) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO guests (user_id, notes)
            VALUES (%s, %s) RETURNING id;
            """,
            (guest.user_id, guest.notes)
        )
        guest_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return guest_id

    def get_by_id(self, guest_id: int) -> Guest | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM guests WHERE id = %s", (guest_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return Guest(**dict(zip([desc[0] for desc in cur.description], row)))
        return None

    def update(self, guest_id: int, data: dict):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE guests
            SET notes = %s
            WHERE id = %s
        """, (data.get("notes"), guest_id))
        conn.commit()
        cur.close()
        conn.close()

    def delete(self, guest_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM guests WHERE id = %s", (guest_id,))
        conn.commit()
        cur.close()
        conn.close()
