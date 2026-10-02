"""
Allergy API URLs.
"""

from django.urls import path

from apps.clinical.allergies.api.views import (
    AllergyListCreateAPIView,
    AllergyRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        AllergyListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:allergy_id>/",
        AllergyRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "urlpatterns",
]
