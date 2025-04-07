# app/api/application/application_routes.py
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.config.database import get_db
from app.api.application import application_types, application_service
from app.helpers.auth import verify_bearer_token

router = APIRouter(prefix="/application", tags=["application"])

@router.post("/visa-requests/", response_model=application_types.VisaRequest)
def create_visa_request(
    visa_request: application_types.VisaRequestCreate,
    db: Session = Depends(get_db),
    user_details: dict = Depends(verify_bearer_token)  # Add this dependency
):
    # Pass user_details to the service layer
    return application_service.create_visa_request(
        db=db, 
        visa_request=visa_request,
        user_details=user_details
    )


@router.get("/visa-requests/", response_model=application_types.PaginatedResponse)
def get_visa_requests(
    user_id: Optional[int] = Query(None),
    vendor_id: Optional[int] = Query(None),
    counter_id: Optional[int] = Query(None),
    visa_process_id: Optional[int] = Query(None),
    initiator_name: Optional[str] = Query(None),
    visa_request_code: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    payment_status: Optional[application_types.PaymentStatusEnum] = Query(None),
    visa_status: Optional[application_types.VisaStatusEnum] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user_details: dict = Depends(verify_bearer_token)
):
    """
    Get all visa requests with pagination and filtering
    
    Available filters:
    - user_id: Filter by user ID
    - vendor_id: Filter by vendor ID
    - counter_id: Filter by counter ID
    - visa_process_id: Filter by visa process ID
    - initiator_name: Filter by initiator name (partial match)
    - visa_request_code: Filter by visa request code (partial match)
    - start_date/end_date: Date range filter
    - payment_status: Filter by payment status
    - visa_status: Filter by visa status
    
    Pagination:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10, max: 100)
    """
    filters = application_types.VisaRequestFilter(
        user_id=user_id,
        vendor_id=vendor_id,
        counter_id=counter_id,
        visa_process_id=visa_process_id,
        initiator_name=initiator_name,
        visa_request_code=visa_request_code,
        start_date=start_date,
        end_date=end_date,
        payment_status=payment_status,
        visa_status=visa_status
    )
    
    return application_service.get_visa_requests(
        db=db,
        filters=filters,
        page=page,
        per_page=per_page
    )


@router.post("/visa-requests/{visa_request_id}/applications", 
            response_model=application_types.ApplicationWithDetails,
            status_code=201)
def create_application_in_visa_request(
    visa_request_id: int,
    application: application_types.ApplicationCreatePayload,
    db: Session = Depends(get_db),
    user_details: dict = Depends(verify_bearer_token)
):
    """
    Create a new application within a visa request
    
    - Creates the application with status DRAFT
    - Creates all associated application details
    - Creates optional remarks if provided
    - assigned_to and assigned_to_name remain null initially
    - Returns the complete application with details
    """
    # Validate visa_request_id matches payload
    if visa_request_id != application.visa_request_id:
        raise HTTPException(
            status_code=400,
            detail="Visa request ID in path and payload don't match"
        )
    
    return application_service.create_application_with_details(
        db=db,
        application_data=application,
        user_details=user_details
    )

@router.post("/applications/{application_id}/remarks", 
            response_model=application_types.ApplicationRemark,
            status_code=201)
def create_application_remark(
    application_id: int,
    remark: application_types.ApplicationRemarkCreateRequest,
    db: Session = Depends(get_db),
    user_details: dict = Depends(verify_bearer_token)
):
    """
    Add a remark to an application
    
    - User details (user_id, vendor_id, etc.) are automatically taken from auth token
    - Only remark text and type need to be provided in payload
    """
    return application_service.add_application_remark(
        db=db,
        application_id=application_id,
        remark_data=remark,
        user_details=user_details
    )

@router.put("/applications/{application_id}", 
           response_model=application_types.Application)
def update_application(
    application_id: int,
    update_data: application_types.ApplicationUpdate,
    db: Session = Depends(get_db),
    user_details: dict = Depends(verify_bearer_token)
):
    """
    Update application metadata
    
    - Cannot update application_code or other system-generated fields
    - Setting is_priority=True automatically sets is_escalated=True
    - All fields are optional (only provided fields will be updated)
    """
    return application_service.update_application_metadata(
        db=db,
        application_id=application_id,
        update_data=update_data
    )

@router.get("/applications/", response_model=application_types.PaginatedResponse)
def get_filtered_applications(
    visa_request_code: Optional[str] = Query(None),
    application_code: Optional[str] = Query(None),
    assigned_to: Optional[int] = Query(None),
    country_id: Optional[int] = Query(None),
    applicant_name: Optional[str] = Query(None),
    visa_process_id: Optional[int] = Query(None),
    status: Optional[application_types.APPLICATION_STATUS_ENUM] = Query(None),
    is_priority: Optional[bool] = Query(None),
    is_escalated: Optional[bool] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user_details: dict = Depends(verify_bearer_token)
):
    """
    Get applications with filtering
    
    Available filters:
    - visa_request_code: Filter by visa request code
    - application_code: Filter by application code
    - assigned_to: Filter by assigned user ID
    - country_id: Filter by country ID
    - applicant_name: Filter by applicant name (partial match)
    - visa_process_id: Filter by visa process ID
    - status: Filter by application status
    - is_priority: Filter by priority flag
    - is_escalated: Filter by escalation flag
    - start_date/end_date: Date range filter
    """
    filters = application_types.ApplicationFilter(
        visa_request_code=visa_request_code,
        application_code=application_code,
        assigned_to=assigned_to,
        country_id=country_id,
        applicant_name=applicant_name,
        visa_process_id=visa_process_id,
        status=status,
        is_priority=is_priority,
        is_escalated=is_escalated,
        start_date=start_date,
        end_date=end_date
    )
    
    return application_service.get_applications(
        db=db,
        filters=filters,
        page=page,
        per_page=per_page
    )

@router.get("/applications/{application_id}/remarks", 
           response_model=application_types.PaginatedResponse)
def get_application_remarks(
    application_id: int,
    remark_type: Optional[application_types.RemarkTypeEnum] = Query(None),
    is_internal: Optional[application_types.IsInternalEnum] = Query(None),
    user_id: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user_details: dict = Depends(verify_bearer_token)
):
    """
    Get remarks for an application with filtering
    
    Available filters:
    - remark_type: Filter by remark type
    - is_internal: Filter by internal/external remarks
    - user_id: Filter by user who created the remark
    - start_date/end_date: Date range filter
    """
    filters = application_types.RemarkFilter(
        remark_type=remark_type,
        is_internal=is_internal,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )
    
    return application_service.get_application_remarks(
        db=db,
        application_id=application_id,
        filters=filters,
        page=page,
        per_page=per_page
    )

@router.post("/visa-requests/{visa_request_id}/submit",
            response_model=application_types.VisaRequest,
            status_code=200)
def submit_visa_request(
    visa_request_id: int,
    submit_data: application_types.VisaRequestSubmit,
    db: Session = Depends(get_db),
    user_details: dict = Depends(verify_bearer_token)
):
    """
    Submit a visa request and all its applications
    - Changes status to PENDING for visa request and all applications
    - Assigns all applications to the specified employee
    - Creates assignment history records
    - Requires visa request to be in DRAFT status
    """
    return application_service.submit_visa_request(
        db=db,
        visa_request_id=visa_request_id,
        submit_data=submit_data,
        user_details=user_details
    )

@router.post("/applications/{application_id}/assign",
            response_model=application_types.Application,
            status_code=200)
def assign_application(
    application_id: int,
    assignment_data: application_types.AssignmentCreate,
    db: Session = Depends(get_db),
    user_details: dict = Depends(verify_bearer_token)
):
    """
    Assign an individual application to an employee
    - Updates assigned_to and assigned_to_name in application
    - Creates an assignment history record
    - Can be used for initial assignment or reassignment
    """
    return application_service.assign_application_to_employee(
        db=db,
        application_id=application_id,
        assignment_data=assignment_data,
        user_details=user_details
    )