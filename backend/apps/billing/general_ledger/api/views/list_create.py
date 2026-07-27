"""
API views for listing and creating general ledger accounts.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.billing.general_ledger.api.serializers import (
    GeneralLedgerAccountCreateSerializer,
    GeneralLedgerAccountDetailSerializer,
    GeneralLedgerAccountListSerializer,
)
from apps.billing.general_ledger.models import GeneralLedgerAccount
from apps.billing.general_ledger.permissions import (
    CanCreateGeneralLedgerAccount,
    CanViewGeneralLedgerAccount,
)
from apps.billing.general_ledger.selectors import GeneralLedgerSelector
from apps.billing.general_ledger.services import GeneralLedgerService
from apps.common.api.base_generics import BaseListCreateAPIView

GENERAL_LEDGER_TAG: Final[tuple[str, ...]] = ("General Ledger",)


@extend_schema(tags=GENERAL_LEDGER_TAG)
class GeneralLedgerAccountListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing and creating general ledger accounts.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewGeneralLedgerAccount,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateGeneralLedgerAccount,
        ),
    }

    serializer_classes = {
        "GET": GeneralLedgerAccountListSerializer,
        "POST": GeneralLedgerAccountCreateSerializer,
    }

    detail_serializer_class = GeneralLedgerAccountDetailSerializer

    create_service = GeneralLedgerService.create

    create_success_message = "General ledger account created successfully."

    search_fields = (
        "code",
        "name",
        "description",
    )

    ordering = (
        "code",
        "name",
    )

    ordering_fields = (
        "code",
        "name",
        "created_at",
    )

    filterset_fields = (
        "account_type",
        "status",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[GeneralLedgerAccount]:
        """
        Return the general ledger account queryset.
        """

        return GeneralLedgerSelector.queryset()


__all__ = [
    "GeneralLedgerAccountListCreateAPIView",
]
