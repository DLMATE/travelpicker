from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid4

import aiohttp
import jwt

from config import AuthConfig
from src.domain.entity import User
from src.domain.value_object import SocialProfile
from src.domain.exception import *
from src.repository.auth import AbstractAuthRepository
from src.dto.auth import *
from src.dto import *
from src.service.user import UserService


class AuthTokenService:
    def __init__(self, repo: AbstractAuthRepository, user_service: UserService) -> None:
        self.repo = repo
        self.user_service = user_service


    async def login(self, profile: SocialProfile) -> AuthLoginResponse:
        user = await self.user_service.get_user_by_email(profile.email)
        if not user:
            user = await self.user_service.create_user(profile.email)

        server_access_token = self._generate_access_token(user.id)
        server_refresh_token = self._generate_refresh_token()

        await self.repo.create(server_refresh_token, user.id)
        return AuthLoginResponse(access_token=server_access_token, refresh_token=server_refresh_token)

    
    async def refresh(self, request: RefreshRequest) -> RefreshResponse:
        auth = await self.repo.get(request.model_dump())
        if not auth:
            raise RefreshTokenNotFoundError("Refresh token is expired or invalid.")

        access_token = self._generate_access_token(auth.user_id)
        return RefreshResponse(access_token=access_token)
        
            

    def _generate_access_token(self, user_id: int):
        to_encode = {"sub": user_id}
        expire = datetime.now(timezone.utc) + timedelta(minutes=AuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, AuthConfig.SECRET_KEY, algorithm=AuthConfig.ALGORITHM)
        return encoded_jwt
    

    def _generate_refresh_token(self):
        to_encode = {"sub": str(uuid4())}
        expire = datetime.now(timezone.utc) + timedelta(minutes=AuthConfig.REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, AuthConfig.SECRET_KEY, algorithm=AuthConfig.ALGORITHM)
        return encoded_jwt