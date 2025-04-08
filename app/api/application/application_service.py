# crud.py
from datetime import datetime
import random
import string
from fastapi import HTTPException
from psycopg2 import IntegrityError
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app import models
from app.api.application.application_utils import generate_application_code, generate_visa_request_code
from app.core.constants import UserType
from .  import application_types


def create_visa_request(
    db: Session, 
    visa_request: application_types.VisaRequestCreate,
    user_details: dict
):
    """
    Create a new visa request.
    - Auto-generates `visa_request_code`.
    - Populates initiator details and user/vendor ID based on `user_details`.
    """
    # Auto-generate visa_request_code
    visa_request_code = generate_visa_request_code(db)

    # Populate initiator details and user/vendor ID based on user type
    initiator_name = user_details.get("name")
    initiator_email = user_details.get("email")
    initiator_phone = user_details.get("contact_number")
    initiator_address = user_details.get("address")

    user_id = None
    vendor_id = None
    if user_details.get("user_type") == UserType.USER:
        user_id = user_details.get("user_id")
    elif user_details.get("user_type") == UserType.VENDOR:
        vendor_id = user_details.get("user_id")

    # Prepare visa request data
    visa_request_data = visa_request.dict()
    visa_request_data["visa_request_code"] = visa_request_code
    visa_request_data["initiator_name"] = initiator_name
    visa_request_data["initiator_email"] = initiator_email
    visa_request_data["initiator_phone"] = initiator_phone
    visa_request_data["initiator_address"] = initiator_address
    visa_request_data["user_id"] = user_id
    visa_request_data["vendor_id"] = vendor_id

    # Create the visa request
    db_visa_request = models.VisaRequest(**visa_request_data)
    db.add(db_visa_request)
    db.commit()
    db.refresh(db_visa_request)
    return db_visa_request

def get_visa_requests(
    db: Session,
    filters: application_types.VisaRequestFilter,
    page: int = 1,
    per_page: int = 10
):
    """
    Get paginated visa requests with filtering
    """
    query = db.query(models.VisaRequest)
    
    # Apply filters
    if filters.user_id is not None:
        query = query.filter(models.VisaRequest.user_id == filters.user_id)
    if filters.vendor_id is not None:
        query = query.filter(models.VisaRequest.vendor_id == filters.vendor_id)
    if filters.counter_id is not None:
        query = query.filter(models.VisaRequest.counter_id == filters.counter_id)
    if filters.visa_process_id is not None:
        query = query.filter(models.VisaRequest.visa_process_id == filters.visa_process_id)
    if filters.initiator_name:
        query = query.filter(models.VisaRequest.initiator_name.ilike(f"%{filters.initiator_name}%"))
    if filters.visa_request_code:
        query = query.filter(models.VisaRequest.visa_request_code.ilike(f"%{filters.visa_request_code}%"))
    if filters.payment_status:
        query = query.filter(models.VisaRequest.payment_status == filters.payment_status)
    if filters.visa_status:
        query = query.filter(models.VisaRequest.visa_status == filters.visa_status)
    if filters.start_date and filters.end_date:
        query = query.filter(
            models.VisaRequest.created_date >= filters.start_date,
            models.VisaRequest.created_date <= filters.end_date
        )
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    visa_requests = query.order_by(
        models.VisaRequest.created_date.desc()
    ).offset(
        (page - 1) * per_page
    ).limit(
        per_page
    ).all()
    
    return {
        "items": visa_requests,
        "total": total,
        "page": page,
        "per_page": per_page
    }

def create_application_with_details(
    db: Session,
    application_data: application_types.ApplicationCreatePayload,
    user_details: dict
):
    """
    Create an application with its details and optional remarks in a single transaction
    """
    try:
        # Get visa request first to validate
        visa_request = db.query(models.VisaRequest).filter(
            models.VisaRequest.visa_request_id == application_data.visa_request_id
        ).first()
        
        if not visa_request:
            raise HTTPException(status_code=404, detail="Visa request not found")
        
        # Generate application code
        application_code = generate_application_code(db, visa_request.visa_request_code)
        
        # Create application
        db_application = models.Applications(
            visa_request_id=application_data.visa_request_id,
            application_code=application_code,
            applicant_first_name=application_data.applicant_first_name,
            applicant_middle_name=application_data.applicant_middle_name,
            applicant_last_name=application_data.applicant_last_name,
            applicant_email=application_data.applicant_email,
            applicant_phone=application_data.applicant_phone,
            applicant_passport_number=application_data.applicant_passport_number,
            applicant_dob=application_data.applicant_dob,
            applicant_gender=application_data.applicant_gender,
            application_status="DRAFT",  # Initial status
            expected_completion_date=application_data.expected_completion_date,
            application_notes=application_data.application_notes,
            is_priority=application_data.is_priority,
            is_escalated=application_data.is_escalated,
            # assigned_to and assigned_to_name remain None initially
        )
        
        db.add(db_application)
        db.flush()  # Flush to get the application_id
        
        # Create application details
        for detail in application_data.details:
            db_detail = models.ApplicationDetails(
                application_id=db_application.application_id,
                document_code=detail.document_code,
                field_name=detail.field_name,
                field_value=detail.field_value,
                field_title=detail.field_title,
                field_description=detail.field_description,
                field_type=detail.field_type,
                document_type=detail.document_type,
                verification_status="PENDING"  # Initial status
            )
            db.add(db_detail)
        
        # Create optional remarks
        if application_data.remarks:
            for remark in application_data.remarks:
                db_remark = models.ApplicationRemarks(
                    application_id=db_application.application_id,
                    remark_type=remark.remark_type,
                    remark_text=remark.remark_text,
                    user_id=remark.user_id,
                    vendor_id=remark.vendor_id,
                    employee_id=remark.employee_id,
                    name=remark.name,
                    is_internal=remark.is_internal
                )
                db.add(db_remark)
        
        db.commit()
        db.refresh(db_application)
        return db_application
    
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

def add_application_remark(
    db: Session,
    application_id: int,
    remark_data: application_types.ApplicationRemarkCreateRequest,
    user_details: dict
):
    """Add remark to an application"""
    # Verify application exists
    application = db.query(models.Applications).filter(
        models.Applications.application_id == application_id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Create remark
    db_remark = models.ApplicationRemarks(
        application_id=application_id,
        remark_type=remark_data.remark_type,
        remark_text=remark_data.remark_text,
        user_id=user_details.get("user_id"),
        vendor_id=user_details.get("vendor_id"),
        employee_id=user_details.get("employee_id"),
        name=user_details.get("name"),
        is_internal=remark_data.is_internal
    )
    
    db.add(db_remark)
    db.commit()
    db.refresh(db_remark)
    return db_remark

def update_application_metadata(
    db: Session,
    application_id: int,
    update_data: application_types.ApplicationUpdate
):
    """Update application metadata"""
    application = db.query(models.Applications).filter(
        models.Applications.application_id == application_id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Update only provided fields
    update_dict = update_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(application, field, value)
    
    # Handle priority/escalation logic
    if update_data.is_priority is not None:
        application.is_priority = update_data.is_priority
        if update_data.is_priority:
            application.is_escalated = True  # Auto-escalate if priority
    
    if update_data.is_escalated is not None:
        application.is_escalated = update_data.is_escalated
    
    application.modified_date = datetime.utcnow()
    
    db.commit()
    db.refresh(application)
    return application


def get_applications(
    db: Session,
    filters: application_types.ApplicationFilter,
    page: int = 1,
    per_page: int = 10
) -> dict:
    """Get applications with filtering and pagination"""
    query = db.query(models.Applications).join(models.VisaRequest)
    
    # Apply filters
    if filters.visa_request_code:
        query = query.filter(models.VisaRequest.visa_request_code.ilike(f"%{filters.visa_request_code}%"))
    if filters.application_code:
        query = query.filter(models.Applications.application_code.ilike(f"%{filters.application_code}%"))
    if filters.assigned_to:
        query = query.filter(models.Applications.assigned_to == filters.assigned_to)
    if filters.country_id:
        query = query.filter(models.VisaRequest.country_id == filters.country_id)
    if filters.applicant_name:
        query = query.filter(or_(
            models.Applications.applicant_first_name.ilike(f"%{filters.applicant_name}%"),
            models.Applications.applicant_last_name.ilike(f"%{filters.applicant_name}%")
        ))
    if filters.visa_process_id:
        query = query.filter(models.VisaRequest.visa_process_id == filters.visa_process_id)
    if filters.status:
        query = query.filter(models.Applications.application_status == filters.status)
    if filters.is_priority is not None:
        query = query.filter(models.Applications.is_priority == filters.is_priority)
    if filters.is_escalated is not None:
        query = query.filter(models.Applications.is_escalated == filters.is_escalated)
    if filters.start_date and filters.end_date:
        query = query.filter(and_(
            models.Applications.created_date >= filters.start_date,
            models.Applications.created_date <= filters.end_date
        ))
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    applications = query.order_by(
        models.Applications.created_date.desc()
    ).offset(
        (page - 1) * per_page
    ).limit(
        per_page
    ).all()
    
    return {
        "items": applications,
        "total": total,
        "page": page,
        "per_page": per_page
    }

def get_application_remarks(
    db: Session,
    application_id: int,
    filters: application_types.RemarkFilter,
    page: int = 1,
    per_page: int = 10
) -> dict:
    """Get remarks for an application with filtering"""
    query = db.query(models.ApplicationRemarks).filter(
        models.ApplicationRemarks.application_id == application_id
    )
    
    # Apply filters
    if filters.remark_type:
        query = query.filter(models.ApplicationRemarks.remark_type == filters.remark_type)
    if filters.is_internal:
        query = query.filter(models.ApplicationRemarks.is_internal == filters.is_internal)
    if filters.user_id:
        query = query.filter(models.ApplicationRemarks.user_id == filters.user_id)
    if filters.start_date and filters.end_date:
        query = query.filter(and_(
            models.ApplicationRemarks.created_date >= filters.start_date,
            models.ApplicationRemarks.created_date <= filters.end_date
        ))
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    remarks = query.order_by(
        models.ApplicationRemarks.created_date.desc()
    ).offset(
        (page - 1) * per_page
    ).limit(
        per_page
    ).all()
    
    return {
        "items": remarks,
        "total": total,
        "page": page,
        "per_page": per_page
    }

from datetime import datetime

# Mock function to simulate getting employee from another service
def get_internal_employee_details(employee_id: int) -> dict:
    """Mock function to get employee details"""
    # In real implementation, this would call another microservice
    return {
        "employee_id": employee_id,
        "name": f"Employee {employee_id}",
        "department": "Visa Processing"
    }

def submit_visa_request(
    db: Session,
    visa_request_id: int,
    submit_data: application_types.VisaRequestSubmit,
    user_details: dict
):
    """
    Submit a visa request and all its applications
    - Assigns all applications to an internal employee
    - Updates statuses to PENDING
    - Creates assignment records
    """
    try:
        # Get visa request with applications
        visa_request = db.query(models.VisaRequest).filter(
            models.VisaRequest.visa_request_id == visa_request_id
        ).first()
        
        if not visa_request:
            raise HTTPException(status_code=404, detail="Visa request not found")
        
        # Verify visa request is in DRAFT status
        if visa_request.visa_status != "DRAFT":
            raise HTTPException(
                status_code=400,
                detail="Visa request is not in DRAFT status"
            )
        
        # Get all applications for this visa request
        applications = db.query(models.Applications).filter(
            models.Applications.visa_request_id == visa_request_id
        ).all()
        
        if not applications:
            raise HTTPException(
                status_code=400,
                detail="No applications found for this visa request"
            )
        
        # Update visa request status
        visa_request.visa_status = "PENDING"
        visa_request.modified_date = datetime.utcnow()
        
        # Process each application
        for application in applications:
            # Update application status and assignment
            application.application_status = "PENDING"
            application.assigned_to = submit_data.assigned_to
            application.assigned_to_name = submit_data.assigned_to_name
            application.modified_date = datetime.utcnow()
            
            # Create assignment record
            assignment = models.ApplicationAssignmentHistory(
                application_id=application.application_id,
                assigned_by=user_details.get("user_id"),
                assigned_by_name=user_details.get("name"),
                assigned_to_name=submit_data.assigned_to_name,
                assigned_to_user_id=submit_data.assigned_to,
                assigned_to_vendor_id=None,  # Internal assignment
                assigned_to_employee_id=submit_data.assigned_to,
                remarks="Initial assignment on visa request submission",
                assignment_status="ASSIGNED"
            )
            db.add(assignment)
        
        db.commit()
        return visa_request
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def assign_application_to_employee(
    db: Session,
    application_id: int,
    assignment_data: application_types.AssignmentCreate,
    user_details: dict
):
    """
    Assign an individual application to an employee
    - Updates application assignment fields
    - Creates assignment history record
    """
    try:
        # Get the application
        application = db.query(models.Applications).filter(
            models.Applications.application_id == application_id
        ).first()
        
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        
        # Get employee details (mock for now)
        employee = get_internal_employee_details(assignment_data.assigned_to)
        
        # Update application assignment
        application.assigned_to = assignment_data.assigned_to
        application.assigned_to_name = assignment_data.assigned_to_name
        application.modified_date = datetime.utcnow()
        
        # Create assignment record
        assignment = models.ApplicationAssignmentHistory(
            application_id=application_id,
            assigned_by=user_details.get("user_id"),
            assigned_by_name=user_details.get("name"),
            assigned_to_name=assignment_data.assigned_to_name,
            assigned_to_user_id=assignment_data.assigned_to,
            assigned_to_vendor_id=None,  # Internal assignment
            assigned_to_employee_id=assignment_data.assigned_to,
            remarks=assignment_data.remarks or f"Reassigned to {assignment_data.assigned_to_name}",
            assignment_status="ASSIGNED"
        )
        db.add(assignment)
        
        db.commit()
        return application
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

def update_application_detail(
    db: Session,
    application_detail_id: int,
    update_data: application_types.ApplicationDetailUpdate,
    user_details: dict
):
    """
    Update application detail field
    - Can update field value, verification status, or add remark
    - Automatically approves application if all details are verified
    """
    try:
        # Get the application detail
        detail = db.query(models.ApplicationDetails).filter(
            models.ApplicationDetails.application_detail_id == application_detail_id
        ).first()
        
        if not detail:
            raise HTTPException(status_code=404, detail="Application detail not found")
        
        # Get the parent application
        application = db.query(models.Applications).filter(
            models.Applications.application_id == detail.application_id
        ).first()
        
        # Update fields if provided
        if update_data.field_value is not None:
            detail.field_value = update_data.field_value
        
        if update_data.verification_status is not None:
            detail.verification_status = update_data.verification_status
            detail.verified_by = user_details.get("user_id")
            detail.verified_by_name = user_details.get("name")
            detail.verified_date = datetime.utcnow()
        
        if update_data.remark is not None:
            # Add verification remark
            remark = models.ApplicationRemarks(
                application_id=detail.application_id,
                remark_type="VERIFICATION",
                remark_text=update_data.remark,
                user_id=user_details.get("user_id"),
                vendor_id=user_details.get("vendor_id"),
                name=user_details.get("name"),
                is_internal="YES"
            )
            db.add(remark)
        
        # Check if all details are verified
        all_details = db.query(models.ApplicationDetails).filter(
            models.ApplicationDetails.application_id == detail.application_id
        ).all()
        
        all_verified = all(
            d.verification_status == "VERIFIED" 
            for d in all_details
        )
        
        if all_verified:
            application.application_status = "APPROVED"
            application.modified_date = datetime.utcnow()
            
            # Add system remark
            remark = models.ApplicationRemarks(
                application_id=detail.application_id,
                remark_type="SYSTEM",
                remark_text="All documents verified - Application approved",
                user_id=user_details.get("user_id"),
                vendor_id=user_details.get("vendor_id"),
                name="System",
                is_internal="YES"
            )
            db.add(remark)
        
        db.commit()
        db.refresh(detail)
        return detail
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))