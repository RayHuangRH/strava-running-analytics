from pydantic import BaseModel
import uuid
from supabase_auth import datetime


class User(BaseModel):
    id: uuid.UUID
    strava_id: int
    name: str
    profile_url: str
    created_at: datetime


class StravaTokens(BaseModel):
    user_id: uuid.UUID
    access_token: str
    refresh_token: str
    expires_at: datetime
    created_at: datetime
