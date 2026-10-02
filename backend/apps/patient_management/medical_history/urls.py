"""Urls."""

from __future__ import annotations

from django.urls import include, path

app_name = "medical_history"

urlpatterns = [path("", include("apps.patient_management.medical_history.api.urls"))]


__all__ = ("app_name",)
