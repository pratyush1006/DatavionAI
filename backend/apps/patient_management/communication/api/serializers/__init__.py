"""Patient Communication serializer exports."""

from __future__ import annotations

from apps.patient_management.communication.api.serializers.create import (
    CommunicationCreateSerializer,
)
from apps.patient_management.communication.api.serializers.detail import (
    CommunicationDetailSerializer,
)
from apps.patient_management.communication.api.serializers.list import (
    CommunicationListSerializer,
)
from apps.patient_management.communication.api.serializers.update import (
    CommunicationUpdateSerializer,
)

__all__ = (
    "CommunicationCreateSerializer",
    "CommunicationDetailSerializer",
    "CommunicationListSerializer",
    "CommunicationUpdateSerializer",
)
