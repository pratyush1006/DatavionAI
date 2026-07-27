"""
API views for leave balances.
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
from apps.hr.leave.api.serializers import (
    LeaveBalanceCreateSerializer,
    LeaveBalanceDetailSerializer,
    LeaveBalanceListSerializer,
    LeaveBalanceUpdateSerializer,
)
from apps.hr.leave.models import LeaveBalance
from apps.hr.leave.permissions import (
    CanCreateLeaveBalance,
    CanDeleteLeaveBalance,
    CanUpdateLeaveBalance,
    CanViewLeaveBalance,
)
from apps.hr.leave.selectors import (
    get_leave_balance_by_id,
    get_leave_balances,
)
from apps.hr.leave.services import (
    create_leave_balance,
    delete_leave_balance,
    update_leave_balance,
)

LEAVE_TAG: Final[tuple[str, ...]] = ("Leave",)


@extend_schema(tags=LEAVE_TAG)
class LeaveBalanceListCreateAPIView(BaseListCreateAPIView):
    """
    List existing leave balances or create a new one.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewLeaveBalance),
        "POST": (IsAuthenticated, CanCreateLeaveBalance),
    }

    serializer_classes = {
        "GET": LeaveBalanceListSerializer,
        "POST": LeaveBalanceCreateSerializer,
    }

    detail_serializer_class = LeaveBalanceDetailSerializer

    create_service = create_leave_balance

    create_success_message = "Leave balance created successfully."

    search_fields = (
        "employee__employee_code",
        "leave_type__name",
    )

    ordering = ("-year",)

    ordering_fields = ("year", "created_at")

    filterset_fields = ("employee", "leave_type", "year")

    def get_queryset(self) -> QuerySet[LeaveBalance]:
        return get_leave_balances()


@extend_schema(tags=LEAVE_TAG)
class LeaveBalanceRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a leave balance.
    """

    lookup_url_kwarg = "leave_balance_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewLeaveBalance),
        "PUT": (IsAuthenticated, CanUpdateLeaveBalance),
        "PATCH": (IsAuthenticated, CanUpdateLeaveBalance),
        "DELETE": (IsAuthenticated, CanDeleteLeaveBalance),
    }

    serializer_classes = {
        "GET": LeaveBalanceDetailSerializer,
        "PUT": LeaveBalanceUpdateSerializer,
        "PATCH": LeaveBalanceUpdateSerializer,
    }

    detail_serializer_class = LeaveBalanceDetailSerializer

    update_service = update_leave_balance

    delete_service = delete_leave_balance

    update_success_message = "Leave balance updated successfully."

    def get_object(self):
        return get_leave_balance_by_id(
            leave_balance_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "LeaveBalanceListCreateAPIView",
    "LeaveBalanceRetrieveUpdateDestroyAPIView",
]
