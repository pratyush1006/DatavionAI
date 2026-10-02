"""Patient emergency API serializers."""

from apps.patient_management.emergency.api.serializers.create import (
    EmergencyCreateSerializer,
)
from apps.patient_management.emergency.api.serializers.detail import (
    EmergencyDetailSerializer,
)
from apps.patient_management.emergency.api.serializers.list import (
    EmergencyListSerializer,
)
from apps.patient_management.emergency.api.serializers.update import (
    EmergencyUpdateSerializer,
)

__all__ = (
    "EmergencyCreateSerializer",
    "EmergencyDetailSerializer",
    "EmergencyListSerializer",
    "EmergencyUpdateSerializer",
)
