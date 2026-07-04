"""
API views for listing and creating encounters.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.encounters.api.serializers import (
    EncounterCreateSerializer,
    EncounterDetailSerializer,
    EncounterListSerializer,
)
from apps.encounters.models import Encounter
from apps.encounters.permissions import (
    CanCreateEncounter,
    CanViewEncounter,
)
from apps.encounters.selectors import get_encounters
from apps.encounters.services import create_encounter

ENCOUNTER_TAG: Final[tuple[str, ...]] = (
    "Encounters",
)


@extend_schema(tags=ENCOUNTER_TAG)
class EncounterListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List existing encounters or create a new encounter.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewEncounter,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateEncounter,
        ),
    }

    serializer_classes = {
        "GET": EncounterListSerializer,
        "POST": EncounterCreateSerializer,
    }

    detail_serializer_class = (
        EncounterDetailSerializer
    )

    create_service = create_encounter

    create_success_message = (
        "Encounter created successfully."
    )

    search_fields = (
        "encounter_number",
        "patient__first_name",
        "patient__last_name",
        "provider__employee__user__first_name",
        "provider__employee__user__last_name",
    )

    ordering = (
        "-created_at",
    )

    ordering_fields = (
        "encounter_number",
        "status",
        "started_at",
        "created_at",
    )

    filterset_fields = (
        "status",
        "is_billable",
        "is_active",
        "patient",
        "provider",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Encounter]:
        """
        Return the encounter queryset.
        """

        return get_encounters()


__all__ = [
    "EncounterListCreateAPIView",
]
