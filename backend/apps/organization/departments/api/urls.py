from django.urls import path

from apps.organization.departments.api.views import (
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
        "<uuid:department_id>/",
        DepartmentRetrieveUpdateDestroyAPIView.as_view(),
        name="department-detail",
    ),
]
