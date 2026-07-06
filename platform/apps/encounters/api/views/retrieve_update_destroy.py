"""
API views for retrieving, updating, and deleting encounters.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.encounters.api.serializers import (
    EncounterDetailSerializer,
    EncounterUpdateSerializer,
)
from apps.encounters.models import Encounter
from apps.encounters.permissions import (
    CanDeleteEncounter,
    CanUpdateEncounter,
    CanViewEncounter,
)
from apps.encounters.selectors import (
    get_encounter_by_id,
)
from apps.encounters.services import (
    delete_encounter,
    update_encounter,
)

ENCOUNTER_TAG: Final[tuple[str, ...]] = ("Encounters",)


@extend_schema(tags=ENCOUNTER_TAG)
class EncounterRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete an encounter.
    """

    lookup_url_kwarg = "encounter_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewEncounter,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateEncounter,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateEncounter,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteEncounter,
        ),
    }

    serializer_classes = {
        "GET": EncounterDetailSerializer,
        "PUT": EncounterUpdateSerializer,
        "PATCH": EncounterUpdateSerializer,
    }

    detail_serializer_class = EncounterDetailSerializer

    update_service = update_encounter

    delete_service = delete_encounter

    def get_object(
        self,
    ) -> Encounter:
        """
        Return the requested encounter.
        """

        return get_encounter_by_id(
            encounter_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "EncounterRetrieveUpdateDestroyAPIView",
]
