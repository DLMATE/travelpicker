from .base import RequestException


class InvalidAccessCodeError(RequestException):
    """
    소셜 로그인 인증 서버의 code가 유효하지 않음
    """
    pass


class InvalidTokenError(RequestException):
    pass


class ExpiredTokenError(RequestException):
    pass


class RefreshTokenNotFoundError(SystemError):
    pass