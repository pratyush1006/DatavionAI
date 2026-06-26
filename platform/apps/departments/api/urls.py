from django.urls import path

from apps.departments.api.views import (
    DepartmentListCreateAPIView,
    DepartmentRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        DepartmentListCreateAPIView.as_view(),
        name="department-list-create",
    ),
    path(
        "<int:department_id>/",
        DepartmentRetrieveUpdateDestroyAPIView.as_view(),
        name="department-detail",
    ),
]
