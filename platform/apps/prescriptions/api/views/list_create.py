"""
API views for listing and creating prescriptions.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.prescriptions.api.serializers import (
    PrescriptionCreateSerializer,
    PrescriptionDetailSerializer,
    PrescriptionListSerializer,
)
from apps.prescriptions.models import Prescription
from apps.prescriptions.permissions import (
    CanCreatePrescription,
    CanViewPrescription,
)
from apps.prescriptions.selectors import get_prescriptions
from apps.prescriptions.services import create_prescription

PRESCRIPTION_TAG: Final[tuple[str, ...]] = (
    "Prescriptions",
)


@extend_schema(tags=PRESCRIPTION_TAG)
class PrescriptionListCreateAPIView(BaseListCreateAPIView):
    """
    List existing prescriptions or create a new prescription.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewPrescription,
        ),
        "POST": (
            IsAuthenticated,
            CanCreatePrescription,
        ),
    }

    serializer_classes = {
        "GET": PrescriptionListSerializer,
        "POST": PrescriptionCreateSerializer,
    }

    detail_serializer_class = (
        PrescriptionDetailSerializer
    )

    create_service = create_prescription

    create_success_message = (
        "Prescription created successfully."
    )

    search_fields = (
        "prescription_number",
        "patient__mrn",
        "patient__first_name",
        "patient__last_name",
        "provider__provider_number",
        "medication__generic_name",
        "medication__brand_name",
    )

    ordering = (
        "-created_at",
    )

    ordering_fields = (
        "prescription_number",
        "start_date",
        "end_date",
        "status",
        "created_at",
    )

    filterset_fields = (
        "status",
        "frequency",
        "is_prn",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Prescription]:
        """
        Return the prescriptions queryset.
        """

        return get_prescriptions()


__all__ = [
    "PrescriptionListCreateAPIView",
]