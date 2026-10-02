"""
Audit API URLs.
"""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path(
        "",
        include(
            "apps.platform.audit.api.urls.audit",
        ),
    ),
]

__all__ = [
    "urlpatterns",
]
