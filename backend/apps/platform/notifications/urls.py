"""
Notification application URLs.
"""

from __future__ import annotations

from django.urls import (
    include,
    path,
)

app_name = "notifications"

urlpatterns = [
    path(
        "",
        include(
            "apps.platform.notifications.api.urls",
        ),
    ),
]
