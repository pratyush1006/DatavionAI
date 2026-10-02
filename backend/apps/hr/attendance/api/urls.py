from django.urls import path

from apps.hr.attendance.api.views import (
    AttendanceRecordListCreateAPIView,
    AttendanceRecordRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        AttendanceRecordListCreateAPIView.as_view(),
        name="attendance-record-list-create",
    ),
    path(
        "<int:attendance_record_id>/",
        AttendanceRecordRetrieveUpdateDestroyAPIView.as_view(),
        name="attendance-record-detail",
    ),
]
