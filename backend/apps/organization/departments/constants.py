"""
Constants for the Departments module.
"""

from __future__ import annotations

from typing import Final

from django.db.models import TextChoices


class DepartmentType(TextChoices):
    """
    Types of organizational departments.
    """

    GENERAL = "GENERAL", "General"

    CLINICAL = "CLINICAL", "Clinical"

    ADMINISTRATION = "ADMINISTRATION", "Administration"

    EMERGENCY = "EMERGENCY", "Emergency"

    OUTPATIENT = "OUTPATIENT", "Outpatient"

    INPATIENT = "INPATIENT", "Inpatient"

    ICU = "ICU", "Intensive Care Unit"

    OPERATION_THEATRE = (
        "OPERATION_THEATRE",
        "Operation Theatre",
    )

    LABORATORY = "LABORATORY", "Laboratory"

    RADIOLOGY = "RADIOLOGY", "Radiology"

    PHARMACY = "PHARMACY", "Pharmacy"

    BLOOD_BANK = "BLOOD_BANK", "Blood Bank"

    REHABILITATION = (
        "REHABILITATION",
        "Rehabilitation",
    )

    BILLING = "BILLING", "Billing"

    FINANCE = "FINANCE", "Finance"

    HUMAN_RESOURCES = (
        "HUMAN_RESOURCES",
        "Human Resources",
    )

    INFORMATION_TECHNOLOGY = (
        "INFORMATION_TECHNOLOGY",
        "Information Technology",
    )

    MEDICAL_RECORDS = (
        "MEDICAL_RECORDS",
        "Medical Records",
    )

    HOUSEKEEPING = (
        "HOUSEKEEPING",
        "Housekeeping",
    )

    SECURITY = "SECURITY", "Security"

    PROCUREMENT = "PROCUREMENT", "Procurement"

    BIOMEDICAL = "BIOMEDICAL", "Biomedical"

    NURSING = "NURSING", "Nursing"

    TELEMEDICINE = "TELEMEDICINE", "Telemedicine"

    RESEARCH = "RESEARCH", "Research"

    QUALITY = "QUALITY", "Quality"

    OTHER = "OTHER", "Other"


class DepartmentStatus(TextChoices):
    """
    Department lifecycle status.
    """

    ACTIVE = "ACTIVE", "Active"

    INACTIVE = "INACTIVE", "Inactive"

    UNDER_MAINTENANCE = (
        "UNDER_MAINTENANCE",
        "Under Maintenance",
    )

    CLOSED = "CLOSED", "Closed"


DEFAULT_DEPARTMENT_STATUS: Final = DepartmentStatus.ACTIVE

DEFAULT_DEPARTMENT_TYPE: Final = DepartmentType.GENERAL


__all__ = (
    "DEFAULT_DEPARTMENT_STATUS",
    "DEFAULT_DEPARTMENT_TYPE",
    "DepartmentStatus",
    "DepartmentType",
)
