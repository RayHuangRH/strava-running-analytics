from services.user_service import create_user, update_strava_credentials
from fastapi import APIRouter

from schemas.auth import TokenExchangeRequest, TokenResponse
from services.strava_service import (
    get_strava_authorize_url,
    exchange_code_for_token,
    refresh_token,
)
from services.auth_service import create_token_response

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/strava/authorize")
async def authorize_strava():
    """
    Initiates the Strava OAuth login flow.
    Frontend should redirect user to this endpoint or directly to Strava.
    """
    auth_url = get_strava_authorize_url()
    return {"authUrl": auth_url}


@router.post("/strava/callback")
async def strava_callback(request: TokenExchangeRequest) -> TokenResponse:
    """
    Handles the OAuth callback from Strava.
    Exchanges the authorization code for an access token.
    """
    strava_response = await exchange_code_for_token(request.code)
    print(strava_response)
    #     token_type='Bearer' expires_at=1773954791 expires_in=16980 refresh_token='5daed33ec6823edfe9cc4b80a5aad475ecccbd8c' access_token='e48954d7a7e5d3796ac82b00f1caedc1d416a7b4' athlete={'id': 153834618, 'username': None,
    # 'resource_state': 2, 'firstname': 'Raymond', 'lastname': 'Huang', 'bio': None, 'city': 'Brooklyn', 'state':
    # 'New York', 'country': 'United States', 'sex': 'M', 'premium': False, 'summit': False, 'created_at': '2024-12-14T16:32:45Z', 'updated_at': '2025-07-23T00:09:09Z', 'badge_type_id':
    # 0, 'profile_medium': 'https://dgalywyr863hv.cloudfront.net/pictures/athletes/153834618/41638503/1/medium.jpg', 'profile': 'https://dgalywyr863hv.cloudfront.net/pictures/athletes/153834618/41638503/1/large.jpg', 'friend': None, 'follower': None}
    user_details = {
        "strava_id": strava_response.athlete["id"],
        "name": f"{strava_response.athlete['firstname']} {strava_response.athlete['lastname']}",
        "profile_url": strava_response.athlete["profile_medium"],
    }
    user = create_user(user_details)
    print(f"User created or found: {user}")
    update_strava_credentials(strava_response)
    return create_token_response(strava_response)


@router.post("/strava/refresh")
async def refresh_strava_token(refresh_token_param: str) -> TokenResponse:
    """
    Refreshes an expired Strava access token.
    """
    strava_response = await refresh_token(refresh_token_param)
    return create_token_response(strava_response)
