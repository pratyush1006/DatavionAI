"""
Accounts application URLs.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "accounts"

urlpatterns = [
    path(
        "",
        include("apps.platform.accounts.api.urls.authentication"),
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
