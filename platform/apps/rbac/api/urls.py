from django.urls import path

from apps.rbac.api.views import (
    RoleListCreateAPIView,
    RoleRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "roles/",
        RoleListCreateAPIView.as_view(),
        name="role-list-create",
    ),
    path(
        "roles/<int:role_id>/",
        RoleRetrieveUpdateDestroyAPIView.as_view(),
        name="role-detail",
    ),
]