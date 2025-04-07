from datetime import datetime
import random
import string
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


def generate_application_code(db: Session) -> str:
    """
    Generate a unique application code in format: APPYYMMDDXXX
    Where:
    - APP: Constant prefix for applications
    - YYMMDD: Current date (year, month, day)
    - XXX: 3 random uppercase letters
    
    Example: APP250408ABC
    """
    # Current date in YYMMDD format
    date_part = datetime.utcnow().strftime("%y%m%d")
    
    # Generate 3 random uppercase letters
    random_part = ''.join(random.choices(string.ascii_uppercase, k=3))
    
    # Construct base code
    base_code = f"APP{date_part}{random_part}"
    
    # Verify uniqueness and generate alternatives if needed
    counter = 1
    final_code = base_code
    while db.query(models.Applications).filter(
        models.Applications.application_code == final_code
    ).count() > 0:
        # If exists, try adding a number suffix
        final_code = f"{base_code}{counter}"
        counter += 1
        if counter > 100:  # Safety limit
            # Fallback to timestamp if too many collisions
            timestamp = int(datetime.utcnow().timestamp() % 10000)
            final_code = f"APP{timestamp}{random_part}"
            break
    
    return final_code