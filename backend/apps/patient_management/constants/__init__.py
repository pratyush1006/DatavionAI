"""
Shared constants for the Patient Management application.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.constants import (
    PatientGender,
    PatientMaritalStatus,
)


class RelationshipType(models.TextChoices):
    """
    Relationship between a patient and a related person.
    """

    SPOUSE = "spouse", "Spouse"

    PARENT = "parent", "Parent"

    CHILD = "child", "Child"

    SIBLING = "sibling", "Sibling"

    GUARDIAN = "guardian", "Guardian"

    GRANDPARENT = "grandparent", "Grandparent"

    OTHER = "other", "Other"


class ContactMethod(models.TextChoices):
    """
    Preferred communication channel.
    """

    EMAIL = "email", "Email"

    SMS = "sms", "SMS"

    PHONE = "phone", "Phone"

    PORTAL = "portal", "Portal"

    POST = "post", "Post"


class DocumentCategory(models.TextChoices):
    """
    Categories of patient documents.
    """

    ID_PROOF = "id_proof", "ID Proof"

    INSURANCE = "insurance", "Insurance"

    CONSENT_FORM = "consent_form", "Consent Form"

    CLINICAL_NOTE = "clinical_note", "Clinical Note"

    IMAGING = "imaging", "Imaging"

    LAB_REPORT = "lab_report", "Lab Report"

    DISCHARGE_SUMMARY = "discharge_summary", "Discharge Summary"

    OTHER = "other", "Other"


class ReferralStatus(models.TextChoices):
    """
    Referral lifecycle status.
    """

    PENDING = "pending", "Pending"

    ACCEPTED = "accepted", "Accepted"

    DECLINED = "declined", "Declined"

    COMPLETED = "completed", "Completed"

    CANCELLED = "cancelled", "Cancelled"


class ReferralPriority(models.TextChoices):
    """
    Referral priority levels.
    """

    ROUTINE = "routine", "Routine"

    URGENT = "urgent", "Urgent"

    STAT = "stat", "STAT"


__all__ = [
    "ContactMethod",
    "DocumentCategory",
    "PatientGender",
    "PatientMaritalStatus",
    "ReferralPriority",
    "ReferralStatus",
    "RelationshipType",
]
