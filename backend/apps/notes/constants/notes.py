"""
Clinical Notes-specific constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class NoteType(models.TextChoices):
    """
    Supported clinical note types.
    """

    SOAP = "soap", "SOAP Note"
    PROGRESS_NOTE = "progress_note", "Progress Note"
    DISCHARGE_SUMMARY = "discharge_summary", "Discharge Summary"
    CONSULTATION = "consultation", "Consultation Note"
    PROCEDURE_NOTE = "procedure_note", "Procedure Note"
    OPERATIVE_NOTE = "operative_note", "Operative Note"
    DELIVERY_NOTE = "delivery_note", "Delivery Note"
    EMERGENCY_NOTE = "emergency_note", "Emergency Note"
    OTHER = "other", "Other"


class TemplateType(models.TextChoices):
    """
    Supported note template types.
    """

    SOAP = "soap", "SOAP"
    PROGRESS_NOTE = "progress_note", "Progress Note"
    DISCHARGE_SUMMARY = "discharge_summary", "Discharge Summary"
    CONSULTATION = "consultation", "Consultation"
    PROCEDURE_NOTE = "procedure_note", "Procedure Note"
    OPERATIVE_NOTE = "operative_note", "Operative Note"
    DELIVERY_NOTE = "delivery_note", "Delivery Note"
    EMERGENCY_NOTE = "emergency_note", "Emergency Note"
    OTHER = "other", "Other"


DEFAULT_NOTE_TYPE: Final[str] = NoteType.SOAP


__all__ = [
    "DEFAULT_NOTE_TYPE",
    "NoteType",
    "TemplateType",
]
