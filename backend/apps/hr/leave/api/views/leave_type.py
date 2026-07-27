"""
API views for leave types.
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
    LeaveTypeCreateSerializer,
    LeaveTypeDetailSerializer,
    LeaveTypeListSerializer,
    LeaveTypeUpdateSerializer,
)
from apps.hr.leave.models import LeaveType
from apps.hr.leave.permissions import (
    CanCreateLeaveType,
    CanDeleteLeaveType,
    CanUpdateLeaveType,
    CanViewLeaveType,
)
from apps.hr.leave.selectors import (
    get_leave_type_by_id,
    get_leave_types,
)
from apps.hr.leave.services import (
    create_leave_type,
    delete_leave_type,
    update_leave_type,
)

LEAVE_TAG: Final[tuple[str, ...]] = ("Leave",)


@extend_schema(tags=LEAVE_TAG)
class LeaveTypeListCreateAPIView(BaseListCreateAPIView):
    """
    List existing leave types or create a new one.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewLeaveType),
        "POST": (IsAuthenticated, CanCreateLeaveType),
    }

    serializer_classes = {
        "GET": LeaveTypeListSerializer,
        "POST": LeaveTypeCreateSerializer,
    }

    detail_serializer_class = LeaveTypeDetailSerializer

    create_service = create_leave_type

    create_success_message = "Leave type created successfully."

    search_fields = ("name", "code")

    ordering = ("name",)

    ordering_fields = ("name", "created_at")

    filterset_fields = ("organization", "is_paid", "is_active")

    def get_queryset(self) -> QuerySet[LeaveType]:
        return get_leave_types()


@extend_schema(tags=LEAVE_TAG)
class LeaveTypeRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a leave type.
    """

    lookup_url_kwarg = "leave_type_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewLeaveType),
        "PUT": (IsAuthenticated, CanUpdateLeaveType),
        "PATCH": (IsAuthenticated, CanUpdateLeaveType),
        "DELETE": (IsAuthenticated, CanDeleteLeaveType),
    }

    serializer_classes = {
        "GET": LeaveTypeDetailSerializer,
        "PUT": LeaveTypeUpdateSerializer,
        "PATCH": LeaveTypeUpdateSerializer,
    }

    detail_serializer_class = LeaveTypeDetailSerializer

    update_service = update_leave_type

    delete_service = delete_leave_type

    update_success_message = "Leave type updated successfully."

    def get_object(self):
        return get_leave_type_by_id(
            leave_type_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "LeaveTypeListCreateAPIView",
    "LeaveTypeRetrieveUpdateDestroyAPIView",
]
