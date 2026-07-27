"""
URL configuration for the Patient Preferences module.
"""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path(
        "preferences/",
        include(
            "apps.patient_management.preferences.api.urls.preference",
        ),
    ),
    path(
        "communication-preferences/",
        include(
            "apps.patient_management.preferences.api.urls.communication_preference",
        ),
    ),
]
