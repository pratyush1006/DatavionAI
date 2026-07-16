"""
API views for retrieving, updating, and deleting diagnoses.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.clinical.diagnoses.api.serializers import (
    DiagnosisDetailSerializer,
    DiagnosisUpdateSerializer,
)
from apps.clinical.diagnoses.models import Diagnosis
from apps.clinical.diagnoses.permissions import (
    CanDeleteDiagnosis,
    CanUpdateDiagnosis,
    CanViewDiagnosis,
)
from apps.clinical.diagnoses.selectors import (
    get_diagnosis_by_id,
)
from apps.clinical.diagnoses.services import (
    delete_diagnosis,
    update_diagnosis,
)
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)

DIAGNOSIS_TAG: Final[tuple[str, ...]] = ("Diagnoses",)


@extend_schema(tags=DIAGNOSIS_TAG)
class DiagnosisRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a diagnosis.
    """

    lookup_url_kwarg = "diagnosis_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewDiagnosis,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateDiagnosis,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateDiagnosis,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteDiagnosis,
        ),
    }

    serializer_classes = {
        "GET": DiagnosisDetailSerializer,
        "PUT": DiagnosisUpdateSerializer,
        "PATCH": DiagnosisUpdateSerializer,
    }

    detail_serializer_class = DiagnosisDetailSerializer

    update_service = update_diagnosis

    delete_service = delete_diagnosis

    def get_object(
        self,
    ) -> Diagnosis:
        """
        Return the requested diagnosis.
        """

        return get_diagnosis_by_id(
            diagnosis_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "DiagnosisRetrieveUpdateDestroyAPIView",
]
