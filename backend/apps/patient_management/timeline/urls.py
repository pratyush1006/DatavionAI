"""
Top-level URL configuration for Patient Timeline.
"""

from __future__ import annotations

from django.urls import include, path

urlpatterns = (path("", include("apps.patient_management.timeline.api.urls")),)


__all__ = ("urlpatterns",)
