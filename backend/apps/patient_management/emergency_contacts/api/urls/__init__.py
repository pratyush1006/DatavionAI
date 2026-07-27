"""
Emergency Contact API URLs.
"""

from django.urls import (
    include,
    path,
)

app_name = "emergency-contacts-api"

urlpatterns = [
    path(
        "",
        include(
            "apps.patient_management.emergency_contacts.api.urls.emergency_contact",
        ),
    ),
]

__all__ = [
    "urlpatterns",
    "app_name",
]
