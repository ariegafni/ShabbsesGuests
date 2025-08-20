from models.thank_you_note import ThankYouNote
from utils.db import get_connection
from datetime import date

class ThankYouNoteRepository:
    def add(self, note: ThankYouNote) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO thank_you_notes (host_id, guest_id, content, date_written)
            VALUES (%s, %s, %s, %s) RETURNING id;
            """,
            (note.host_id, note.guest_id, note.content, note.date_written or date.today())
        )
        note_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return note_id

    def get_by_host(self, host_id: int) -> list[ThankYouNote]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM thank_you_notes WHERE host_id = %s ORDER BY date_written DESC", (host_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [ThankYouNote(**dict(zip([desc[0] for desc in cur.description], row))) for row in rows]

    def update(self, note_id: int, content: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE thank_you_notes SET content = %s WHERE id = %s", (content, note_id))
        conn.commit()
        cur.close()
        conn.close()

    def delete(self, note_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM thank_you_notes WHERE id = %s", (note_id,))
        conn.commit()
        cur.close()
        conn.close()
