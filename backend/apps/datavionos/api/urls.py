"""
Platform Core API URLs.

Canonical DatavionOS platform API boundary.
"""

from django.urls import path

from apps.datavionos.api.effective_context import (
    EffectiveCapabilityContextAPIView,
)
from apps.datavionos.api.views.bootstrap import (
    PlatformBootstrapAPIView,
)
from apps.datavionos.api.views.doctor_overview import DoctorOverviewAPIView
from apps.datavionos.api.views.organization_overview import OrganizationOverviewAPIView

app_name = "platform-core"

urlpatterns = [
    path(
        "bootstrap/",
        PlatformBootstrapAPIView.as_view(),
        name="bootstrap",
    ),
    path(
        "context/effective/",
        EffectiveCapabilityContextAPIView.as_view(),
        name="effective-capability-context",
    ),
    path("doctor-overview/", DoctorOverviewAPIView.as_view(), name="doctor-overview"),
    path(
        "organization-overview/",
        OrganizationOverviewAPIView.as_view(),
        name="organization-overview",
    ),
]
