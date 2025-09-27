import httpx
from typing import Dict, Optional
from app.config import settings


class GoogleOAuth:
    """Google OAuth integration"""
    
    @staticmethod
    async def verify_token(token: str) -> Optional[Dict]:
        """Verify Google OAuth token and get user info"""
        try:
            async with httpx.AsyncClient() as client:
                # First, verify the token
                verify_response = await client.get(
                    f"https://oauth2.googleapis.com/tokeninfo?access_token={token}"
                )
                verify_response.raise_for_status()
                token_info = verify_response.json()
                
                # Then get user info
                user_response = await client.get(
                    "https://www.googleapis.com/oauth2/v2/userinfo",
                    headers={"Authorization": f"Bearer {token}"}
                )
                user_response.raise_for_status()
                user_info = user_response.json()
                
                return {
                    "provider_id": user_info["id"],
                    "email": user_info["email"],
                    "first_name": user_info.get("given_name", ""),
                    "last_name": user_info.get("family_name", ""),
                    "provider": "google"
                }
        except Exception:
            return None


class LinkedInOAuth:
    """LinkedIn OAuth integration"""
    
    @staticmethod
    async def verify_token(token: str) -> Optional[Dict]:
        """Verify LinkedIn OAuth token and get user info"""
        try:
            async with httpx.AsyncClient() as client:
                # Get user profile
                profile_response = await client.get(
                    "https://api.linkedin.com/v2/people/~:(id,firstName,lastName,emailAddress)",
                    headers={"Authorization": f"Bearer {token}"}
                )
                profile_response.raise_for_status()
                profile_data = profile_response.json()
                
                # Get email separately if needed
                email_response = await client.get(
                    "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))",
                    headers={"Authorization": f"Bearer {token}"}
                )
                email_response.raise_for_status()
                email_data = email_response.json()
                
                email = ""
                if email_data.get("elements"):
                    email = email_data["elements"][0]["handle~"]["emailAddress"]
                
                return {
                    "provider_id": profile_data["id"],
                    "email": email,
                    "first_name": profile_data.get("firstName", {}).get("localized", {}).get("en_US", ""),
                    "last_name": profile_data.get("lastName", {}).get("localized", {}).get("en_US", ""),
                    "provider": "linkedin"
                }
        except Exception:
            return None


async def verify_oauth_token(provider: str, token: str) -> Optional[Dict]:
    """Verify OAuth token for given provider"""
    if provider == "google":
        return await GoogleOAuth.verify_token(token)
    elif provider == "linkedin":
        return await LinkedInOAuth.verify_token(token)
    else:
        return None
