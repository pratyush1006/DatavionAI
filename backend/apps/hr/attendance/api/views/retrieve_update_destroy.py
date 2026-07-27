"""
API views for retrieving, updating and deleting attendance records.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.hr.attendance.api.serializers import (
    AttendanceRecordDetailSerializer,
    AttendanceRecordUpdateSerializer,
)
from apps.hr.attendance.permissions import (
    CanDeleteAttendance,
    CanUpdateAttendance,
    CanViewAttendance,
)
from apps.hr.attendance.selectors import (
    get_attendance_record_by_id,
)
from apps.hr.attendance.services import (
    delete_attendance_record,
    update_attendance_record,
)

ATTENDANCE_TAG: Final[tuple[str, ...]] = ("Attendance",)


@extend_schema(tags=ATTENDANCE_TAG)
class AttendanceRecordRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete an attendance record.
    """

    lookup_url_kwarg = "attendance_record_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAttendance,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateAttendance,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateAttendance,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteAttendance,
        ),
    }

    serializer_classes = {
        "GET": AttendanceRecordDetailSerializer,
        "PUT": AttendanceRecordUpdateSerializer,
        "PATCH": AttendanceRecordUpdateSerializer,
    }

    detail_serializer_class = AttendanceRecordDetailSerializer

    update_service = update_attendance_record

    delete_service = delete_attendance_record

    update_success_message = "Attendance record updated successfully."

    def get_object(self):
        """
        Return the requested attendance record.
        """

        return get_attendance_record_by_id(
            attendance_record_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "AttendanceRecordRetrieveUpdateDestroyAPIView",
]
