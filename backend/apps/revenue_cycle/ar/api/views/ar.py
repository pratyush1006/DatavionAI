"""
API views for the AR Record module.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.revenue_cycle.ar.api.serializers import (
    AccountsReceivableCreateSerializer,
    AccountsReceivableDetailSerializer,
    AccountsReceivableListSerializer,
    AccountsReceivableUpdateSerializer,
)
from apps.revenue_cycle.ar.models import AccountsReceivable
from apps.revenue_cycle.ar.permissions import (
    CanCreateAccountsReceivable,
    CanDeleteAccountsReceivable,
    CanUpdateAccountsReceivable,
    CanViewAccountsReceivable,
)
from apps.revenue_cycle.ar.selectors import AccountsReceivableSelector
from apps.revenue_cycle.ar.services import AccountsReceivableService
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

TAG: Final[tuple[str, ...]] = ("Accounts Receivable",)


@extend_schema(tags=TAG)
class AccountsReceivableListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewAccountsReceivable),
        "POST": (IsAuthenticated, CanCreateAccountsReceivable),
    }

    serializer_classes = {
        "GET": AccountsReceivableListSerializer,
        "POST": AccountsReceivableCreateSerializer,
    }

    detail_serializer_class = AccountsReceivableDetailSerializer

    create_service = AccountsReceivableService.create

    create_success_message = "AR Record created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[AccountsReceivable]:
        return AccountsReceivableSelector.queryset()


@extend_schema(tags=TAG)
class AccountsReceivableRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "ar_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewAccountsReceivable),
        "PUT": (IsAuthenticated, CanUpdateAccountsReceivable),
        "PATCH": (IsAuthenticated, CanUpdateAccountsReceivable),
        "DELETE": (IsAuthenticated, CanDeleteAccountsReceivable),
    }

    serializer_classes = {
        "GET": AccountsReceivableDetailSerializer,
        "PUT": AccountsReceivableUpdateSerializer,
        "PATCH": AccountsReceivableUpdateSerializer,
    }

    update_service = AccountsReceivableService.update
    delete_service = AccountsReceivableService.delete

    def get_object(
        self,
    ) -> AccountsReceivable:
        return AccountsReceivableSelector.get(
            ar_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "AccountsReceivableListCreateAPIView",
    "AccountsReceivableRetrieveUpdateDestroyAPIView",
]
