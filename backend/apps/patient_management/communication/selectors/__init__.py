"""Patient Communication selector exports."""

from __future__ import annotations

from apps.patient_management.communication.selectors.communication import (
    get_communication,
    list_communications,
)

__all__ = ("get_communication", "list_communications")
