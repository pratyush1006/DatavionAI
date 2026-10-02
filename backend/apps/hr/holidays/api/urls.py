from django.urls import path

from apps.hr.holidays.api.views import (
    HolidayApplyToAttendanceAPIView,
    HolidayListCreateAPIView,
    HolidayRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        HolidayListCreateAPIView.as_view(),
        name="holiday-list-create",
    ),
    path(
        "<int:holiday_id>/",
        HolidayRetrieveUpdateDestroyAPIView.as_view(),
        name="holiday-detail",
    ),
    path(
        "<int:holiday_id>/apply-to-attendance/",
        HolidayApplyToAttendanceAPIView.as_view(),
        name="holiday-apply-to-attendance",
    ),
]
