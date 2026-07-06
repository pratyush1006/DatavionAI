"""
Vital URL configuration.
"""

from django.urls import include, path

app_name = "vitals"

urlpatterns = [
    path(
        "",
        include("apps.vitals.api.urls"),
    ),
]
