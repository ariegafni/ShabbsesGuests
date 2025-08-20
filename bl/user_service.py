
from models.user import User
from dal.repository.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def add_user(self, user: User) -> int:
        return self.repo.add(user)

    def get_user(self, user_id: int) -> User | None:
        return self.repo.get_by_id(user_id)

    def update_user(self, user_id: int, data: dict):
        self.repo.update(user_id, data)

    def delete_user(self, user_id: int):
        self.repo.delete(user_id)

    def login(self, email: str, password: str) -> bool:
        # For simplicity
        "TODO:change it "
        return email == "david@example.com" and password == "secret"

    def send_2fa(self, user_id: int) -> bool:
        "TODO:change it "
        print(f"Sending 2FA to user {user_id}")
        return True

    def verify_2fa(self, user_id: int, code: str) -> bool:
        "TODO:change it "
        return code == "123456"
