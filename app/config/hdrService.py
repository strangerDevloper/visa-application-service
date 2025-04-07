import os
from fastapi import HTTPException, status
import requests

from app.config.settings import settings

class HdrService:
    def __init__(self):
        """
        Initialize the HdrService with the base URL from environment variables.
        """
        # Fetch the base URL from environment variables
        self.base_url =  settings.BASE_URL

        if not self.base_url:
            raise ValueError("HDR_SERVICE_BASE_URL environment variable is not set.")

    def get_current_logged_in_user(self, auth_token: str) -> dict:
        """
        Fetch the current logged-in user by hitting the /api/me endpoint.
        :param auth_token: The authorization token to be passed in the headers.
        :return: A dictionary containing the user details or an error message.
        """
        url = f"{self.base_url}/api/me"
        print("url", url)
        print("auth_token", auth_token)
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Failed to fetch user details"
                )
            user_details = response.json()
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error while communicating with the authentication service"
            ) from e
        
        return user_details