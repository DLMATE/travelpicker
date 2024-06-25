from fastapi import APIRouter, Security, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from fastapi.security import APIKeyHeader
import jwt

from config import GoogleConfig, AuthConfig
from src.service.auth import *
from src.service.user import UserService
from src.repository.auth import AuthMemoryRepository
from src.repository.user import UserMemoryRepository
from src.dto.auth import *
from src.dto import ResponseFailureItem, ResponseTypes, ResponseModel
from app.utils import verify_header


router = APIRouter(prefix="/auth", tags=["Auth"])


def format_message(msg: str| Exception) -> str:
    if isinstance(msg, Exception):
        return "{}: {}".format(
            msg.__class__.__name__, "{}".format(msg)
        )
    return msg


data = {
    "User": [],
    "Auth": [],
}

auth_repo = AuthMemoryRepository(data)
user_repo = UserMemoryRepository(data)


@router.get("/login/google")
async def google_login():
    return RedirectResponse(GoogleConfig.LOGIN_URL)


@router.get("/login/google/callback")
async def callback(code: str) -> AuthLoginResponse:
    request = AuthLoginRequest(code=code)
    service = GoogleAuthService(AuthTokenService(auth_repo, UserService(user_repo)))
    response = await service.login(request)
    print(data)
    return response


@router.get("/token/refresh")
async def refresh(refreshToken: str) -> RefreshResponse:
    try:
        request = RefreshRequest(refresh_token=refreshToken)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=format_message(exc))
    
    try:
        service = AuthTokenService(auth_repo, UserService(user_repo))
        response = await service.refresh(request)
        return response
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=format_message(exc))


@router.get("/test", dependencies=[Depends(verify_header)])
async def test():
    return "test success"