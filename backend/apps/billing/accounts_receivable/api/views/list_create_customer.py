"""
API views for listing and creating customer records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.accounts_receivable.api.serializers import (
    CustomerCreateSerializer,
    CustomerDetailSerializer,
    CustomerListSerializer,
)
from apps.billing.accounts_receivable.models import Customer
from apps.billing.accounts_receivable.permissions import (
    CanCreateAccountsReceivable,
    CanViewAccountsReceivable,
)
from apps.billing.accounts_receivable.selectors import CustomerSelector
from apps.billing.accounts_receivable.services import CustomerService
from apps.common.api.base_generics import BaseListCreateAPIView
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

CUSTOMER_TAG: Final[tuple[str, ...]] = ("Accounts Receivable",)


@extend_schema(tags=CUSTOMER_TAG)
class CustomerListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing and creating customer records.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAccountsReceivable,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateAccountsReceivable,
        ),
    }

    serializer_classes = {
        "GET": CustomerListSerializer,
        "POST": CustomerCreateSerializer,
    }

    detail_serializer_class = CustomerDetailSerializer

    create_service = CustomerService.create

    create_success_message = "Customer created successfully."

    search_fields = (
        "code",
        "name",
        "email",
        "is_active",
    )

    ordering = ("created_at",)

    ordering_fields = ("created_at",)

    filterset_fields = (
        "organization",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Customer]:
        """
        Return the customer queryset.
        """

        return CustomerSelector.queryset()


__all__ = [
    "CustomerListCreateAPIView",
]
