"""
URL configuration for the Accounts application.
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
            "apps.accounts.api.urls",
        ),
    ),
]

__all__ = [
    "urlpatterns",
]
