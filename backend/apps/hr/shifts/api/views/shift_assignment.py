"""
API views for shift assignments.
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
from apps.hr.shifts.api.serializers import (
    ShiftAssignmentCreateSerializer,
    ShiftAssignmentDetailSerializer,
    ShiftAssignmentListSerializer,
    ShiftAssignmentUpdateSerializer,
)
from apps.hr.shifts.models import ShiftAssignment
from apps.hr.shifts.permissions import (
    CanCreateShiftAssignment,
    CanDeleteShiftAssignment,
    CanUpdateShiftAssignment,
    CanViewShiftAssignment,
)
from apps.hr.shifts.selectors import (
    get_shift_assignment_by_id,
    get_shift_assignments,
)
from apps.hr.shifts.services import (
    create_shift_assignment,
    delete_shift_assignment,
    update_shift_assignment,
)

SHIFTS_TAG: Final[tuple[str, ...]] = ("Shifts",)


@extend_schema(tags=SHIFTS_TAG)
class ShiftAssignmentListCreateAPIView(BaseListCreateAPIView):
    """
    List existing shift assignments or create a new one.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewShiftAssignment),
        "POST": (IsAuthenticated, CanCreateShiftAssignment),
    }

    serializer_classes = {
        "GET": ShiftAssignmentListSerializer,
        "POST": ShiftAssignmentCreateSerializer,
    }

    detail_serializer_class = ShiftAssignmentDetailSerializer

    create_service = create_shift_assignment

    create_success_message = "Shift assignment created successfully."

    search_fields = (
        "employee__employee_code",
        "shift__name",
    )

    ordering = ("-work_date",)

    ordering_fields = ("work_date", "created_at")

    filterset_fields = (
        "organization",
        "employee",
        "shift",
        "status",
        "work_date",
    )

    def get_queryset(self) -> QuerySet[ShiftAssignment]:
        return get_shift_assignments()


@extend_schema(tags=SHIFTS_TAG)
class ShiftAssignmentRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a shift assignment.
    """

    lookup_url_kwarg = "shift_assignment_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewShiftAssignment),
        "PUT": (IsAuthenticated, CanUpdateShiftAssignment),
        "PATCH": (IsAuthenticated, CanUpdateShiftAssignment),
        "DELETE": (IsAuthenticated, CanDeleteShiftAssignment),
    }

    serializer_classes = {
        "GET": ShiftAssignmentDetailSerializer,
        "PUT": ShiftAssignmentUpdateSerializer,
        "PATCH": ShiftAssignmentUpdateSerializer,
    }

    detail_serializer_class = ShiftAssignmentDetailSerializer

    update_service = update_shift_assignment

    delete_service = delete_shift_assignment

    update_success_message = "Shift assignment updated successfully."

    def get_object(self):
        return get_shift_assignment_by_id(
            shift_assignment_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "ShiftAssignmentListCreateAPIView",
    "ShiftAssignmentRetrieveUpdateDestroyAPIView",
]
