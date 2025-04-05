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

from app.models.enums import COUPON_TYPE_ENUM, PAYMENT_STATUS_ENUM, VISA_STATUS_ENUM

Base = declarative_base()

class VisaRequest(Base):
    __tablename__ = "visa_request"

    visa_request_id = Column(Integer, primary_key=True, autoincrement=True)
    visa_request_code = Column(String(50), nullable=False, unique=True)

    visa_process_id = Column(Integer, nullable=False)
    visa_type = Column(String(50), nullable=False)
    country_id = Column(Integer, nullable=False)
    country_name = Column(String(100), nullable=False)

    initiator_name = Column(String(100), nullable=False)
    initiator_email = Column(String(100), nullable=False)
    initiator_phone = Column(String(20), nullable=False)
    initiator_address = Column(String, nullable=False)
    user_id = Column(Integer,  nullable=True)
    vendor_id = Column(Integer, nullable=True)
 
    total_applicants = Column(Integer, nullable=False)
    application_fee = Column(Integer, nullable=False)
    visa_fee = Column(Integer, nullable=False)
    service_fee = Column(Integer, nullable=False)
    total_fee = Column(Integer, nullable=False)
    total_fee_currency = Column(String(10), nullable=False)
    amount_paid = Column(Integer, nullable=False)
    amount_due = Column(Integer, nullable=False)
    payment_status = Column(PAYMENT_STATUS_ENUM, default="PENDING")
    payment_date = Column(DateTime, nullable=True)
    payment_reference = Column(String(100), nullable=True)

    coupon_code = Column(String(50), nullable=True)
    coupon_discount = Column(Integer, nullable=True)
    coupon_id = Column(Integer, nullable=True)
    coupon_type = Column(COUPON_TYPE_ENUM, nullable=True)

    visa_status = Column(VISA_STATUS_ENUM, default="PENDING")

    created_date = Column(DateTime, server_default=func.now())
    modified_date = Column(DateTime, onupdate=func.now())
    active_status = Column(Boolean, default=True)
    visa_request_notes = Column(String, nullable=True)

    # Relationship with Applications
    applications = relationship('Applications', backref="visa_request")