"""
Organization type enumeration.
"""

from __future__ import annotations

from enum import StrEnum


class OrganizationType(
    StrEnum,
):
    """
    Supported organization types.
    """

    HOSPITAL = "hospital"

    CLINIC = "clinic"

    LABORATORY = "laboratory"

    PHARMACY = "pharmacy"

    IMAGING_CENTER = "imaging_center"

    DIAGNOSTIC_CENTER = "diagnostic_center"

    TELEMEDICINE = "telemedicine"

    REHABILITATION_CENTER = "rehabilitation_center"

    BLOOD_BANK = "blood_bank"

    HEALTHCARE_NETWORK = "healthcare_network"
