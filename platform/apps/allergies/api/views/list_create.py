"""
API views for listing and creating allergies.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.allergies.api.serializers import (
    AllergyCreateSerializer,
    AllergyDetailSerializer,
    AllergyListSerializer,
)
from apps.allergies.models import Allergy
from apps.allergies.permissions import (
    CanCreateAllergy,
    CanViewAllergy,
)
from apps.allergies.selectors import get_allergies
from apps.allergies.services import create_allergy
from apps.common.api.base_generics import BaseListCreateAPIView

ALLERGY_TAG: Final[tuple[str, ...]] = ("Allergies",)


@extend_schema(tags=ALLERGY_TAG)
class AllergyListCreateAPIView(BaseListCreateAPIView):
    """
    List existing allergies or create a new allergy.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAllergy,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateAllergy,
        ),
    }

    serializer_classes = {
        "GET": AllergyListSerializer,
        "POST": AllergyCreateSerializer,
    }

    detail_serializer_class = AllergyDetailSerializer

    create_service = create_allergy

    create_success_message = "Allergy created successfully."

    search_fields = (
        "allergen",
        "patient__mrn",
        "patient__first_name",
        "patient__last_name",
        "provider__provider_number",
    )

    ordering = ("-created_at",)

    ordering_fields = (
        "allergen",
        "category",
        "severity",
        "status",
        "created_at",
    )

    filterset_fields = (
        "category",
        "severity",
        "status",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Allergy]:
        """
        Return the allergies queryset.
        """

        return get_allergies()


__all__ = [
    "AllergyListCreateAPIView",
]
