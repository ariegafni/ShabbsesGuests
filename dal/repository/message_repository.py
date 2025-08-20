
from models.message import Message
from utils.db import get_connection
from datetime import datetime

class MessageRepository:
    def add(self, msg: Message) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO messages (sender_id, receiver_id, thread_id, content, timestamp)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
            """,
            (msg.sender_id, msg.receiver_id, msg.thread_id, msg.content, msg.timestamp or datetime.utcnow())
        )
        message_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return message_id

    def get_thread(self, thread_id: str) -> list[Message]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM messages WHERE thread_id = %s ORDER BY timestamp", (thread_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [Message(**dict(zip([desc[0] for desc in cur.description], row))) for row in rows]

    def update(self, message_id: int, content: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE messages SET content = %s WHERE id = %s",
            (content, message_id)
        )
        conn.commit()
        cur.close()
        conn.close()

    def delete(self, message_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM messages WHERE id = %s", (message_id,))
        conn.commit()
        cur.close()
        conn.close()
