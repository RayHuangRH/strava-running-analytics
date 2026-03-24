from typing import List
import uuid
from datetime import datetime
from services.strava_activity_fetcher import (
    get_athlete_activities,
    parse_strava_activity,
)
from services.activity_service import upsert_activity
from services.user_service import get_strava_tokens, update_user_last_synced
from schemas.activity import ActivityCreate


class SyncProgress:
    def __init__(self, user_id: uuid.UUID):
        self.user_id = user_id
        self.total_activities = 0
        self.synced_activities = 0
        self.status = "initializing"
        self.start_time = datetime.utcnow()
        self.error = None

    def to_dict(self):
        return {
            "user_id": str(self.user_id),
            "total_activities": self.total_activities,
            "synced_activities": self.synced_activities,
            "progress_percent": (
                (self.synced_activities / self.total_activities * 100)
                if self.total_activities > 0
                else 0
            ),
            "status": self.status,
            "error": self.error,
        }


# Global sync progress tracker (in production, use Redis or database)
_sync_progress = {}


async def sync_user_activities(user_id: uuid.UUID, is_first_sync: bool = False):
    """
    Sync running activities for a user from Strava.

    If first_sync=True, fetch all activities.
    Otherwise, fetch only activities since last_synced.
    """
    progress = SyncProgress(user_id)
    _sync_progress[str(user_id)] = progress

    try:
        progress.status = "fetching_tokens"

        # Get user's Strava tokens
        tokens = get_strava_tokens(user_id)
        if not tokens:
            progress.error = "No Strava tokens found for user"
            progress.status = "error"
            return

        print(f"Starting sync for user {user_id}. Tokens: {tokens}")
        progress.status = "fetching_activities"

        # Determine if we need incremental or full sync
        after_time = None if is_first_sync else tokens.get("last_synced")

        # Fetch activities from Strava
        strava_activities = await get_athlete_activities(
            access_token=tokens["access_token"],
            after=after_time,
        )

        print(f"Fetched {len(strava_activities)} activities for user {user_id}")
        print(strava_activities)

        progress.total_activities = len(strava_activities)
        progress.status = "processing"

        # Parse and save activities
        running_activities = []
        for strava_activity in strava_activities:
            parsed = parse_strava_activity(strava_activity, user_id)
            if parsed:  # Only running activities
                running_activities.append(parsed)

        # Upsert all activities
        for activity in running_activities:
            try:
                upsert_activity(activity)
                progress.synced_activities += 1
            except Exception as e:
                # Log and continue with next activity
                print(f"Error syncing activity {activity.id}: {str(e)}")
                continue

        # Update last_synced timestamp
        progress.status = "finalizing"
        update_user_last_synced(user_id)

        progress.status = "completed"

    except Exception as e:
        progress.error = str(e)
        progress.status = "error"
        print(f"Error in sync_user_activities for {user_id}: {str(e)}")
        raise


def get_sync_progress(user_id: uuid.UUID) -> dict:
    """Get the current sync progress for a user."""
    progress = _sync_progress.get(str(user_id))
    if not progress:
        return {
            "user_id": str(user_id),
            "status": "not_started",
            "synced_activities": 0,
            "total_activities": 0,
            "progress_percent": 0,
        }
    return progress.to_dict()
