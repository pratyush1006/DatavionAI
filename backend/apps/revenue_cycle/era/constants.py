"""Lifecycle and source constants for electronic remittance advice."""

from __future__ import annotations

from django.db import models


class ERAStatus(models.TextChoices):
    """Lifecycle states for an ERA record."""

    RECEIVED = "received", "Received"
    VALIDATED = "validated", "Validated"
    POSTING = "posting", "Posting"
    POSTED = "posted", "Posted"
    FAILED = "failed", "Failed"
    REVERSED = "reversed", "Reversed"


class ERASource(models.TextChoices):
    """Sources from which remittance advice may arrive."""

    EDI_835 = "edi_835", "EDI 835"
    PORTAL = "portal", "Payer Portal"
    MANUAL = "manual", "Manual"
    API = "api", "API"


__all__ = ("ERASource", "ERAStatus")
