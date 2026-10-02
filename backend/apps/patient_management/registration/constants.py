"""
Constants for the Patient Registration module.
"""

from __future__ import annotations

from django.db import models


class RegistrationType(models.TextChoices):
    """
    Registration type choices.
    """

    NEW_PATIENT = (
        "NEW_PATIENT",
        "New Patient",
    )
    EXISTING_PATIENT = (
        "EXISTING_PATIENT",
        "Existing Patient",
    )
    FOLLOW_UP = (
        "FOLLOW_UP",
        "Follow-up",
    )
    WALK_IN = (
        "WALK_IN",
        "Walk-in",
    )
    ONLINE = (
        "ONLINE",
        "Online",
    )
    REFERRAL = (
        "REFERRAL",
        "Referral",
    )
    EMERGENCY = (
        "EMERGENCY",
        "Emergency",
    )
    CORPORATE = (
        "CORPORATE",
        "Corporate",
    )
    INSURANCE = (
        "INSURANCE",
        "Insurance",
    )


class RegistrationStatus(models.TextChoices):
    """
    Registration lifecycle status.
    """

    DRAFT = (
        "DRAFT",
        "Draft",
    )
    PENDING_VERIFICATION = (
        "PENDING_VERIFICATION",
        "Pending Verification",
    )
    VERIFIED = (
        "VERIFIED",
        "Verified",
    )
    REGISTERED = (
        "REGISTERED",
        "Registered",
    )
    CHECKED_IN = (
        "CHECKED_IN",
        "Checked In",
    )
    COMPLETED = (
        "COMPLETED",
        "Completed",
    )
    CANCELLED = (
        "CANCELLED",
        "Cancelled",
    )
    REJECTED = (
        "REJECTED",
        "Rejected",
    )
    NO_SHOW = (
        "NO_SHOW",
        "No Show",
    )


class RegistrationSource(models.TextChoices):
    """
    Registration source.
    """

    FRONT_DESK = (
        "FRONT_DESK",
        "Front Desk",
    )
    PATIENT_PORTAL = (
        "PATIENT_PORTAL",
        "Patient Portal",
    )
    MOBILE_APP = (
        "MOBILE_APP",
        "Mobile App",
    )
    KIOSK = (
        "KIOSK",
        "Kiosk",
    )
    API = (
        "API",
        "API",
    )
    IMPORT = (
        "IMPORT",
        "Import",
    )
    CALL_CENTER = (
        "CALL_CENTER",
        "Call Center",
    )


class VisitType(models.TextChoices):
    """
    Visit type.
    """

    OPD = (
        "OPD",
        "Outpatient",
    )
    IPD = (
        "IPD",
        "Inpatient",
    )
    DAY_CARE = (
        "DAY_CARE",
        "Day Care",
    )
    EMERGENCY = (
        "EMERGENCY",
        "Emergency",
    )
    TELEMEDICINE = (
        "TELEMEDICINE",
        "Telemedicine",
    )
    HOME_CARE = (
        "HOME_CARE",
        "Home Care",
    )


class VerificationMethod(models.TextChoices):
    """
    Registration verification method.
    """

    NONE = (
        "NONE",
        "None",
    )
    MOBILE_OTP = (
        "MOBILE_OTP",
        "Mobile OTP",
    )
    EMAIL_OTP = (
        "EMAIL_OTP",
        "Email OTP",
    )
    GOVERNMENT_ID = (
        "GOVERNMENT_ID",
        "Government ID",
    )
    INSURANCE = (
        "INSURANCE",
        "Insurance",
    )
    MANUAL = (
        "MANUAL",
        "Manual",
    )


class RegistrationPriority(models.TextChoices):
    """
    Registration priority.
    """

    LOW = (
        "LOW",
        "Low",
    )
    NORMAL = (
        "NORMAL",
        "Normal",
    )
    HIGH = (
        "HIGH",
        "High",
    )
    URGENT = (
        "URGENT",
        "Urgent",
    )
    CRITICAL = (
        "CRITICAL",
        "Critical",
    )


class CancellationReason(models.TextChoices):
    """
    Registration cancellation reason.
    """

    PATIENT_REQUEST = (
        "PATIENT_REQUEST",
        "Patient Request",
    )
    DUPLICATE_REGISTRATION = (
        "DUPLICATE_REGISTRATION",
        "Duplicate Registration",
    )
    INVALID_INFORMATION = (
        "INVALID_INFORMATION",
        "Invalid Information",
    )
    INSURANCE_DECLINED = (
        "INSURANCE_DECLINED",
        "Insurance Declined",
    )
    PAYMENT_PENDING = (
        "PAYMENT_PENDING",
        "Payment Pending",
    )
    ADMINISTRATIVE = (
        "ADMINISTRATIVE",
        "Administrative",
    )
    OTHER = (
        "OTHER",
        "Other",
    )


class RegistrationNumberPrefix:
    """
    Registration number prefixes.
    """

    DEFAULT = "REG"
