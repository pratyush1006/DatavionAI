"""
RBAC URL configuration.
"""

from __future__ import annotations

from django.urls import (
    include,
    path,
)

urlpatterns = [
    path(
        "",
        include(
            (
                "apps.platform.rbac.api.urls",
                "rbac-api",
            ),
            namespace="rbac-api",
        ),
    ),
]

__all__ = [
    "urlpatterns",
]
