"""
Constants for the Patient Consents module.
"""

from __future__ import annotations

from django.db.models import TextChoices

__all__ = [
    "ConsentMethod",
    "ConsentSource",
    "ConsentStatus",
    "ConsentType",
]


class ConsentType(TextChoices):
    """
    Supported consent types.
    """

    TREATMENT = "TREATMENT", "Treatment"
    SURGERY = "SURGERY", "Surgery"
    TELEMEDICINE = "TELEMEDICINE", "Telemedicine"
    LABORATORY = "LABORATORY", "Laboratory"
    RADIOLOGY = "RADIOLOGY", "Radiology"
    BLOOD_TRANSFUSION = "BLOOD_TRANSFUSION", "Blood Transfusion"
    RESEARCH = "RESEARCH", "Research"
    PRIVACY = "PRIVACY", "Privacy"
    DATA_SHARING = "DATA_SHARING", "Data Sharing"
    INSURANCE = "INSURANCE", "Insurance"
    VACCINATION = "VACCINATION", "Vaccination"
    ORGAN_DONATION = "ORGAN_DONATION", "Organ Donation"
    CLINICAL_TRIAL = "CLINICAL_TRIAL", "Clinical Trial"
    CUSTOM = "CUSTOM", "Custom"


class ConsentStatus(TextChoices):
    """
    Consent lifecycle status.
    """

    DRAFT = "DRAFT", "Draft"
    PENDING = "PENDING", "Pending"
    REQUESTED = "REQUESTED", "Requested"
    GRANTED = "GRANTED", "Granted"
    REJECTED = "REJECTED", "Rejected"
    REVOKED = "REVOKED", "Revoked"
    WITHDRAWN = "WITHDRAWN", "Withdrawn"
    EXPIRED = "EXPIRED", "Expired"
    ARCHIVED = "ARCHIVED", "Archived"


class ConsentMethod(TextChoices):
    """
    Consent acquisition method.
    """

    PAPER = "PAPER", "Paper Signature"
    DIGITAL = "DIGITAL", "Digital Signature"
    OTP = "OTP", "OTP"
    BIOMETRIC = "BIOMETRIC", "Biometric"
    VOICE = "VOICE", "Voice"
    GUARDIAN = "GUARDIAN", "Guardian Approval"
    API = "API", "API"


class ConsentSource(TextChoices):
    """
    Source where consent originated.
    """

    RECEPTION = "RECEPTION", "Reception"
    PATIENT_PORTAL = "PATIENT_PORTAL", "Patient Portal"
    DOCTOR = "DOCTOR", "Doctor"
    NURSE = "NURSE", "Nurse"
    MOBILE_APP = "MOBILE_APP", "Mobile App"
    TELEMEDICINE = "TELEMEDICINE", "Telemedicine"
    API = "API", "API"
    IMPORT = "IMPORT", "Imported"
