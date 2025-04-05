# crud.py
from sqlalchemy.orm import Session

from app import models
from .  import application_types


def create_visa_request(db: Session, visa_request: application_types.VisaRequestCreate):
    db_visa_request = models.VisaRequest(**visa_request.dict())
    db.add(db_visa_request)
    db.commit()
    db.refresh(db_visa_request)
    return db_visa_request

def get_visa_request(db: Session, visa_request_id: int):
    return db.query(models.VisaRequest).filter(models.VisaRequest.visa_request_id == visa_request_id).first()

def get_visa_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.VisaRequest).offset(skip).limit(limit).all()

def create_application(db: Session, application: application_types.ApplicationCreate):
    db_application = models.Applications(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_application(db: Session, application_id: int):
    return db.query(models.Applications).filter(models.Applications.application_id == application_id).first()

def get_applications_by_request(db: Session, visa_request_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Applications).filter(models.Applications.visa_request_id == visa_request_id).offset(skip).limit(limit).all()

def create_application_detail(db: Session, detail: application_types.ApplicationDetailCreate):
    db_detail = models.ApplicationDetails(**detail.dict())
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail

def get_application_details(db: Session, application_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.ApplicationDetails).filter(models.ApplicationDetails.application_id == application_id).offset(skip).limit(limit).all()

def create_application_remark(db: Session, remark: application_types.ApplicationRemarkCreate):
    db_remark = models.ApplicationRemarks(**remark.dict())
    db.add(db_remark)
    db.commit()
    db.refresh(db_remark)
    return db_remark

def get_application_remarks(db: Session, application_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.ApplicationRemarks).filter(models.ApplicationRemarks.application_id == application_id).offset(skip).limit(limit).all()

def create_assignment_history(db: Session, assignment: application_types.AssignmentHistoryCreate):
    db_assignment = models.ApplicationAssignmentHistory(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def get_assignment_history(db: Session, application_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.ApplicationAssignmentHistory).filter(models.ApplicationAssignmentHistory.application_id == application_id).offset(skip).limit(limit).all()