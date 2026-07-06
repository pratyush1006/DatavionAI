"""
Allergy URL configuration.
"""

from django.urls import include, path

app_name = "allergies"

urlpatterns = [
    path(
        "",
        include("apps.allergies.api.urls"),
    ),
]

__all__ = [
    "urlpatterns",
]
