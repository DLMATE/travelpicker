__all__ = ["AbstractAuthRepository", "AuthMemoryRepository"]

from abc import ABC, abstractmethod
from typing import Dict, List, Any

from src.domain.entity import Auth


class AbstractAuthRepository(ABC):
    @abstractmethod
    async def create(self, refresh_token: str, user_id: int) -> Auth:
        pass


    @abstractmethod
    async def get(self, filter: Dict[str, Any]) -> Auth:
        pass



class AuthMemoryRepository(AbstractAuthRepository):
    key = "Auth"
    
    def __init__(self, data: Dict[str, List[Any]]) -> None:
        self.data = data


    async def create(self, refresh_token: str, user_id: int) -> Auth:
        auth = Auth(
            id=len(self.data[self.key]) + 1,
            refresh_token=refresh_token,
            user_id=user_id
        )
        self.data[self.key].append(auth)
        return auth
    

    async def get(self, filter: Dict[str, Any]) -> Auth | None:
        for auth in self.data[self.key]:
            if self._match(auth, filter):
                return auth
        return None


    def _match(self, user: Auth, filter: Dict[str, Any]) -> bool:
        for k, v in filter.items():
            if getattr(user, k) != v:
                return False
        return True