"""
Workflow API views for holidays.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.hr.holidays.permissions import CanUpdateHoliday
from apps.hr.holidays.selectors import get_holiday_by_id
from apps.hr.holidays.services import apply_holiday_to_attendance

HOLIDAYS_TAG: Final[tuple[str, ...]] = ("Holidays",)


@extend_schema(tags=HOLIDAYS_TAG)
class HolidayApplyToAttendanceAPIView(APIView):
    """
    Mark every active employee in the holiday's organization as
    on holiday in their attendance records for that date.
    """

    permission_classes = (IsAuthenticated, CanUpdateHoliday)

    def post(self, request: Request, holiday_id) -> Response:
        instance = get_holiday_by_id(holiday_id=holiday_id)

        affected = apply_holiday_to_attendance(instance=instance)

        return Response(
            {"success": True, "attendance_records_affected": affected},
            status=status.HTTP_200_OK,
        )


__all__ = [
    "HolidayApplyToAttendanceAPIView",
]
