from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field


def utc_now_factory():
    return datetime.now(timezone.utc)


class Entity(BaseModel):
    id: int
    created_at: datetime = Field(default_factory=utc_now_factory)
    updated_at: datetime = Field(default_factory=utc_now_factory)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
    )


class Auth(Entity):
    # access_token: str
    refresh_token: str
    user_id: int


class User(Entity):
    email: str