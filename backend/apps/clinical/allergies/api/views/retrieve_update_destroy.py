"""
API views for retrieving, updating, and deleting allergies.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.clinical.allergies.api.serializers import (
    AllergyDetailSerializer,
    AllergyUpdateSerializer,
)
from apps.clinical.allergies.models import Allergy
from apps.clinical.allergies.permissions import (
    CanDeleteAllergy,
    CanUpdateAllergy,
    CanViewAllergy,
)
from apps.clinical.allergies.selectors import (
    get_allergy_by_id,
)
from apps.clinical.allergies.services import (
    delete_allergy,
    update_allergy,
)
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)

ALLERGY_TAG: Final[tuple[str, ...]] = ("Allergies",)


@extend_schema(tags=ALLERGY_TAG)
class AllergyRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete an allergy.
    """

    lookup_url_kwarg = "allergy_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAllergy,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateAllergy,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateAllergy,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteAllergy,
        ),
    }

    serializer_classes = {
        "GET": AllergyDetailSerializer,
        "PUT": AllergyUpdateSerializer,
        "PATCH": AllergyUpdateSerializer,
    }

    detail_serializer_class = AllergyDetailSerializer

    update_service = update_allergy

    delete_service = delete_allergy

    def get_object(
        self,
    ) -> Allergy:
        """
        Return the requested allergy.
        """

        return get_allergy_by_id(
            allergy_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "AllergyRetrieveUpdateDestroyAPIView",
]
