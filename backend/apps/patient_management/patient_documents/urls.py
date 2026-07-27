"""
URL configuration for the Patient Documents module.
"""

from __future__ import annotations

from django.urls import (
    include,
    path,
)

app_name = "patient-documents"

urlpatterns = [
    path(
        "",
        include(
            "apps.patient_management.patient_documents.api.urls.patient_document",
        ),
    ),
]
