from services.user_service import (
    create_user,
    update_strava_credentials,
    find_user_by_athlete_id,
)
from fastapi import APIRouter, BackgroundTasks
import asyncio

from schemas.auth import TokenExchangeRequest, TokenResponse
from services.strava_service import (
    exchange_code_for_token,
    refresh_token,
)
from services.auth_service import create_token_response
from services.sync_service import sync_user_activities, get_sync_progress

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _trigger_activity_sync(user_id: str, is_first_sync: bool):
    """Background task to sync activities."""
    try:
        asyncio.run(sync_user_activities(user_id, is_first_sync))
    except Exception as e:
        print(f"Error syncing activities: {str(e)}")


@router.post("/strava/callback")
async def strava_callback(
    request: TokenExchangeRequest, background_tasks: BackgroundTasks
) -> dict:
    """
    Handles the OAuth callback from Strava.
    Exchanges the authorization code for an access token.
    """
    strava_response = await exchange_code_for_token(request.code)

    # Check if user already exists
    existing_user = find_user_by_athlete_id(strava_response.athlete["id"])
    is_first_sync = existing_user is None or existing_user.last_synced is None

    # Create or get user
    user_details = {
        "strava_id": strava_response.athlete["id"],
        "name": f"{strava_response.athlete['firstname']} {strava_response.athlete['lastname']}",
        "profile_url": strava_response.athlete["profile_medium"],
    }
    user = create_user(user_details)

    # Update Strava tokens
    update_strava_credentials(strava_response)

    # Trigger background task to sync activities
    background_tasks.add_task(_trigger_activity_sync, str(user.id), is_first_sync)

    # Return token and sync info
    token_response = create_token_response(strava_response)
    return {
        **token_response.model_dump(),
        "should_sync": True,
        "is_first_sync": is_first_sync,
    }


@router.post("/strava/refresh")
async def refresh_strava_token(refresh_token_param: str) -> TokenResponse:
    """
    Refreshes an expired Strava access token.
    """
    strava_response = await refresh_token(refresh_token_param)
    return create_token_response(strava_response)


@router.get("/sync/progress/{user_id}")
async def get_activity_sync_progress(user_id: str) -> dict:
    """
    Get the current progress of activity syncing for a user.
    Frontend polls this endpoint to update the loading UI.
    """
    return get_sync_progress(user_id)
