from django.urls import path

from apps.organizations.api.views import (
    OrganizationListCreateAPIView,
    OrganizationRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        OrganizationListCreateAPIView.as_view(),
        name="organization-list-create",
    ),
    path(
        "<int:organization_id>/",
        OrganizationRetrieveUpdateDestroyAPIView.as_view(),
        name="organization-detail",
    ),
]
