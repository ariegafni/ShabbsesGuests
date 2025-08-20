
from models.availability import Availability
from utils.db import get_connection

class AvailabilityRepository:
    def add(self, availability: Availability) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO availability (host_id, date, max_guests, notes)
            VALUES (%s, %s, %s, %s) RETURNING id;
            """,
            (availability.host_id, availability.date, availability.max_guests, availability.notes)
        )
        availability_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return availability_id

    def get_by_host(self, host_id: int) -> list[Availability]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM availability WHERE host_id = %s ORDER BY date", (host_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [Availability(**dict(zip([desc[0] for desc in cur.description], row))) for row in rows]

    def update(self, availability_id: int, data: dict):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE availability
            SET date = %s, max_guests = %s, notes = %s
            WHERE id = %s
        """, (
            data.get("date"),
            data.get("max_guests"),
            data.get("notes"),
            availability_id
        ))
        conn.commit()
        cur.close()
        conn.close()

    def delete(self, availability_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM availability WHERE id = %s", (availability_id,))
        conn.commit()
        cur.close()
        conn.close()
