from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config.hdrService import HdrService

security = HTTPBearer()
hdr_service = HdrService()  # Placeholder for the HdrService instance

def verify_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Function to verify the Bearer token.
    Replace this with your actual token verification logic.
    """
    print("credentials", credentials)  # For debugging purposes
    token = credentials.credentials
    # Add your token verification logic here (e.g., check against a database or decode it)
    if not token:  # Example validation
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    
    # Call the HdrService to fetch user details
    try:
        user_details = hdr_service.get_current_logged_in_user(token)
        user_details['access_token'] = token  # Add the token to the user details
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to fetch user details"
        ) from e

    print("user details " ,user_details)  # For debugging purposes
    return user_details