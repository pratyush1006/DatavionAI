"""
Encounter constants.
"""

from django.db import models


class EncounterStatus(models.TextChoices):
    """
    Encounter lifecycle status.
    """

    SCHEDULED = (
        "scheduled",
        "Scheduled",
    )

    IN_PROGRESS = (
        "in_progress",
        "In Progress",
    )

    COMPLETED = (
        "completed",
        "Completed",
    )

    CANCELLED = (
        "cancelled",
        "Cancelled",
    )


DEFAULT_ENCOUNTER_STATUS = (
    EncounterStatus.SCHEDULED
)


__all__ = [
    "EncounterStatus",
    "DEFAULT_ENCOUNTER_STATUS",
]
