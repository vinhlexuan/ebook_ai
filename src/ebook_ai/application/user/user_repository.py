from typing import Protocol

from models.user import User


class UserRepository(Protocol):
    def create_user(self, user_dict: dict) -> User:
        ...

    def update_role(self, user_id: int, role_id: int) -> None:
        ...

    def login(self, user_dict: dict) -> User:
        ...