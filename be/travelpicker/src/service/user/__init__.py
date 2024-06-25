__all__ = ["UserService"]

from src.domain.entity import User
from src.repository.user import AbstractUserRepository


class UserService:
    def __init__(self, repo: AbstractUserRepository) -> None:
        self._repo = repo


    async def create_user(self, email: str) -> User:
        return await self._repo.create(email)
    

    async def get_user_by_id(self, id: int) -> User | None:
        return await self._repo.get({"id": id})
    

    async def get_user_by_email(self, email: str) -> User | None:
        return await self._repo.get({"email": email})