from __future__ import annotations

from django.urls import include, path

app_name = "patient-management"

urlpatterns = [
    path(
        "registrations/",
        include(
            "apps.patient_management.registration.api.urls",
        ),
    ),
    # Other patient management modules
    path(
        "patients/",
        include(
            "apps.patient_management.patients.api.urls",
        ),
    ),
    path(
        "preferences/",
        include(
            "apps.patient_management.preferences.api.urls",
        ),
    ),
    path(
        "contacts/",
        include(
            "apps.patient_management.contacts.api.urls",
        ),
    ),
]
