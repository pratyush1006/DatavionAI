"""
API views for laboratory tests.
"""

from __future__ import annotations

from apps.clinical.laboratories.api.serializers.laboratory_test import (
    LaboratoryTestDetailSerializer,
    LaboratoryTestUpdateSerializer,
)
from apps.clinical.laboratories.permissions import (
    IsLaboratoryTestUser,
)
from apps.clinical.laboratories.selectors import (
    list_laboratory_tests,
)
from apps.clinical.laboratories.services import (
    cancel_laboratory_test,
    update_laboratory_test,
)
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Laboratories"],
)
class LaboratoryTestRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update and delete laboratory tests.
    """

    permission_classes = (IsLaboratoryTestUser,)

    lookup_field = "id"
    lookup_url_kwarg = "uuid"

    update_service = update_laboratory_test

    delete_service = cancel_laboratory_test

    serializer_classes = {
        "GET": LaboratoryTestDetailSerializer,
        "PUT": LaboratoryTestUpdateSerializer,
        "PATCH": LaboratoryTestUpdateSerializer,
    }

    def get_queryset(
        self,
    ):
        """
        Return the queryset.
        """

        return list_laboratory_tests()


__all__ = [
    "LaboratoryTestRetrieveUpdateDestroyAPIView",
]
