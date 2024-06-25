from abc import ABC, abstractmethod

import aiohttp
from fastapi import HTTPException, status

from config import GoogleConfig
from src.domain.value_object import SocialProfile
from src.domain.exception import InvalidAccessCodeError
from src.service.auth.token import AuthTokenService
from src.dto.auth import *
from src.dto import *


class AbstractSocialAuthService(ABC):
    def __init__(self, auth_token_service: AuthTokenService) -> None:
        self._auth_token_service = auth_token_service
        

    async def login(self, request: AuthLoginRequest) -> AuthLoginResponse:
        async with aiohttp.ClientSession() as session:
            access_token = await self._get_access_token(request.code, session)
            profile = await self._get_profile(access_token, session)
            return await self._auth_token_service.login(SocialProfile.model_validate(profile))


    @abstractmethod
    async def _get_access_token(self, code: str, session: aiohttp.ClientSession) -> str:
        pass


    @abstractmethod
    async def _get_profile(self, access_token: str, session: aiohttp.ClientSession) -> dict:
        pass


class GoogleAuthService(AbstractSocialAuthService):
    async def _get_access_token(self, code: str, session: aiohttp.ClientSession) -> str:
        token_data = {
            "code": code,
            "client_id": GoogleConfig.CLIENT_ID,
            "client_secret": GoogleConfig.CLIENT_SECRET,
            "redirect_uri": GoogleConfig.REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        async with session.post(url=GoogleConfig.TOKEN_URL, data=token_data) as response:
            if response.status != 200:
                raise InvalidAccessCodeError()
                # raise HTTPException(
                #     status_code=status.HTTP_400_BAD_REQUEST,
                #     detail="Failed to exchange authorization code for tokens",
                # )
            
            response = await response.json()
            return response["access_token"]
        

    async def _get_profile(self, access_token: str, session: aiohttp.ClientSession) -> dict:
        async with session.get(GoogleConfig.PROFILE_URL, headers={"Authorization": f"Bearer {access_token}"}) as response:
            return await response.json()