"""
API views for the Prior Authorization module.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.revenue_cycle.prior_authorization.api.serializers import (
    PriorAuthorizationRequestCreateSerializer,
    PriorAuthorizationRequestDetailSerializer,
    PriorAuthorizationRequestListSerializer,
    PriorAuthorizationRequestUpdateSerializer,
)
from apps.revenue_cycle.prior_authorization.models import PriorAuthorizationRequest
from apps.revenue_cycle.prior_authorization.permissions import (
    CanCreatePriorAuthorizationRequest,
    CanDeletePriorAuthorizationRequest,
    CanUpdatePriorAuthorizationRequest,
    CanViewPriorAuthorizationRequest,
)
from apps.revenue_cycle.prior_authorization.selectors import (
    PriorAuthorizationRequestSelector,
)
from apps.revenue_cycle.prior_authorization.services import (
    PriorAuthorizationRequestService,
)

TAG: Final[tuple[str, ...]] = ("Prior Authorization",)


@extend_schema(tags=TAG)
class PriorAuthorizationRequestListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPriorAuthorizationRequest),
        "POST": (IsAuthenticated, CanCreatePriorAuthorizationRequest),
    }

    serializer_classes = {
        "GET": PriorAuthorizationRequestListSerializer,
        "POST": PriorAuthorizationRequestCreateSerializer,
    }

    detail_serializer_class = PriorAuthorizationRequestDetailSerializer

    create_service = PriorAuthorizationRequestService.create

    create_success_message = "Prior Authorization created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[PriorAuthorizationRequest]:
        return PriorAuthorizationRequestSelector.queryset()


@extend_schema(tags=TAG)
class PriorAuthorizationRequestRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "authorization_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPriorAuthorizationRequest),
        "PUT": (IsAuthenticated, CanUpdatePriorAuthorizationRequest),
        "PATCH": (IsAuthenticated, CanUpdatePriorAuthorizationRequest),
        "DELETE": (IsAuthenticated, CanDeletePriorAuthorizationRequest),
    }

    serializer_classes = {
        "GET": PriorAuthorizationRequestDetailSerializer,
        "PUT": PriorAuthorizationRequestUpdateSerializer,
        "PATCH": PriorAuthorizationRequestUpdateSerializer,
    }

    update_service = PriorAuthorizationRequestService.update
    delete_service = PriorAuthorizationRequestService.delete

    def get_object(
        self,
    ) -> PriorAuthorizationRequest:
        return PriorAuthorizationRequestSelector.get(
            authorization_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "PriorAuthorizationRequestListCreateAPIView",
    "PriorAuthorizationRequestRetrieveUpdateDestroyAPIView",
]
