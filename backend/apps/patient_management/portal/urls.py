"""
Patient Portal URL exports.
"""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.patient_management.portal.api.urls"),
    ),
]

__all__ = ("urlpatterns",)
