"""
Patient Identifier API serializer exports.
"""

from __future__ import annotations

from apps.patient_management.identifiers.api.serializers.create import (
    PatientIdentifierCreateSerializer,
)
from apps.patient_management.identifiers.api.serializers.detail import (
    PatientIdentifierDetailSerializer,
)
from apps.patient_management.identifiers.api.serializers.list import (
    PatientIdentifierListSerializer,
)
from apps.patient_management.identifiers.api.serializers.update import (
    PatientIdentifierUpdateSerializer,
)

__all__ = (
    "PatientIdentifierCreateSerializer",
    "PatientIdentifierDetailSerializer",
    "PatientIdentifierListSerializer",
    "PatientIdentifierUpdateSerializer",
)
