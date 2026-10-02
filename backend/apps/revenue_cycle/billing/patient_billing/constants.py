"""Patient Billing lifecycle and domain constants."""

from __future__ import annotations

from django.db import models


class PatientBillingAccountStatus(models.TextChoices):
    """Patient billing account lifecycle states."""

    ACTIVE = "ACTIVE", "Active"
    SUSPENDED = "SUSPENDED", "Suspended"
    CLOSED = "CLOSED", "Closed"


class BillingPartyType(models.TextChoices):
    """Financial responsibility party types."""

    SELF = "SELF", "Patient"
    GUARANTOR = "GUARANTOR", "Guarantor"
    INSURANCE = "INSURANCE", "Insurance"


class PatientStatementStatus(models.TextChoices):
    """Patient statement lifecycle states."""

    DRAFT = "DRAFT", "Draft"
    ISSUED = "ISSUED", "Issued"
    PAID = "PAID", "Paid"
    VOID = "VOID", "Void"


__all__ = (
    "BillingPartyType",
    "PatientBillingAccountStatus",
    "PatientStatementStatus",
)
