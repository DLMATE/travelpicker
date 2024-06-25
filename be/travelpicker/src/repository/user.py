__all__ = ["AbstractUserRepository", "UserMemoryRepository"]

from abc import ABC, abstractmethod
from typing import Dict, List, Any

from src.domain.entity import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create(self, email: str) -> User:
        pass


    @abstractmethod
    async def get(self, filter: Dict[str, Any]) -> User:
        pass



class UserMemoryRepository(AbstractUserRepository):
    key = "User"
    
    def __init__(self, data: Dict[str, List[Any]]) -> None:
        self.data = data


    async def create(self, email: str) -> User:
        user = User(
            id=len(self.data[self.key]) + 1,
            email=email
        )
        self.data[self.key].append(user)
        return user
    

    async def get(self, filter: Dict[str, Any]) -> User | None:
        for user in self.data[self.key]:
            if self._match(user, filter):
                return user
        return None


    def _match(self, user: User, filter: Dict[str, Any]) -> bool:
        for k, v in filter.items():
            if getattr(user, k) != v:
                return False
        return True