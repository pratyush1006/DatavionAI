"""
Public API routing for the Accounts application.
"""

from __future__ import annotations

from django.urls import (
    include,
    path,
)

app_name = "accounts-api"


urlpatterns = [
    path(
        "authentication/",
        include(
            "apps.platform.accounts.api.urls.authentication",
        ),
    ),
    path(
        "users/",
        include(
            "apps.platform.accounts.api.urls.users",
        ),
    ),
]
