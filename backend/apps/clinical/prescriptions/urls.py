"""
Prescription URL configuration.
"""

from django.urls import include, path

app_name = "prescriptions"

urlpatterns = [
    path(
        "",
        include("apps.clinical.prescriptions.api.urls"),
    ),
]
