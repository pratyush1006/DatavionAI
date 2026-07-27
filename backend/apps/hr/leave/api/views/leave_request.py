"""
API views for leave requests.
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
    LeaveRequestCreateSerializer,
    LeaveRequestDetailSerializer,
    LeaveRequestListSerializer,
    LeaveRequestUpdateSerializer,
)
from apps.hr.leave.models import LeaveRequest
from apps.hr.leave.permissions import (
    CanCreateLeaveRequest,
    CanDeleteLeaveRequest,
    CanUpdateLeaveRequest,
    CanViewLeaveRequest,
)
from apps.hr.leave.selectors import (
    get_leave_request_by_id,
    get_leave_requests,
)
from apps.hr.leave.services import (
    create_leave_request,
    delete_leave_request,
    update_leave_request,
)

LEAVE_TAG: Final[tuple[str, ...]] = ("Leave",)


@extend_schema(tags=LEAVE_TAG)
class LeaveRequestListCreateAPIView(BaseListCreateAPIView):
    """
    List existing leave requests or create a new one.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewLeaveRequest),
        "POST": (IsAuthenticated, CanCreateLeaveRequest),
    }

    serializer_classes = {
        "GET": LeaveRequestListSerializer,
        "POST": LeaveRequestCreateSerializer,
    }

    detail_serializer_class = LeaveRequestDetailSerializer

    create_service = create_leave_request

    create_success_message = "Leave request submitted successfully."

    search_fields = (
        "employee__employee_code",
        "leave_type__name",
        "reason",
    )

    ordering = ("-start_date",)

    ordering_fields = ("start_date", "end_date", "created_at")

    filterset_fields = (
        "organization",
        "employee",
        "leave_type",
        "status",
    )

    def get_queryset(self) -> QuerySet[LeaveRequest]:
        return get_leave_requests()


@extend_schema(tags=LEAVE_TAG)
class LeaveRequestRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a leave request.
    """

    lookup_url_kwarg = "leave_request_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewLeaveRequest),
        "PUT": (IsAuthenticated, CanUpdateLeaveRequest),
        "PATCH": (IsAuthenticated, CanUpdateLeaveRequest),
        "DELETE": (IsAuthenticated, CanDeleteLeaveRequest),
    }

    serializer_classes = {
        "GET": LeaveRequestDetailSerializer,
        "PUT": LeaveRequestUpdateSerializer,
        "PATCH": LeaveRequestUpdateSerializer,
    }

    detail_serializer_class = LeaveRequestDetailSerializer

    update_service = update_leave_request

    delete_service = delete_leave_request

    update_success_message = "Leave request updated successfully."

    def get_object(self):
        return get_leave_request_by_id(
            leave_request_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "LeaveRequestListCreateAPIView",
    "LeaveRequestRetrieveUpdateDestroyAPIView",
]
