"""Validation helpers for Patient Communication."""

from __future__ import annotations

from typing import Any

from apps.patient_management.communication.constants import (
    CommunicationChannel,
    CommunicationDirection,
)
from apps.patient_management.communication.exceptions import (
    PatientCommunicationValidationError,
)


def validate_communication_data(data: dict[str, Any]) -> None:
    """Validate cross-field communication invariants."""
    channel = data.get("channel")
    direction = data.get("direction")
    content = data.get("content")
    if channel == CommunicationChannel.PHONE and not content:
        raise PatientCommunicationValidationError(
            "Phone communications require a note or summary."
        )
    if direction == CommunicationDirection.INBOUND and data.get("status") == "queued":
        raise PatientCommunicationValidationError(
            "Inbound communications cannot be queued for delivery."
        )


__all__ = ("validate_communication_data",)
