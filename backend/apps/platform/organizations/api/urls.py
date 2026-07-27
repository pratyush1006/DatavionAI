"""
Organization API router.
"""

from __future__ import annotations

from django.urls import (
    include,
    path,
)

app_name = "organizations-api"

urlpatterns = [
    path(
        "",
        include(
            (
                "apps.platform.organizations.api.organization.urls",
                "organizations",
            ),
        ),
    ),
    path(
        "hierarchies/",
        include(
            (
                "apps.platform.organizations.api.organization_hierarchy.urls",
                "organization-hierarchy",
            ),
        ),
    ),
    path(
        "branding/",
        include(
            (
                "apps.platform.organizations.api.organization_branding.urls",
                "organization-branding",
            ),
        ),
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
