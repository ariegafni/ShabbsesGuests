
from models.report import Report
from utils.db import get_connection
from datetime import datetime

class ReportRepository:
    def add(self, report: Report) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO reports (reporter_id, reported_user_id, reason, details, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
            """,
            (report.reporter_id, report.reported_user_id, report.reason, report.details, report.status, report.created_at or datetime.utcnow())
        )
        report_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return report_id

    def get_all(self) -> list[Report]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM reports ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [Report(**dict(zip([desc[0] for desc in cur.description], row))) for row in rows]

    def update_status(self, report_id: int, status: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE reports SET status = %s WHERE id = %s", (status, report_id))
        conn.commit()
        cur.close()
        conn.close()