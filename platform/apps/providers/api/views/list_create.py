"""
API views for listing and creating providers.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.providers.api.serializers import (
    ProviderCreateSerializer,
    ProviderDetailSerializer,
    ProviderListSerializer,
)
from apps.providers.models import Provider
from apps.providers.permissions import (
    CanCreateProvider,
    CanViewProvider,
)
from apps.providers.selectors import get_providers
from apps.providers.services import create_provider

PROVIDER_TAG: Final[tuple[str, ...]] = ("Providers",)


@extend_schema(tags=PROVIDER_TAG)
class ProviderListCreateAPIView(BaseListCreateAPIView):
    """
    List existing providers or create a new provider.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewProvider,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateProvider,
        ),
    }

    serializer_classes = {
        "GET": ProviderListSerializer,
        "POST": ProviderCreateSerializer,
    }

    detail_serializer_class = ProviderDetailSerializer

    create_service = create_provider

    create_success_message = "Provider created successfully."

    search_fields = (
        "provider_number",
        "license_number",
        "employee__first_name",
        "employee__last_name",
    )

    ordering = ("provider_number",)

    ordering_fields = (
        "provider_number",
        "provider_type",
        "created_at",
    )

    filterset_fields = (
        "provider_type",
        "status",
        "is_accepting_patients",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Provider]:
        """
        Return the providers queryset.
        """

        return get_providers()


__all__ = [
    "ProviderListCreateAPIView",
]
