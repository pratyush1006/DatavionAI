"""
API views for listing and creating providers.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.clinical.providers.api.serializers import (
    ProviderCreateSerializer,
    ProviderDetailSerializer,
    ProviderListSerializer,
)
from apps.clinical.providers.models import Provider
from apps.clinical.providers.permissions import (
    CanCreateProvider,
    CanViewProvider,
)
from apps.clinical.providers.selectors import (
    ProviderSelector,
)
from apps.clinical.providers.services import (
    ProviderService,
)
from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)

PROVIDER_TAG: Final[tuple[str, ...]] = ("Providers",)


@extend_schema(tags=PROVIDER_TAG)
class ProviderListCreateAPIView(
    BaseListCreateAPIView,
):
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

    create_service = ProviderService.create

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
        Return the provider queryset.
        """

        return ProviderSelector.queryset()


__all__ = [
    "ProviderListCreateAPIView",
]
