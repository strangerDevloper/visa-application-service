from datetime import datetime
from sqlalchemy.orm import Session
from app import models

def generate_visa_request_code(db: Session) -> str:
    """
    Generate a unique visa_request_code in the format VRDateMonthYearNumber.
    Example: VR080420251 for the first visa request on April 8, 2025.
    """
    # Get the current date in DDMMYYYY format
    current_date = datetime.utcnow().strftime("%d%m%Y")

    # Count the number of visa requests created today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)
    count_today = db.query(models.VisaRequest).filter(
        models.VisaRequest.created_date >= today_start,
        models.VisaRequest.created_date <= today_end
    ).count()

    # Increment the count to get the next unique number
    next_number = count_today + 1

    # Generate the visa_request_code
    visa_request_code = f"VR{current_date}{next_number}"
    return visa_request_code