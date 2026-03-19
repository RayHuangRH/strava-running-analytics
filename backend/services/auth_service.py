import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import jwt
from typing import Dict, Any

from schemas.auth import StravaTokenResponse, TokenResponse

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


def create_jwt_token(strava_response: StravaTokenResponse) -> str:
    """
    Creates a JWT token from a Strava token response.

    Args:
        strava_response: The response from Strava containing athlete and token info

    Returns:
        str: Encoded JWT token
    """
    jwt_payload = {
        "athlete_id": strava_response.athlete["id"],
        "athlete_username": strava_response.athlete.get("username"),
        "strava_access_token": strava_response.access_token,
        "strava_refresh_token": strava_response.refresh_token,
        "strava_token_expires_at": strava_response.expires_at,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow(),
    }

    return jwt.encode(jwt_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_token_response(strava_response: StravaTokenResponse) -> TokenResponse:
    """
    Creates a TokenResponse from a Strava token response.

    Args:
        strava_response: The response from Strava

    Returns:
        TokenResponse: The token response to send to the frontend
    """
    jwt_token = create_jwt_token(strava_response)

    return TokenResponse(
        accessToken=jwt_token,
        refreshToken=strava_response.refresh_token,
        athlete=strava_response.athlete,
        expiresIn=strava_response.expires_in,
    )


def decode_jwt_token(token: str) -> Dict[str, Any]:
    """
    Decodes and validates a JWT token.

    Args:
        token: The JWT token to decode

    Returns:
        Dict: The decoded token payload

    Raises:
        jwt.InvalidTokenError: If the token is invalid
    """
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
