"""Compliance API views."""

from __future__ import annotations

from typing import Any

from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.compliance.api.serializers import ConsentSerializer, PhiAccessLogSerializer
from apps.compliance.models import Consent, PhiAccessLog


class ConsentListCreateAPIView(BaseListCreateAPIView):
    """List and create consent records inside the current organization."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ConsentSerializer
    queryset = Consent.objects.none()
    search_fields = ("patient__mrn", "patient__first_name", "patient__last_name")
    ordering = ("-created_at",)
    ordering_fields = ("created_at", "status", "purpose")

    def get_queryset(self) -> QuerySet[Consent]:
        organization = getattr(self.request, "organization", None)
        if organization is None:
            return Consent.objects.none()
        return Consent.objects.filter(organization=organization).select_related(
            "patient",
            "organization",
        )

    def perform_create(self, serializer: ConsentSerializer) -> None:
        organization = getattr(self.request, "organization", None)
        if organization is None:
            raise ValueError("Organization context is required.")
        serializer.save(organization=organization)


class ConsentDetailAPIView(BaseRetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete an organization-scoped consent."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ConsentSerializer
    queryset = Consent.objects.none()
    lookup_url_kwarg = "consent_id"

    def get_queryset(self) -> QuerySet[Consent]:
        organization = getattr(self.request, "organization", None)
        if organization is None:
            return Consent.objects.none()
        return Consent.objects.filter(organization=organization)


class PhiAccessLogListAPIView(BaseListCreateAPIView):
    """Read PHI access audit records for the current organization."""

    permission_classes = (IsAuthenticated,)
    serializer_class = PhiAccessLogSerializer
    queryset = PhiAccessLog.objects.none()
    http_method_names = ["get", "head", "options"]
    search_fields = ("resource_type", "resource_id", "patient__mrn")
    ordering = ("-created_at",)
    ordering_fields = ("created_at", "action")

    def get_queryset(self) -> QuerySet[PhiAccessLog]:
        organization = getattr(self.request, "organization", None)
        if organization is None:
            return PhiAccessLog.objects.none()
        return PhiAccessLog.objects.filter(organization=organization).select_related(
            "actor",
            "patient",
        )

    def create(
        self, request: Any, *args: Any, **kwargs: Any
    ):  # pragma: no cover - method blocked by http_method_names
        return self.http_method_not_allowed(request, *args, **kwargs)


__all__ = [
    "ConsentDetailAPIView",
    "ConsentListCreateAPIView",
    "PhiAccessLogListAPIView",
]
