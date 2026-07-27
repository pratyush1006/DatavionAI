"""
Telemedicine permissions module.
"""

from __future__ import annotations

from apps.telemedicine.permissions.telemedicine import (
    CanCreateTelemedicineSession,
    CanDeleteTelemedicineSession,
    CanEndTelemedicineSession,
    CanRecordTelemedicineSession,
    CanStartTelemedicineSession,
    CanUpdateTelemedicineSession,
    CanViewTelemedicineSession,
    TelemedicinePermission,
)

__all__ = [
    "CanCreateTelemedicineSession",
    "CanDeleteTelemedicineSession",
    "CanEndTelemedicineSession",
    "CanRecordTelemedicineSession",
    "CanStartTelemedicineSession",
    "CanUpdateTelemedicineSession",
    "CanViewTelemedicineSession",
    "TelemedicinePermission",
]
