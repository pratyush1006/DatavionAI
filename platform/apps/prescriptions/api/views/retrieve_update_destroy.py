"""
API views for retrieving, updating, and deleting prescriptions.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.prescriptions.api.serializers import (
    PrescriptionDetailSerializer,
    PrescriptionUpdateSerializer,
)
from apps.prescriptions.models import Prescription
from apps.prescriptions.permissions import (
    CanDeletePrescription,
    CanUpdatePrescription,
    CanViewPrescription,
)
from apps.prescriptions.selectors import (
    get_prescription_by_id,
)
from apps.prescriptions.services import (
    delete_prescription,
    update_prescription,
)

PRESCRIPTION_TAG: Final[tuple[str, ...]] = (
    "Prescriptions",
)


@extend_schema(tags=PRESCRIPTION_TAG)
class PrescriptionRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a prescription.
    """

    lookup_url_kwarg = "prescription_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewPrescription,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdatePrescription,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdatePrescription,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeletePrescription,
        ),
    }

    serializer_classes = {
        "GET": PrescriptionDetailSerializer,
        "PUT": PrescriptionUpdateSerializer,
        "PATCH": PrescriptionUpdateSerializer,
    }

    detail_serializer_class = (
        PrescriptionDetailSerializer
    )

    update_service = update_prescription

    delete_service = delete_prescription

    def get_object(
        self,
    ) -> Prescription:
        """
        Return the requested prescription.
        """

        return get_prescription_by_id(
            prescription_id=self.kwargs[
                self.lookup_url_kwarg
            ],
        )


__all__ = [
    "PrescriptionRetrieveUpdateDestroyAPIView",
]