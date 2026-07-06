"""
API views for retrieving, updating, and deleting medications.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.medications.api.serializers import (
    MedicationDetailSerializer,
    MedicationUpdateSerializer,
)
from apps.medications.models import Medication
from apps.medications.permissions import (
    CanDeleteMedication,
    CanUpdateMedication,
    CanViewMedication,
)
from apps.medications.selectors import (
    get_medication_by_id,
)
from apps.medications.services import (
    delete_medication,
    update_medication,
)

MEDICATION_TAG: Final[tuple[str, ...]] = ("Medications",)


@extend_schema(tags=MEDICATION_TAG)
class MedicationRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a medication.
    """

    lookup_url_kwarg = "medication_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewMedication,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateMedication,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateMedication,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteMedication,
        ),
    }

    serializer_classes = {
        "GET": MedicationDetailSerializer,
        "PUT": MedicationUpdateSerializer,
        "PATCH": MedicationUpdateSerializer,
    }

    detail_serializer_class = MedicationDetailSerializer

    update_service = update_medication

    delete_service = delete_medication

    def get_object(
        self,
    ) -> Medication:
        """
        Return the requested medication.
        """

        return get_medication_by_id(
            medication_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "MedicationRetrieveUpdateDestroyAPIView",
]
