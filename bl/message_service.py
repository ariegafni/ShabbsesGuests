
from dal.repository.message_repository import MessageRepository
from models.message import Message

class MessageService:
    def __init__(self):
        self.repo = MessageRepository()

    def send_message(self, msg: Message) -> int:
        return self.repo.add(msg)

    def get_thread(self, thread_id: str) -> list[Message]:
        return self.repo.get_thread(thread_id)

    def update_message(self, message_id: int, content: str):
        self.repo.update(message_id, content)

    def delete_message(self, message_id: int):
        self.repo.delete(message_id)

