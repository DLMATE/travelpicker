from pydantic import BaseModel


class SocialProfile(BaseModel):
    email: str