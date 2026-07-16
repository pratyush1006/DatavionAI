"""
RBAC API URL configuration.
"""

from __future__ import annotations

from django.urls import (
    include,
    path,
)

app_name = "rbac-api"

urlpatterns = [
    # =========================================================================
    # Permission
    # =========================================================================
    path(
        "permissions/",
        include(
            (
                "apps.platform.rbac.api.permission.urls",
                "permissions",
            ),
        ),
    ),
    # =========================================================================
    # Permission Group
    # =========================================================================
    path(
        "permission-groups/",
        include(
            (
                "apps.platform.rbac.api.permission_group.urls",
                "permission-groups",
            ),
        ),
    ),
    # =========================================================================
    # Role
    # =========================================================================
    path(
        "roles/",
        include(
            (
                "apps.platform.rbac.api.role.urls",
                "roles",
            ),
        ),
    ),
    # =========================================================================
    # Role Permission
    # =========================================================================
    path(
        "role-permissions/",
        include(
            (
                "apps.platform.rbac.api.role_permission.urls",
                "role-permissions",
            ),
        ),
    ),
    # =========================================================================
    # User Role
    # =========================================================================
    path(
        "user-roles/",
        include(
            (
                "apps.platform.rbac.api.user_role.urls",
                "user-roles",
            ),
        ),
    ),
    # =========================================================================
    # Organization Role
    # =========================================================================
    path(
        "organization-roles/",
        include(
            (
                "apps.platform.rbac.api.organization_role.urls",
                "organization-roles",
            ),
        ),
    ),
    # ============================================================================
    # Role Hierarchy
    # ============================================================================
    path(
        "role-hierarchies/",
        include(
            (
                "apps.platform.rbac.api.role_hierarchy.urls",
                "role-hierarchies",
            ),
        ),
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
