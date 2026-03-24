import httpx
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException
from schemas.activity import ActivityCreate
from utils.type_utils import to_datetime
import uuid

STRAVA_API_BASE = "https://www.strava.com/api/v3"


async def get_athlete_activities(
    access_token: str,
    after: Optional[datetime] = None,
    per_page: int = 30,
) -> List[dict]:
    """
    Fetch activities from Strava API.

    Args:
        access_token: Strava OAuth access token
        after: Only return activities after this timestamp (for incremental syncs)
        per_page: Number of activities per page (max 200)

    Returns:
        List of activity dicts from Strava
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    all_activities = []
    page = 1

    try:
        async with httpx.AsyncClient() as client:
            while True:
                params = {
                    "per_page": per_page,
                    "page": page,
                }

                if after:
                    # Convert to Unix timestamp
                    params["after"] = int(after.timestamp())

                response = await client.get(
                    f"{STRAVA_API_BASE}/athlete/activities",
                    headers=headers,
                    params=params,
                    timeout=10.0,
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Failed to fetch Strava activities: {response.text}",
                    )

                activities = response.json()
                if not activities:
                    break

                all_activities.extend(activities)
                page += 1

    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500, detail=f"Error communicating with Strava API: {str(e)}"
        )

    return all_activities


def parse_strava_activity(strava_activity: dict, user_id: uuid.UUID) -> ActivityCreate:
    """
    Convert a Strava API activity response to our ActivityCreate schema.
    Only includes running activities.
    """
    # Only support running activities for now
    if strava_activity.get("type") != "Run":
        return None

    return ActivityCreate(
        id=strava_activity["id"],
        user_id=str(user_id),
        name=strava_activity.get("name", ""),
        type=strava_activity.get("type", "Run"),
        start_date=datetime.fromisoformat(
            strava_activity["start_date"].replace("Z", "+00:00")
        ),
        duration_seconds=strava_activity.get("moving_time", 0),
        distance_meters=strava_activity.get("distance", 0),
        average_speed=strava_activity.get("average_speed"),
        max_speed=strava_activity.get("max_speed"),
        elevation_gain_meters=strava_activity.get("total_elevation_gain"),
        average_heart_rate=strava_activity.get("average_heartrate"),
        max_heart_rate=strava_activity.get("max_heartrate"),
        gps_polyline=strava_activity.get("map", {}).get("summary_polyline"),
    )
