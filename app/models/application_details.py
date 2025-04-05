from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    Boolean,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.models.enums import FIELD_TYPE_ENUM, DOCUMENT_TYPE_ENUM, VERIFICATION_STATUS_ENUM


Base = declarative_base()

class ApplicationDetails(Base):
    __tablename__ = "application_details"

    application_detail_id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey('applications.application_id'), nullable=False)  # Key name preserved
    document_code = Column(String(50), nullable=False, unique=True)
    field_name = Column(String(100), nullable=False)
    field_value = Column(String(100), nullable=False)
    field_title = Column(String(100), nullable=False)
    field_description = Column(String(255), nullable=True)
    field_type = Column(FIELD_TYPE_ENUM, nullable=False)
    document_type = Column(DOCUMENT_TYPE_ENUM, nullable=False)

    uploaded_date = Column(DateTime, server_default=func.now())
    verification_status = Column(VERIFICATION_STATUS_ENUM, default="PENDING")
    remark = Column(String, nullable=True)
    verified_by = Column(Integer, nullable=True)
    veerified_by_name = Column(String(100), nullable=True)
    verified_date = Column(DateTime, nullable=True)

    application = relationship('Applications', backref="application_details")
