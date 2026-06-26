from django.urls import path

from apps.rbac.api.views import (
    RoleListCreateAPIView,
    RoleRetrieveUpdateDestroyAPIView,
    UserRoleAPIView,
    UserRoleDeleteAPIView,
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
    path(
    "users/<int:user_id>/roles/",
    UserRoleAPIView.as_view(),
    name="user-role",
),

path(
    "users/<int:user_id>/roles/<int:role_id>/",
    UserRoleDeleteAPIView.as_view(),
    name="user-role-delete",
),
]