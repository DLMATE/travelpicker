from typing import Dict, Any

from fastapi import Security, status, HTTPException
from fastapi.security import APIKeyHeader
import jwt

from config import AuthConfig
from src.dto import ResponseTypes, ResponseFailureItem
from src.domain.exception import ExpiredTokenError, InvalidTokenError


def format_message(msg: str| Exception) -> str:
    if isinstance(msg, Exception):
        return "{}: {}".format(
            msg.__class__.__name__, "{}".format(msg)
        )
    return msg


def decode_token(access_token: str) -> dict:
    try:
        payload = jwt.decode(access_token, AuthConfig.SECRET_KEY, algorithms=[AuthConfig.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()
    return payload


def verify_header(access_token=Security(APIKeyHeader(name='access_token'))) -> int:
    try:
        payload = decode_token(access_token)
    except ExpiredTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=format_message(exc))
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=format_message(exc))
    else:
        user_id = payload["sub"]
        return user_id


# STATUS_CODES = {
#     ResponseTypes.SUCCESS: status.HTTP_200_OK,
#     ResponseTypes.RESOURCE_ERROR: status.HTTP_404_NOT_FOUND,
#     ResponseTypes.PARAMETERS_ERROR: status.HTTP_400_BAD_REQUEST,
#     ResponseTypes.SYSTEM_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
# }


def common_response() -> Dict[int, Dict[str, Any]]:
    return {
        status.HTTP_404_NOT_FOUND: {
            "description": "404 Not Found"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Parameters is not valid",
            "model": ResponseFailureItem,
            "content": {
                "application/json": {
                    "example": {"type": ResponseTypes.PARAMETERS_ERROR, "value": "message"}
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "System Error",
            "model": ResponseFailureItem,
            "content": {
                "application/json": {
                    "example": {"type": ResponseTypes.SYSTEM_ERROR, "value": "message"}
                }
            },
        },
    }