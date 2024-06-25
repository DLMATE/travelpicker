__all__ = ["AuthLoginRequest", "AuthLoginResponse", "RefreshRequest", "RefreshResponse"]

from pydantic import BaseModel, field_validator
import jwt

from config import AuthConfig
from src.domain.exception import InvalidTokenError, ExpiredTokenError, RequestException


class AuthLoginRequest(BaseModel):
    code: str


class AuthLoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshRequest(BaseModel):
    refresh_token: str

    @field_validator('refresh_token')
    @classmethod
    def check_token_is_valid(cls, token: str) -> str:
        try:
            jwt.decode(token, AuthConfig.SECRET_KEY, algorithms=[AuthConfig.ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()
        except:
            raise RequestException()
        else:
            return token


class RefreshResponse(BaseModel):
    access_token: str