"""
Platform Core API URLs.
"""

from django.urls import path

from apps.datavionos.api.views.bootstrap import (
    PlatformBootstrapAPIView,
)

app_name = "platform-core"

urlpatterns = [
    path(
        "bootstrap/",
        PlatformBootstrapAPIView.as_view(),
        name="bootstrap",
    ),
]
