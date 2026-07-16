"""
API views for listing and creating vitals.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.clinical.vitals.api.serializers import (
    VitalCreateSerializer,
    VitalDetailSerializer,
    VitalListSerializer,
)
from apps.clinical.vitals.models import Vital
from apps.clinical.vitals.permissions import (
    CanCreateVital,
    CanViewVital,
)
from apps.clinical.vitals.selectors import get_vitals
from apps.clinical.vitals.services import create_vital
from apps.common.api.base_generics import BaseListCreateAPIView

VITAL_TAG: Final[tuple[str, ...]] = ("Vitals",)


@extend_schema(tags=VITAL_TAG)
class VitalListCreateAPIView(BaseListCreateAPIView):
    """
    List existing vitals or create a new vital record.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewVital,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateVital,
        ),
    }

    serializer_classes = {
        "GET": VitalListSerializer,
        "POST": VitalCreateSerializer,
    }

    detail_serializer_class = VitalDetailSerializer

    create_service = create_vital

    create_success_message = "Vital created successfully."

    search_fields = (
        "patient__mrn",
        "patient__first_name",
        "patient__last_name",
        "provider__provider_number",
        "encounter__encounter_number",
    )

    ordering = ("-recorded_at",)

    ordering_fields = (
        "recorded_at",
        "status",
        "temperature",
        "pulse",
        "oxygen_saturation",
        "created_at",
    )

    filterset_fields = (
        "status",
        "temperature_unit",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Vital]:
        """
        Return the vitals queryset.
        """

        return get_vitals()


__all__ = [
    "VitalListCreateAPIView",
]
