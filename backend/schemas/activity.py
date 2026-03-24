from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


class Activity(BaseModel):
    id: int
    user_id: uuid.UUID
    name: str
    type: str
    start_date: datetime
    duration_seconds: float
    distance_meters: float
    average_speed: Optional[float] = None
    max_speed: Optional[float] = None
    elevation_gain_meters: Optional[float] = None
    average_heart_rate: Optional[float] = None
    max_heart_rate: Optional[float] = None
    gps_polyline: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ActivityCreate(BaseModel):
    id: int
    user_id: uuid.UUID
    name: str
    type: str
    start_date: datetime
    duration_seconds: float
    distance_meters: float
    average_speed: Optional[float] = None
    max_speed: Optional[float] = None
    elevation_gain_meters: Optional[float] = None
    average_heart_rate: Optional[float] = None
    max_heart_rate: Optional[float] = None
    gps_polyline: Optional[str] = None
