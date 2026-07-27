"""
API views for listing and creating attendance records.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.hr.attendance.api.serializers import (
    AttendanceRecordCreateSerializer,
    AttendanceRecordDetailSerializer,
    AttendanceRecordListSerializer,
)
from apps.hr.attendance.models import AttendanceRecord
from apps.hr.attendance.permissions import (
    CanCreateAttendance,
    CanViewAttendance,
)
from apps.hr.attendance.selectors import (
    get_attendance_records,
)
from apps.hr.attendance.services import (
    create_attendance_record,
)

ATTENDANCE_TAG: Final[tuple[str, ...]] = ("Attendance",)


@extend_schema(tags=ATTENDANCE_TAG)
class AttendanceRecordListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List existing attendance records or create a new one.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAttendance,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateAttendance,
        ),
    }

    serializer_classes = {
        "GET": AttendanceRecordListSerializer,
        "POST": AttendanceRecordCreateSerializer,
    }

    detail_serializer_class = AttendanceRecordDetailSerializer

    create_service = create_attendance_record

    create_success_message = "Attendance record created successfully."

    search_fields = (
        "employee__employee_code",
        "employee__user__first_name",
        "employee__user__last_name",
    )

    ordering = ("-work_date",)

    ordering_fields = (
        "work_date",
        "created_at",
    )

    filterset_fields = (
        "organization",
        "employee",
        "status",
        "work_date",
    )

    def get_queryset(
        self,
    ) -> QuerySet[AttendanceRecord]:
        """
        Return attendance records.
        """

        return get_attendance_records()


__all__ = [
    "AttendanceRecordListCreateAPIView",
]
