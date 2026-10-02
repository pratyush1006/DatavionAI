"""Constants for Revenue Cycle claim submission."""

from __future__ import annotations

from django.db import models


class SubmissionStatus(models.TextChoices):
    """Lifecycle states for a claim submission."""

    PENDING = "pending", "Pending"
    VALIDATED = "validated", "Validated"
    SUBMITTING = "submitting", "Submitting"
    SUBMITTED = "submitted", "Submitted"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"


class SubmissionMethod(models.TextChoices):
    """Supported claim submission channels."""

    EDI = "edi", "EDI"
    API = "api", "API"
    PORTAL = "portal", "Portal"
    MANUAL = "manual", "Manual"


__all__ = ("SubmissionStatus", "SubmissionMethod")
