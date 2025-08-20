
from models.host import Host
from utils.db import get_connection


class HostRepository:
    def add(self, host: Host) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO hosts (user_id, area, max_guests, accepts_sleepover, religious_level, languages)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
            """,
            (host.user_id, host.area, host.max_guests, host.accepts_sleepover, host.religious_level, host.languages)
        )
        host_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return host_id

    def get_by_id(self, host_id: int) -> Host | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM hosts WHERE id = %s", (host_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return Host(**dict(zip([desc[0] for desc in cur.description], row)))
        return None

    def update(self, host_id: int, data: dict):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE hosts
            SET area = %s, max_guests = %s, accepts_sleepover = %s, religious_level = %s, languages = %s
            WHERE id = %s
        """, (
            data.get("area"),
            data.get("max_guests"),
            data.get("accepts_sleepover"),
            data.get("religious_level"),
            data.get("languages"),
            host_id
        ))
        conn.commit()
        cur.close()
        conn.close()

    def delete(self, host_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM hosts WHERE id = %s", (host_id,))
        conn.commit()
        cur.close()
        conn.close()

    def search(self, filters: dict) -> list[Host]:
        conn = get_connection()
        cur = conn.cursor()
        query = "SELECT * FROM hosts WHERE 1=1"
        params = []

        if "area" in filters:
            query += " AND area = %s"
            params.append(filters["area"])
        if "accepts_sleepover" in filters:
            query += " AND accepts_sleepover = %s"
            params.append(filters["accepts_sleepover"])

        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [Host(**dict(zip([desc[0] for desc in cur.description], row))) for row in rows]
