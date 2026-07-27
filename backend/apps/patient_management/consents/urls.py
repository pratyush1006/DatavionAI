"""
URL configuration for the Patient Consents module.
"""

from __future__ import annotations

from django.urls import (
    include,
    path,
)

app_name = "consents"

urlpatterns = [
    path(
        "",
        include(
            "apps.patient_management.consents.api.urls.consent",
        ),
    ),
]
