from db.supabase import supabase
from schemas.activity import Activity, ActivityCreate
from datetime import datetime
from typing import List
import uuid


def create_activity(activity_data: ActivityCreate) -> Activity:
    """Create a new activity in the database."""
    response = (
        supabase.schema("public")
        .table("activity")
        .insert(activity_data.model_dump(mode="json"))
        .execute()
    )
    return Activity(**response.data[0])


def upsert_activity(activity_data: ActivityCreate) -> Activity:
    """Insert or update an activity (upsert on id)."""
    response = (
        supabase.schema("public")
        .table("activity")
        .upsert(activity_data.model_dump(mode="json"), ignore_duplicates=False)
        .execute()
    )
    return Activity(**response.data[0])


def get_user_activities(
    user_id: uuid.UUID, limit: int = 100, offset: int = 0
) -> List[Activity]:
    """Get all activities for a user, paginated."""
    response = (
        supabase.schema("public")
        .table("activity")
        .select("*")
        .eq("user_id", str(user_id))
        .order("start_date", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return [Activity(**item) for item in response.data]


def get_user_activities_count(user_id: uuid.UUID) -> int:
    """Get total count of activities for a user."""
    response = (
        supabase.schema("public")
        .table("activity")
        .select("id", count="exact")
        .eq("user_id", str(user_id))
        .execute()
    )
    return response.count
