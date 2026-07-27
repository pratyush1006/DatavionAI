from django.urls import path

from apps.hr.shifts.api.views import (
    ShiftAssignmentListCreateAPIView,
    ShiftAssignmentRetrieveUpdateDestroyAPIView,
    ShiftListCreateAPIView,
    ShiftRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        ShiftListCreateAPIView.as_view(),
        name="shift-list-create",
    ),
    path(
        "<int:shift_id>/",
        ShiftRetrieveUpdateDestroyAPIView.as_view(),
        name="shift-detail",
    ),
    path(
        "assignments/",
        ShiftAssignmentListCreateAPIView.as_view(),
        name="shift-assignment-list-create",
    ),
    path(
        "assignments/<int:shift_assignment_id>/",
        ShiftAssignmentRetrieveUpdateDestroyAPIView.as_view(),
        name="shift-assignment-detail",
    ),
]
