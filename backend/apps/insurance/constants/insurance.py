"""
Insurance constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class InsuranceType(models.TextChoices):
    """
    Supported insurance plan types.
    """

    GOVERNMENT = "government", "Government"
    PRIVATE = "private", "Private"
    EMPLOYER = "employer", "Employer"
    SELF_PAY = "self_pay", "Self Pay"
    CHARITY = "charity", "Charity"


class AuthorizationServiceType(models.TextChoices):
    """
    Supported prior authorization service types.
    """

    INPATIENT = "inpatient", "Inpatient"
    OUTPATIENT = "outpatient", "Outpatient"
    EMERGENCY = "emergency", "Emergency"
    PHARMACY = "pharmacy", "Pharmacy"
    LABORATORY = "laboratory", "Laboratory"
    IMAGING = "imaging", "Imaging"
    THERAPY = "therapy", "Therapy"


class AuthorizationStatus(models.TextChoices):
    """
    Prior authorization lifecycle status.
    """

    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    DENIED = "denied", "Denied"
    EXPIRED = "expired", "Expired"
    CANCELLED = "cancelled", "Cancelled"


class ClaimStatus(models.TextChoices):
    """
    Claim lifecycle status.
    """

    DRAFT = "draft", "Draft"
    SUBMITTED = "submitted", "Submitted"
    PROCESSING = "processing", "Processing"
    APPROVED = "approved", "Approved"
    DENIED = "denied", "Denied"
    PARTIALLY_PAID = "partially_paid", "Partially Paid"
    PAID = "paid", "Paid"
    APPEALED = "appealed", "Appealed"


DEFAULT_INSURANCE_TYPE: Final[str] = InsuranceType.PRIVATE

DEFAULT_AUTHORIZATION_STATUS: Final[str] = AuthorizationStatus.PENDING

DEFAULT_CLAIM_STATUS: Final[str] = ClaimStatus.DRAFT


__all__ = [
    "AuthorizationServiceType",
    "AuthorizationStatus",
    "ClaimStatus",
    "DEFAULT_AUTHORIZATION_STATUS",
    "DEFAULT_CLAIM_STATUS",
    "DEFAULT_INSURANCE_TYPE",
    "InsuranceType",
]
