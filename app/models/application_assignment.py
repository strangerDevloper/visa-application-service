from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app.models.enums import ASSIGNMENT_STATUS_ENUM

Base = declarative_base()

class ApplicationAssignmentHistory(Base):
    __tablename__ = "application_assignment_history"

    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey('applications.application_id'), nullable=False)
    assigned_by = Column(Integer, nullable=False)
    assigned_by_name = Column(String(100), nullable=False)
    assigned_to_name = Column(String(100), nullable=False)
    assigned_to_user_id = Column(Integer, nullable=False)
    assigned_to_vendor_id = Column(Integer, nullable=False)
    assigned_to_employee_id = Column(Integer, nullable=True)
    assigned_date = Column(DateTime, server_default=func.now())
    remarks = Column(String, nullable=True)
    assignment_status = Column(ASSIGNMENT_STATUS_ENUM, nullable=True)


    application = relationship('Applications', backref="assignment_history")
