from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path("", include("apps.clinical.laboratories.api.urls")),
]

__all__ = ("urlpatterns",)
