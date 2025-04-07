# app/core/constants.py
from enum import Enum


USER_TYPE_EMPLOYEE = "employee"
USER_TYPE_USER = "user"
USER_TYPE_VENDOR = "vendor"

class UserType(str, Enum):
    EMPLOYEE = USER_TYPE_EMPLOYEE
    USER = USER_TYPE_USER
    VENDOR = USER_TYPE_VENDOR
