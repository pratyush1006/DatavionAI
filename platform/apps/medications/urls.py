"""
Medication URL configuration.
"""

from django.urls import include, path

app_name = "medications"

urlpatterns = [
    path(
        "",
        include("apps.medications.api.urls"),
    ),
]
