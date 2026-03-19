import os
from dotenv import load_dotenv
import httpx
from fastapi import HTTPException
from schemas.auth import StravaTokenResponse

load_dotenv()

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REDIRECT_URI = os.getenv(
    "STRAVA_REDIRECT_URI", "http://localhost:3000/auth/callback"
)


def get_strava_authorize_url() -> str:
    """
    Generates the Strava OAuth authorization URL.

    Returns:
        str: The authorization URL to redirect the user to
    """
    scope = "activity:read_all,athlete:read_all"

    strava_auth_url = (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={STRAVA_CLIENT_ID}&"
        f"redirect_uri={STRAVA_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope={scope}"
    )

    return strava_auth_url


async def exchange_code_for_token(code: str) -> StravaTokenResponse:
    """
    Exchanges an authorization code for a Strava access token.

    Args:
        code: The authorization code from Strava

    Returns:
        StravaTokenResponse: The token response from Strava

    Raises:
        HTTPException: If credentials are missing or token exchange fails
    """
    _validate_credentials()

    if not code:
        raise HTTPException(status_code=400, detail="Authorization code is missing")

    try:
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://www.strava.com/oauth/token",
                data={
                    "client_id": STRAVA_CLIENT_ID,
                    "client_secret": STRAVA_CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                },
            )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=401,
                detail="Failed to exchange authorization code for token",
            )

        token_data = token_response.json()
        return StravaTokenResponse(**token_data)

    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500, detail=f"Error communicating with Strava: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid response from Strava: {str(e)}"
        )


async def refresh_token(refresh_token: str) -> StravaTokenResponse:
    """
    Refreshes an expired Strava access token.

    Args:
        refresh_token: The refresh token from previous authentication

    Returns:
        StravaTokenResponse: The new token response from Strava

    Raises:
        HTTPException: If credentials are missing or token refresh fails
    """
    _validate_credentials()

    try:
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://www.strava.com/oauth/token",
                data={
                    "client_id": STRAVA_CLIENT_ID,
                    "client_secret": STRAVA_CLIENT_SECRET,
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                },
            )

        if token_response.status_code != 200:
            raise HTTPException(status_code=401, detail="Failed to refresh token")

        token_data = token_response.json()
        return StravaTokenResponse(**token_data)

    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500, detail=f"Error communicating with Strava: {str(e)}"
        )


def _validate_credentials() -> None:
    """
    Validates that required Strava credentials are configured.

    Raises:
        HTTPException: If credentials are not configured
    """
    if not STRAVA_CLIENT_ID or not STRAVA_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Strava credentials not configured")
