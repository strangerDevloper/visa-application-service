from sqlalchemy import Enum

# Gender Enum
GENDER_ENUM = Enum("MALE", "FEMALE", "OTHER", name="gender_enum")

# Visa Status Enum
VISA_STATUS_ENUM = Enum("DRAFT","PENDING", "APPROVED", "REJECTED", "PROCESSING", name="visa_status_enum")

# Application Status Enum
APPLICATION_STATUS_ENUM = Enum("DRAFT","PENDING", "APPROVED", "REJECTED", "PROCESSING", name="application_status_enum")

# Coupon Type Enum
COUPON_TYPE_ENUM = Enum("FLAT", "PERCENTAGE", name="coupon_type_enum")

# Payment Status Enum
PAYMENT_STATUS_ENUM = Enum("PENDING", "PARTIAL", "PAID", "REFUNDED", name="payment_status_enum")

# Field Type Enum
FIELD_TYPE_ENUM = Enum("TEXT", "NUMBER", "DATE", "DOCUMENT", name="field_type_enum")

# Document Type Enum
DOCUMENT_TYPE_ENUM = Enum("PASSPORT", "PHOTO", "VISA_FORM", "OTHER", name="document_type_enum")

# Verification Status Enum
VERIFICATION_STATUS_ENUM = Enum("PENDING", "VERIFIED", "REJECTED", name="verification_status_enum")

# Remark Type Enum
REMARK_TYPE_ENUM = Enum("GENERAL", "VERIFICATION", "ESCALATION", name="remark_type_enum")

# Is Internal Enum
IS_INTERNAL_ENUM = Enum("YES", "NO", name="is_internal_enum")

# Assignment Status Enum
ASSIGNMENT_STATUS_ENUM = Enum("ASSIGNED", "REASSIGNED", "UNASSIGNED", name="assignment_status_enum")