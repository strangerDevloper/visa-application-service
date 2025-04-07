from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.models.enums import GENDER_ENUM, APPLICATION_STATUS_ENUM


class Applications(Base):
    __tablename__ = "applications"

    application_id = Column(Integer, primary_key=True, autoincrement=True)
    visa_request_id = Column(Integer, ForeignKey('visa_request.visa_request_id'), nullable=False)
    application_code = Column(String(50), nullable=False, unique=True)

    applicant_first_name = Column(String(100), nullable=False)
    applicant_middle_name = Column(String(100), nullable=True)
    applicant_last_name = Column(String(100), nullable=True)
    applicant_email = Column(String(100), nullable=False)
    applicant_phone = Column(String(20), nullable=False)
    applicant_passport_number = Column(String(50), nullable=False)
    applicant_dob = Column(DateTime, nullable=False)
    applicant_gender = Column(GENDER_ENUM, nullable=False)
    
    application_status = Column(APPLICATION_STATUS_ENUM, default="PENDING")
    submission_date = Column(DateTime, server_default=func.now())
    modified_date = Column(DateTime, onupdate=func.now())
    active_status = Column(Boolean, default=True)

    assigned_to = Column(Integer, nullable=True)
    assigned_to_name = Column(String(100), nullable=True)

    expected_completion_date = Column(DateTime, nullable=True)
    application_notes = Column(String, nullable=True)

    is_priority = Column(Boolean, default=False)
    is_escilated = Column(Boolean, default=False)

    # Relationships
    visa_request = relationship('VisaRequest', back_populates="applications")
    details = relationship('ApplicationDetails', back_populates="application", 
                         cascade="all, delete-orphan")
    remarks = relationship('ApplicationRemarks', back_populates="application",
                         cascade="all, delete-orphan")
    assignments = relationship('ApplicationAssignmentHistory', back_populates="application",
                             cascade="all, delete-orphan")