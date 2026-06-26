from django.urls import path

from apps.rbac.api.views import (
    PermissionListAPIView,
    RoleListCreateAPIView,
    RolePermissionAPIView,
    RolePermissionDeleteAPIView,
    RoleRetrieveUpdateDestroyAPIView,
    UserRoleAPIView,
    UserRoleDeleteAPIView,
)

urlpatterns = [

    # ==========================================
    # Roles
    # ==========================================

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

    # ==========================================
    # User Roles
    # ==========================================

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

    # ==========================================
    # Permissions
    # ==========================================

    path(
        "permissions/",
        PermissionListAPIView.as_view(),
        name="permission-list",
    ),

    path(
        "roles/<int:role_id>/permissions/",
        RolePermissionAPIView.as_view(),
        name="role-permission",
    ),

    path(
        "roles/<int:role_id>/permissions/<int:permission_id>/",
        RolePermissionDeleteAPIView.as_view(),
        name="role-permission-delete",
    ),
]