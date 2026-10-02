from django.db import models


class EncounterStatus(models.TextChoices):
    SCHEDULED = "scheduled", "Scheduled"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


ENCOUNTER_TRANSITIONS = {
    EncounterStatus.SCHEDULED: frozenset(
        {EncounterStatus.IN_PROGRESS, EncounterStatus.CANCELLED}
    ),
    EncounterStatus.IN_PROGRESS: frozenset(
        {EncounterStatus.COMPLETED, EncounterStatus.CANCELLED}
    ),
    EncounterStatus.COMPLETED: frozenset(),
    EncounterStatus.CANCELLED: frozenset(),
}


def is_valid_encounter_transition(current_status: str, target_status: str) -> bool:
    if current_status == target_status:
        return True
    return target_status in ENCOUNTER_TRANSITIONS.get(current_status, frozenset())
