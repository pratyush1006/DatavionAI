"""
Constants for the Emergency Contacts module.
"""

from __future__ import annotations

from django.db import models


class EmergencyContactRelationship(models.TextChoices):
    """
    Relationship between the patient and the emergency contact.
    """

    SPOUSE = "SPOUSE", "Spouse"
    FATHER = "FATHER", "Father"
    MOTHER = "MOTHER", "Mother"
    SON = "SON", "Son"
    DAUGHTER = "DAUGHTER", "Daughter"
    BROTHER = "BROTHER", "Brother"
    SISTER = "SISTER", "Sister"
    GRANDFATHER = "GRANDFATHER", "Grandfather"
    GRANDMOTHER = "GRANDMOTHER", "Grandmother"
    UNCLE = "UNCLE", "Uncle"
    AUNT = "AUNT", "Aunt"
    COUSIN = "COUSIN", "Cousin"
    FRIEND = "FRIEND", "Friend"
    GUARDIAN = "GUARDIAN", "Guardian"
    CAREGIVER = "CAREGIVER", "Caregiver"
    LEGAL_REPRESENTATIVE = (
        "LEGAL_REPRESENTATIVE",
        "Legal Representative",
    )
    EMPLOYER = "EMPLOYER", "Employer"
    NEIGHBOR = "NEIGHBOR", "Neighbor"
    OTHER = "OTHER", "Other"


class EmergencyContactStatus(models.TextChoices):
    """
    Lifecycle status of an emergency contact.
    """

    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    BLOCKED = "BLOCKED", "Blocked"


class PreferredContactMethod(models.TextChoices):
    """
    Preferred communication channel.
    """

    MOBILE = "MOBILE", "Mobile"
    HOME_PHONE = "HOME_PHONE", "Home Phone"
    WORK_PHONE = "WORK_PHONE", "Work Phone"
    EMAIL = "EMAIL", "Email"
    SMS = "SMS", "SMS"
    WHATSAPP = "WHATSAPP", "WhatsApp"
    ANY = "ANY", "Any"


class EmergencyContactAvailability(models.TextChoices):
    """
    Availability of the emergency contact.
    """

    ALWAYS = "ALWAYS", "Always Available"
    DAYTIME = "DAYTIME", "Daytime"
    NIGHT = "NIGHT", "Night"
    BUSINESS_HOURS = (
        "BUSINESS_HOURS",
        "Business Hours",
    )
    WEEKENDS = "WEEKENDS", "Weekends"
    ON_CALL = "ON_CALL", "On Call"


class EmergencyContactNumberPrefix:
    """
    Prefix used when generating emergency contact numbers.
    """

    DEFAULT = "EC"


__all__ = [
    "EmergencyContactAvailability",
    "EmergencyContactNumberPrefix",
    "EmergencyContactRelationship",
    "EmergencyContactStatus",
    "PreferredContactMethod",
]
