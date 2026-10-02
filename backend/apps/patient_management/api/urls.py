from __future__ import annotations

from importlib import import_module

from django.urls import include, path

app_name = "patient-management"

urlpatterns = [
    path(
        "identifiers/",
        include(
            "apps.patient_management.identifiers.api.urls",
            namespace="patient-identifiers",
        ),
    ),
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
    path("profile/", include("apps.patient_management.profile.urls")),
    path("mpi/", include("apps.patient_management.mpi.api.urls")),
    path("addresses/", include("apps.patient_management.addresses.api.urls")),
    path("emergency/", include("apps.patient_management.emergency.api.urls")),
    path("communication/", include("apps.patient_management.communication.api.urls")),
    path("consents/", include("apps.patient_management.consents.api.urls")),
    path(
        "medical_history/", include("apps.patient_management.medical_history.api.urls")
    ),
    path("relationships/", include("apps.patient_management.relationships.api.urls")),
    path(
        "family_members/",
        include(
            "apps.patient_management.family_members.api.urls",
            namespace="family-members-api",
        ),
    ),
    path("referrals/", include("apps.patient_management.referrals.api.urls")),
    path(
        "patient_documents/",
        include("apps.patient_management.patient_documents.api.urls"),
    ),
    path("timeline/", include("apps.patient_management.timeline.api.urls")),
]

# The portal package is an optional deployment component.  Some environments
# contain the patient-management core without its portal API package; importing
# a missing optional route must not make every unrelated API endpoint return
# HTTP 500 during URL resolution.
try:
    import_module("apps.patient_management.portal.api.urls")
except ModuleNotFoundError as exc:
    if exc.name != "apps.patient_management.portal.api":
        raise
else:
    urlpatterns.append(
        path("portal/", include("apps.patient_management.portal.api.urls"))
    )
