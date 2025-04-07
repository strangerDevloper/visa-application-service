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
from app.config.database import Base
from app.models.enums import REMARK_TYPE_ENUM, IS_INTERNAL_ENUM


class ApplicationRemarks(Base):
    __tablename__ = "application_remarks"

    remark_id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey('applications.application_id'), nullable=False)
    remark_type = Column(REMARK_TYPE_ENUM, nullable=False)
    remark_text = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    vendor_id = Column(Integer, nullable=False)
    employee_id = Column(Integer, nullable=True)
    name = Column(String(100), nullable=True)
    created_date = Column(DateTime, server_default=func.now())
    is_internal = Column(IS_INTERNAL_ENUM, default="NO")

    application = relationship('Applications', backref="application_remarks")
