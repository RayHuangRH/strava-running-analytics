from utils.type_utils import to_datetime
from db.supabase import supabase
from schemas.user import User


def find_user_by_athlete_id(strava_id: int) -> User:
    user = (
        supabase.schema("public")
        .table("users")
        .select("*")
        .eq("strava_id", strava_id)
        .execute()
    )
    if user.data:
        return User(**user.data[0])
    return None


def create_user(user_data: dict) -> User:
    user = find_user_by_athlete_id(user_data["strava_id"])
    if user:
        return user
    response = supabase.schema("public").table("users").insert(user_data).execute()
    return User(**response.data[0])


def update_strava_credentials(strava_response_data: dict) -> None:
    user = find_user_by_athlete_id(strava_response_data.athlete["id"])
    if not user:
        raise ValueError("User not found for strava_credentials update")

    strava_token_data = {
        "user_id": str(user.id),
        "access_token": strava_response_data.access_token,
        "refresh_token": strava_response_data.refresh_token,
        "expires_at": to_datetime(strava_response_data.expires_at).isoformat(),
    }
    supabase.schema("public").table("strava_tokens").upsert(strava_token_data).execute()
