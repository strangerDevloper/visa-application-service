# schemas.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

from app.models.application_remarks import ApplicationRemarks


class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class VisaStatusEnum(str, Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PROCESSING = "PROCESSING"


class ApplicationStatusEnum(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"
    PROCESSING = "PROCESSING"
    DRAFT = "DRAFT"


class PaymentStatusEnum(str, Enum):
    PENDING = "PENDING"
    PARTIAL = "PARTIAL"
    PAID = "PAID"
    REFUNDED = "REFUNDED"

class CouponTypeEnum(str, Enum):
    FLAT = "FLAT"
    PERCENTAGE = "PERCENTAGE"

class FieldTypeEnum(str, Enum):
    TEXT = "TEXT"
    NUMBER = "NUMBER"
    DATE = "DATE"
    DOCUMENT = "DOCUMENT"

class DocumentTypeEnum(str, Enum):
    PASSPORT = "PASSPORT"
    PHOTO = "PHOTO"
    VISA_FORM = "VISA_FORM"
    OTHER = "OTHER"

class VerificationStatusEnum(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"

class RemarkTypeEnum(str, Enum):
    GENERAL = "GENERAL"
    VERIFICATION = "VERIFICATION"
    ESCALATION = "ESCALATION"

class IsInternalEnum(str, Enum):
    YES = "YES"
    NO = "NO"

class AssignmentStatusEnum(str, Enum):
    ASSIGNED = "ASSIGNED"
    REASSIGNED = "REASSIGNED"
    UNASSIGNED = "UNASSIGNED"

# Base schemas
class VisaRequestBase(BaseModel):
    visa_request_code: str
    visa_process_id: int
    visa_type: str
    country_id: int
    country_name: str
    initiator_name: str
    initiator_email: str
    initiator_phone: str
    initiator_address: str
    user_id: Optional[int] = None
    vendor_id: Optional[int] = None
    total_applicants: int
    application_fee: int
    visa_fee: int
    service_fee: int
    total_fee: int
    total_fee_currency: str
    amount_paid: int
    amount_due: int
    payment_status: PaymentStatusEnum = PaymentStatusEnum.PENDING
    coupon_code: Optional[str] = None
    coupon_discount: Optional[int] = None
    coupon_id: Optional[int] = None
    coupon_type: Optional[CouponTypeEnum] = None
    visa_request_notes: Optional[str] = None

class ApplicationBase(BaseModel):
    visa_request_id: int
    applicant_first_name: str
    applicant_middle_name: Optional[str] = None
    applicant_last_name: Optional[str] = None
    applicant_email: str
    applicant_phone: str
    applicant_passport_number: str
    applicant_dob: datetime
    applicant_gender: GenderEnum
    assigned_to: Optional[int] = None
    expected_completion_date: Optional[datetime] = None
    application_notes: Optional[str] = None
    is_priority: bool = False
    is_escalated: bool = False

class ApplicationDetailBase(BaseModel):
    application_id: int
    document_code: str
    field_name: str
    field_value: str
    field_title: str
    field_description: Optional[str] = None
    field_type: FieldTypeEnum
    document_type: DocumentTypeEnum
    remark: Optional[str] = None

class ApplicationRemarkBase(BaseModel):
    application_id: int
    remark_type: RemarkTypeEnum
    remark_text: str
    user_id: int
    vendor_id: int
    employee_id: Optional[int] = None
    name: Optional[str] = None
    is_internal: IsInternalEnum = IsInternalEnum.NO

class AssignmentHistoryBase(BaseModel):
    application_id: int
    assigned_by: int
    assigned_by_name: str
    assigned_to_name: str
    assigned_to_user_id: int
    assigned_to_vendor_id: int
    assigned_to_employee_id: Optional[int] = None
    remarks: Optional[str] = None
    assignment_status: Optional[AssignmentStatusEnum] = None

# Create schemas
class VisaRequestCreate(BaseModel):
    """
    Schema for creating a Visa Request.
    The following fields will be populated programmatically:
    - initiator_name
    - initiator_email
    - initiator_phone
    - initiator_address
    - user_id
    - vendor_id
    """
    visa_process_id: int
    visa_type: str
    country_id: int
    country_name: str
    total_applicants: int
    application_fee: int
    visa_fee: int
    service_fee: int
    total_fee: int
    total_fee_currency: str
    amount_paid: int
    amount_due: int
    payment_status: PaymentStatusEnum = PaymentStatusEnum.PENDING
    coupon_code: Optional[str] = None
    coupon_discount: Optional[int] = None
    coupon_id: Optional[int] = None
    coupon_type: Optional[CouponTypeEnum] = None
    visa_request_notes: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationDetailCreate(BaseModel):
    document_code: str
    field_name: str
    field_value: str
    field_title: str
    field_description: Optional[str] = None
    field_type: FieldTypeEnum
    document_type: DocumentTypeEnum

# Add to your existing schemas

class ApplicationDetailUpdate(BaseModel):
    field_value: Optional[str] = None
    verification_status: Optional[VerificationStatusEnum] = None
    remark: Optional[str] = None
    verified_by: Optional[int] = None  # Will be set from auth token
    verified_by_name: Optional[str] = None  # Will be set from auth token

class ApplicationUpdate(BaseModel):
    applicant_first_name: Optional[str] = None
    applicant_middle_name: Optional[str] = None
    applicant_last_name: Optional[str] = None
    applicant_email: Optional[str] = None
    applicant_phone: Optional[str] = None
    applicant_passport_number: Optional[str] = None
    applicant_dob: Optional[datetime] = None
    applicant_gender: Optional[GenderEnum] = None
    expected_completion_date: Optional[datetime] = None
    application_notes: Optional[str] = None
    is_priority: Optional[bool] = None
    is_escalated: Optional[bool] = None

class ApplicationRemarkCreate(BaseModel):
    remark_type: RemarkTypeEnum
    remark_text: str
    user_id: int
    vendor_id: int
    employee_id: Optional[int] = None
    name: Optional[str] = None
    is_internal: IsInternalEnum = IsInternalEnum.NO


class AssignmentHistoryCreate(AssignmentHistoryBase):
    pass


class ApplicationCreatePayload(BaseModel):
    visa_request_id: int
    applicant_first_name: str
    applicant_middle_name: Optional[str] = None
    applicant_last_name: Optional[str] = None
    applicant_email: str
    applicant_phone: str
    applicant_passport_number: str
    applicant_dob: datetime
    applicant_gender: GenderEnum
    expected_completion_date: Optional[datetime] = None
    application_notes: Optional[str] = None
    is_priority: bool = False
    is_escalated: bool = False
    details: List[ApplicationDetailCreate]
    remarks: Optional[List[ApplicationRemarkCreate]] = None


class ApplicationRemarkCreateRequest(BaseModel):
    remark_type: RemarkTypeEnum
    remark_text: str
    is_internal: IsInternalEnum = IsInternalEnum.NO

# Add to your existing schemas.py
class VisaRequestFilter(BaseModel):
    user_id: Optional[int] = None
    vendor_id: Optional[int] = None
    counter_id: Optional[int] = None
    visa_process_id: Optional[int] = None
    initiator_name: Optional[str] = None
    visa_request_code: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    payment_status: Optional[PaymentStatusEnum] = None
    visa_status: Optional[VisaStatusEnum] = None

class ApplicationFilter(BaseModel):
    visa_request_code: Optional[str] = None
    application_code: Optional[str] = None
    assigned_to: Optional[int] = None
    country_id: Optional[int] = None
    applicant_name: Optional[str] = None
    visa_process_id: Optional[int] = None
    status: Optional[ApplicationStatusEnum] = None
    is_priority: Optional[bool] = None
    is_escalated: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class RemarkFilter(BaseModel):
    remark_type: Optional[RemarkTypeEnum] = None
    is_internal: Optional[IsInternalEnum] = None
    user_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class MediaUploadResponse(BaseModel):
    file_url: str
    preview_url: str  # Presigned URL
    s3_key: str

class BulkMediaUploadResponse(BaseModel):
    uploaded_files: List[MediaUploadResponse]
    visa_request_code: str
    application_code: str
    
# Response schemas
class VisaRequest(VisaRequestBase):
    visa_request_id: int
    created_date: datetime
    modified_date: Optional[datetime] = None
    active_status: bool = True

    class Config:
        from_attributes = True

class Application(ApplicationBase):
    application_id: int
    application_code: str
    visa_status: VisaStatusEnum = VisaStatusEnum.PENDING
    submission_date: datetime
    modified_date: Optional[datetime] = None
    active_status: bool = True
    assigned_to_name: Optional[str] = None

    class Config:
        from_attributes = True

class ApplicationDetail(ApplicationDetailBase):
    application_detail_id: int
    uploaded_date: datetime
    verification_status: VerificationStatusEnum = VerificationStatusEnum.PENDING
    verified_by: Optional[int] = None
    verified_by_name: Optional[str] = None
    verified_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class ApplicationRemark(ApplicationRemarkBase):
    remark_id: int
    created_date: datetime

    class Config:
        from_attributes = True

class AssignmentHistory(AssignmentHistoryBase):
    assignment_id: int
    assigned_date: datetime

    class Config:
        from_attributes = True

# Full response schemas with relationships
class VisaRequestWithApplications(VisaRequest):
    applications: List[Application] = []

class PaginatedResponse(BaseModel):
    items: List[VisaRequestWithApplications]
    total: int
    page: int
    per_page: int

class ApplicationWithDetails(Application):
    application_details: List[ApplicationDetail] = []
    application_remarks: List[ApplicationRemark] = []
    assignment_history: List[AssignmentHistory] = []

# Add these to your existing schemas

class AssignmentCreate(BaseModel):
    assigned_to: int
    assigned_to_name: str
    remarks: Optional[str] = None

class VisaRequestSubmit(BaseModel):
    assigned_to: int  # Internal employee ID
    assigned_to_name: str  # Internal employee name