__all__ = ["AppConfig", "GoogleConfig", "AuthConfig"]

import os
from abc import ABC, abstractmethod


class Config(ABC):
    
    @classmethod
    @abstractmethod
    def setup(*args, **kwargs) -> None:
        pass


class AppConfig(Config):
    HOST: str
    PORT: int

    @classmethod
    def setup(cls):
        cls.HOST = os.environ.get("APP_HOST", "localhost")
        cls.PORT = int(os.environ.get("APP_PORT", "8000"))


class GoogleConfig(Config):
    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str
    LOGIN_URL: str
    TOKEN_URL: str
    PROFILE_URL: str
    
    @classmethod
    def setup(cls, host: str, port: int) -> None:
        cls.CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
        cls.CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
        cls.REDIRECT_URI = f"http://{host}:{port}/auth/login/google/callback"
        cls.LOGIN_URL = (
            "https://accounts.google.com/o/oauth2/auth"
            "?response_type=code"
            f"&client_id={cls.CLIENT_ID}"
            f"&redirect_uri={cls.REDIRECT_URI}"
            "&scope=openid%20email%20"
        )
        cls.TOKEN_URL = "https://oauth2.googleapis.com/token"
        cls.PROFILE_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


class AuthConfig(Config):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    @classmethod
    def setup(cls) -> None:
        cls.SECRET_KEY = os.environ.get("AUTH_SECRET_KEY")
        cls.ALGORITHM = os.environ.get("AUTH_ALGORITHM", "HS256")
        cls.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        cls.REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", 14*24*60))