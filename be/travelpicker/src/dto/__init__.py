from __future__ import annotations

__all__ = ["ResponseTypes", "Response"]

from typing import TypeVar, Generic, Union
from enum import Enum

from pydantic import BaseModel, field_validator, ConfigDict


class ResponseTypes(Enum):
    PARAMETERS_ERROR = "ParametersError"
    RESOURCE_ERROR = "ResourceError"
    SYSTEM_ERROR = "SystemError"
    SUCCESS = "Success"


class ResponseFailureItem(BaseModel):
    type: ResponseTypes
    message: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            ResponseTypes: lambda x: x.value
        }
    )

    @field_validator('type')
    @classmethod
    def type_must_not_equal_success(cls, type: ResponseTypes) -> ResponseTypes:
        if type == ResponseTypes.SUCCESS:
            raise Exception("ResponseFailureItem의 type은 SUCCESS일 수 없습니다.")
        return type

    @field_validator('message', mode='before')
    @classmethod
    def _format_message(cls, msg: str| Exception) -> str:
        if isinstance(msg, Exception):
            return "{}: {}".format(
                msg.__class__.__name__, "{}".format(msg)
            )
        return msg
    

T = TypeVar('T', bound = BaseModel | None)
ResponseModel = TypeVar('ResponseModel', bound = BaseModel | None | ResponseFailureItem)
    

class Response(Generic[T]):
    type: ResponseTypes
    value: T | ResponseFailureItem

    def __init__(self, type: ResponseTypes, value: ResponseModel):
        self.type = type
        self.value = value

    def __bool__(self):
        return True

    @classmethod
    def success(cls, value: T) -> Response:
        return cls(
            type=ResponseTypes.SUCCESS,
            value=value
        )
    
    @classmethod
    def fail(cls, type: ResponseTypes, message: str | Exception) -> Response:
        res = cls(
            type=type,
            value=ResponseFailureItem(type=type, message=message)
        )
        res.__bool__ = False
        return res