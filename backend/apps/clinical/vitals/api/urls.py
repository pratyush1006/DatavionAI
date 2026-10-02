"""
Vital API URLs.
"""

from django.urls import path

from apps.clinical.vitals.api.views import (
    VitalListCreateAPIView,
    VitalRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        VitalListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:vital_id>/",
        VitalRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "urlpatterns",
]
