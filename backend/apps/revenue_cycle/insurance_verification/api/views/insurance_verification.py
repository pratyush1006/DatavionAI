"""
API views for the Insurance Verification module.
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
from apps.revenue_cycle.insurance_verification.api.serializers import (
    InsuranceVerificationCreateSerializer,
    InsuranceVerificationDetailSerializer,
    InsuranceVerificationListSerializer,
    InsuranceVerificationUpdateSerializer,
)
from apps.revenue_cycle.insurance_verification.models import InsuranceVerification
from apps.revenue_cycle.insurance_verification.permissions import (
    CanCreateInsuranceVerification,
    CanDeleteInsuranceVerification,
    CanUpdateInsuranceVerification,
    CanViewInsuranceVerification,
)
from apps.revenue_cycle.insurance_verification.selectors import (
    InsuranceVerificationSelector,
)
from apps.revenue_cycle.insurance_verification.services import (
    InsuranceVerificationService,
)

TAG: Final[tuple[str, ...]] = ("Insurance Verification",)


@extend_schema(tags=TAG)
class InsuranceVerificationListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewInsuranceVerification),
        "POST": (IsAuthenticated, CanCreateInsuranceVerification),
    }

    serializer_classes = {
        "GET": InsuranceVerificationListSerializer,
        "POST": InsuranceVerificationCreateSerializer,
    }

    detail_serializer_class = InsuranceVerificationDetailSerializer

    create_service = InsuranceVerificationService.create

    create_success_message = "Insurance Verification created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[InsuranceVerification]:
        return InsuranceVerificationSelector.queryset()


@extend_schema(tags=TAG)
class InsuranceVerificationRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "verification_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewInsuranceVerification),
        "PUT": (IsAuthenticated, CanUpdateInsuranceVerification),
        "PATCH": (IsAuthenticated, CanUpdateInsuranceVerification),
        "DELETE": (IsAuthenticated, CanDeleteInsuranceVerification),
    }

    serializer_classes = {
        "GET": InsuranceVerificationDetailSerializer,
        "PUT": InsuranceVerificationUpdateSerializer,
        "PATCH": InsuranceVerificationUpdateSerializer,
    }

    update_service = InsuranceVerificationService.update
    delete_service = InsuranceVerificationService.delete

    def get_object(
        self,
    ) -> InsuranceVerification:
        return InsuranceVerificationSelector.get(
            verification_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "InsuranceVerificationListCreateAPIView",
    "InsuranceVerificationRetrieveUpdateDestroyAPIView",
]
