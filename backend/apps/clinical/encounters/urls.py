"""
Encounter URL configuration.
"""

from django.urls import include, path

urlpatterns = [
    path(
        "",
        include(
            (
                "apps.clinical.encounters.api.urls",
                "encounters",
            ),
            namespace="encounters",
        ),
    ),
]
