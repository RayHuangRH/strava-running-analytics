from typing import Optional
from pydantic import BaseModel


class TokenExchangeRequest(BaseModel):
    code: str
    state: Optional[str] = None


class TokenResponse(BaseModel):
    accessToken: str
    refreshToken: Optional[str] = None
    athlete: dict
    expiresIn: int


class StravaTokenResponse(BaseModel):
    token_type: str
    expires_at: int
    expires_in: int
    refresh_token: str
    access_token: str
    athlete: dict
