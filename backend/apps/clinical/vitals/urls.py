"""
Vital URL configuration.
"""

from django.urls import include, path

app_name = "vitals"

urlpatterns = [
    path(
        "",
        include("apps.clinical.vitals.api.urls"),
    ),
]
