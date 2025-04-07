# app/api/application/application_routes.py
import random
import string
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

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


@router.get("/visa-requests/", response_model=List[application_types.VisaRequest])
def read_visa_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    visa_requests = application_service.get_visa_requests(db, skip=skip, limit=limit)
    return visa_requests

@router.get("/visa-requests/{visa_request_id}", response_model=application_types.VisaRequestWithApplications)
def read_visa_request(visa_request_id: int, db: Session = Depends(get_db)):
    db_visa_request = application_service.get_visa_request(db, visa_request_id=visa_request_id)
    if db_visa_request is None:
        raise HTTPException(status_code=404, detail="Visa request not found")
    return db_visa_request

@router.post("/applications/", response_model=application_types.Application)
def create_application(application: application_types.ApplicationCreate, db: Session = Depends(get_db)):
    return application_service.create_application(db=db, application=application)

@router.get("/applications/{application_id}", response_model=application_types.ApplicationWithDetails)
def read_application(application_id: int, db: Session = Depends(get_db)):
    db_application = application_service.get_application(db, application_id=application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application

@router.get("/visa-requests/{visa_request_id}/applications/", response_model=List[application_types.Application])
def read_applications_by_request(visa_request_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return application_service.get_applications_by_request(db, visa_request_id=visa_request_id, skip=skip, limit=limit)

@router.post("/application-details/", response_model=application_types.ApplicationDetail)
def create_application_detail(detail: application_types.ApplicationDetailCreate, db: Session = Depends(get_db)):
    return application_service.create_application_detail(db=db, detail=detail)

@router.get("/applications/{application_id}/details/", response_model=List[application_types.ApplicationDetail])
def read_application_details(application_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return application_service.get_application_details(db, application_id=application_id, skip=skip, limit=limit)

@router.post("/application-remarks/", response_model=application_types.ApplicationRemark)
def create_application_remark(remark: application_types.ApplicationRemarkCreate, db: Session = Depends(get_db)):
    return application_service.create_application_remark(db=db, remark=remark)

@router.get("/applications/{application_id}/remarks/", response_model=List[application_types.ApplicationRemark])
def read_application_remarks(application_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return application_service.get_application_remarks(db, application_id=application_id, skip=skip, limit=limit)

@router.post("/assignment-history/", response_model=application_types.AssignmentHistory)
def create_assignment_history(assignment: application_types.AssignmentHistoryCreate, db: Session = Depends(get_db)):
    return application_service.create_assignment_history(db=db, assignment=assignment)

@router.get("/applications/{application_id}/assignment-history/", response_model=List[application_types.AssignmentHistory])
def read_assignment_history(application_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return application_service.get_assignment_history(db, application_id=application_id, skip=skip, limit=limit)