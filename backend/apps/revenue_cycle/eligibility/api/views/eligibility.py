"""
API views for the Eligibility Check module.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.revenue_cycle.eligibility.api.serializers import (
    EligibilityCheckCreateSerializer,
    EligibilityCheckDetailSerializer,
    EligibilityCheckListSerializer,
    EligibilityCheckUpdateSerializer,
)
from apps.revenue_cycle.eligibility.models import EligibilityCheck
from apps.revenue_cycle.eligibility.permissions import (
    CanCreateEligibilityCheck,
    CanDeleteEligibilityCheck,
    CanUpdateEligibilityCheck,
    CanViewEligibilityCheck,
)
from apps.revenue_cycle.eligibility.selectors import EligibilityCheckSelector
from apps.revenue_cycle.eligibility.services import EligibilityCheckService
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

TAG: Final[tuple[str, ...]] = ("Eligibility",)


@extend_schema(tags=TAG)
class EligibilityCheckListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewEligibilityCheck),
        "POST": (IsAuthenticated, CanCreateEligibilityCheck),
    }

    serializer_classes = {
        "GET": EligibilityCheckListSerializer,
        "POST": EligibilityCheckCreateSerializer,
    }

    detail_serializer_class = EligibilityCheckDetailSerializer

    create_service = EligibilityCheckService.create

    create_success_message = "Eligibility Check created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[EligibilityCheck]:
        return EligibilityCheckSelector.queryset()


@extend_schema(tags=TAG)
class EligibilityCheckRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "eligibility_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewEligibilityCheck),
        "PUT": (IsAuthenticated, CanUpdateEligibilityCheck),
        "PATCH": (IsAuthenticated, CanUpdateEligibilityCheck),
        "DELETE": (IsAuthenticated, CanDeleteEligibilityCheck),
    }

    serializer_classes = {
        "GET": EligibilityCheckDetailSerializer,
        "PUT": EligibilityCheckUpdateSerializer,
        "PATCH": EligibilityCheckUpdateSerializer,
    }

    update_service = EligibilityCheckService.update
    delete_service = EligibilityCheckService.delete

    def get_object(
        self,
    ) -> EligibilityCheck:
        return EligibilityCheckSelector.get(
            eligibility_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "EligibilityCheckListCreateAPIView",
    "EligibilityCheckRetrieveUpdateDestroyAPIView",
]
