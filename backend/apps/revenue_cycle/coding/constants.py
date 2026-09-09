from __future__ import annotations

"""Coding domain constants and lifecycle definitions."""

from django.db import models


class CodingStatus(models.TextChoices):
    """Lifecycle states for coding records."""

    DRAFT = "draft", "Draft"
    ASSIGNED = "assigned", "Assigned"
    IN_REVIEW = "in_review", "In Review"
    CODED = "coded", "Coded"
    VALIDATED = "validated", "Validated"
    REJECTED = "rejected", "Rejected"
    RELEASED = "released", "Released"
    VOIDED = "voided", "Voided"


class CodingType(models.TextChoices):
    """Coding classifications supported by the bounded context."""

    PROFESSIONAL = "professional", "Professional"
    FACILITY = "facility", "Facility"
    OUTPATIENT = "outpatient", "Outpatient"
    INPATIENT = "inpatient", "Inpatient"
    OTHER = "other", "Other"


class CodeSystem(models.TextChoices):
    """Supported clinical and billing code systems."""

    ICD10CM = "icd10cm", "ICD-10-CM"
    ICD10PCS = "icd10pcs", "ICD-10-PCS"
    CPT = "cpt", "CPT"
    HCPCS = "hcpcs", "HCPCS"
    MODIFIER = "modifier", "Modifier"
    OTHER = "other", "Other"


DEFAULT_STATUS = CodingStatus.DRAFT

ALLOWED_TRANSITIONS = {
    CodingStatus.DRAFT: {CodingStatus.ASSIGNED, CodingStatus.VOIDED},
    CodingStatus.ASSIGNED: {
        CodingStatus.IN_REVIEW,
        CodingStatus.REJECTED,
        CodingStatus.VOIDED,
    },
    CodingStatus.IN_REVIEW: {
        CodingStatus.CODED,
        CodingStatus.REJECTED,
        CodingStatus.VOIDED,
    },
    CodingStatus.CODED: {
        CodingStatus.VALIDATED,
        CodingStatus.IN_REVIEW,
        CodingStatus.REJECTED,
    },
    CodingStatus.VALIDATED: {
        CodingStatus.RELEASED,
        CodingStatus.IN_REVIEW,
        CodingStatus.VOIDED,
    },
    CodingStatus.REJECTED: {
        CodingStatus.ASSIGNED,
        CodingStatus.VOIDED,
    },
    CodingStatus.RELEASED: {CodingStatus.VOIDED},
    CodingStatus.VOIDED: set(),
}

__all__ = (
    "ALLOWED_TRANSITIONS",
    "CodeSystem",
    "CodingStatus",
    "CodingType",
    "DEFAULT_STATUS",
)
