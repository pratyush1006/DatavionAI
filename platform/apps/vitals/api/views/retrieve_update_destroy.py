"""
API views for retrieving, updating, and deleting vitals.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.vitals.api.serializers import (
    VitalDetailSerializer,
    VitalUpdateSerializer,
)
from apps.vitals.models import Vital
from apps.vitals.permissions import (
    CanDeleteVital,
    CanUpdateVital,
    CanViewVital,
)
from apps.vitals.selectors import (
    get_vital_by_id,
)
from apps.vitals.services import (
    delete_vital,
    update_vital,
)

VITAL_TAG: Final[tuple[str, ...]] = ("Vitals",)


@extend_schema(tags=VITAL_TAG)
class VitalRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a vital record.
    """

    lookup_url_kwarg = "vital_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewVital,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateVital,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateVital,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteVital,
        ),
    }

    serializer_classes = {
        "GET": VitalDetailSerializer,
        "PUT": VitalUpdateSerializer,
        "PATCH": VitalUpdateSerializer,
    }

    detail_serializer_class = VitalDetailSerializer

    update_service = update_vital

    delete_service = delete_vital

    def get_object(
        self,
    ) -> Vital:
        """
        Return the requested vital.
        """

        return get_vital_by_id(
            vital_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "VitalRetrieveUpdateDestroyAPIView",
]
