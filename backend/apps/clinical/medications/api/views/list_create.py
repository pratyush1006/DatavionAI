"""
API views for listing and creating medications.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.clinical.medications.api.serializers import (
    MedicationCreateSerializer,
    MedicationDetailSerializer,
    MedicationListSerializer,
)
from apps.clinical.medications.models import Medication
from apps.clinical.medications.permissions import (
    CanCreateMedication,
    CanViewMedication,
)
from apps.clinical.medications.selectors import get_medications
from apps.clinical.medications.services import create_medication
from apps.common.api.base_generics import BaseListCreateAPIView

MEDICATION_TAG: Final[tuple[str, ...]] = ("Medications",)


@extend_schema(tags=MEDICATION_TAG)
class MedicationListCreateAPIView(BaseListCreateAPIView):
    """
    List existing medications or create a new medication.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewMedication,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateMedication,
        ),
    }

    serializer_classes = {
        "GET": MedicationListSerializer,
        "POST": MedicationCreateSerializer,
    }

    detail_serializer_class = MedicationDetailSerializer

    create_service = create_medication

    create_success_message = "Medication created successfully."

    search_fields = (
        "medication_code",
        "generic_name",
        "brand_name",
        "manufacturer",
    )

    ordering = ("generic_name",)

    ordering_fields = (
        "medication_code",
        "generic_name",
        "brand_name",
        "created_at",
    )

    filterset_fields = (
        "dosage_form",
        "route",
        "is_controlled",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Medication]:
        """
        Return the medications queryset.
        """

        return get_medications()


__all__ = [
    "MedicationListCreateAPIView",
]
