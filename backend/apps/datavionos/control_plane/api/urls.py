from __future__ import annotations

from django.urls import path

from apps.datavionos.control_plane.api.views import (
    OrganizationControlPlaneAPIView,
    OrganizationFeatureToggleAPIView,
    OrganizationModuleToggleAPIView,
)

app_name = "organization-control-plane"

urlpatterns = [
    path("", OrganizationControlPlaneAPIView.as_view(), name="snapshot"),
    path(
        "modules/<uuid:module_id>/",
        OrganizationModuleToggleAPIView.as_view(),
        name="module-toggle",
    ),
    path(
        "features/<uuid:feature_id>/",
        OrganizationFeatureToggleAPIView.as_view(),
        name="feature-toggle",
    ),
]
