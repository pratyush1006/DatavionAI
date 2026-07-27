"""
API URLs for the Patient Registration module.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "registration"

urlpatterns = [
    path(
        "",
        include(
            (
                "apps.patient_management.registration.api.urls.registration",
                "registration-api",
            ),
        ),
    ),
]
