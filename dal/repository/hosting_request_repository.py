from models.hosting_request import HostingRequest
from utils.db import get_connection

class HostingRequestRepository:
    def add(self, request: HostingRequest) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO hosting_requests (host_id, guest_id, requested_date, status, message)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
            """,
            (request.host_id, request.guest_id, request.requested_date, request.status, request.message)
        )
        request_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return request_id

    def get_by_id(self, request_id: int) -> HostingRequest | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM hosting_requests WHERE id = %s", (request_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return HostingRequest(**dict(zip([desc[0] for desc in cur.description], row)))
        return None

    def get_by_guest(self, guest_id: int) -> list[HostingRequest]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM hosting_requests WHERE guest_id = %s ORDER BY requested_date DESC", (guest_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [HostingRequest(**dict(zip([desc[0] for desc in cur.description], row))) for row in rows]

    def get_by_host(self, host_id: int) -> list[HostingRequest]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM hosting_requests WHERE host_id = %s ORDER BY requested_date DESC", (host_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [HostingRequest(**dict(zip([desc[0] for desc in cur.description], row))) for row in rows]

    def update(self, request_id: int, data: dict):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE hosting_requests
            SET status = %s, message = %s
            WHERE id = %s
        """, (data.get("status"), data.get("message"), request_id))
        conn.commit()
        cur.close()
        conn.close()

    def delete(self, request_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM hosting_requests WHERE id = %s", (request_id,))
        conn.commit()
        cur.close()
        conn.close()
