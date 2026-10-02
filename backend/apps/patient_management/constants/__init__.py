"""
Shared constants for the Patient Management application.

This module exposes shared Patient Management constants while keeping
Patient-specific constants owned by the canonical Patients module.
"""

from __future__ import annotations

from django.db import models

from apps.patient_management.patients.constants import (
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
    Preferred communication channel for patient communication.
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

# Consolidated definitions from the former constants.py.
"""Application-level constants for DatavionOS Patient Management."""

PATIENT_MANAGEMENT_APP_LABEL = "patient_management"
PATIENT_MANAGEMENT_IDENTIFIER = "patient-management"
PATIENT_MANAGEMENT_DISPLAY_NAME = "Patient Management"

PATIENT_MANAGEMENT_SUBMODULES = (
    "registration",
    "patients",
    "profile",
    "mpi",
    "addresses",
    "contacts",
    "emergency",
    "emergency_contacts",
    "communication",
    "consents",
    "medical_history",
    "relationships",
    "family_members",
    "referrals",
    "patient_documents",
    "portal",
    "preferences",
    "timeline",
)

PROTECTED_SUBMODULES = ("family_members",)
