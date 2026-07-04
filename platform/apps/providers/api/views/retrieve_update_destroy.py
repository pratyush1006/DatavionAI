"""
API views for retrieving, updating, and deleting providers.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.providers.api.serializers import (
    ProviderDetailSerializer,
    ProviderUpdateSerializer,
)
from apps.providers.permissions import (
    CanDeleteProvider,
    CanUpdateProvider,
    CanViewProvider,
)
from apps.providers.selectors import get_provider_by_id
from apps.providers.services import (
    delete_provider,
    update_provider,
)

PROVIDER_TAG: Final[tuple[str, ...]] = ("Providers",)


@extend_schema(tags=PROVIDER_TAG)
class ProviderRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a provider.
    """

    lookup_url_kwarg = "provider_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewProvider,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateProvider,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateProvider,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteProvider,
        ),
    }

    serializer_classes = {
        "GET": ProviderDetailSerializer,
        "PUT": ProviderUpdateSerializer,
        "PATCH": ProviderUpdateSerializer,
    }

    detail_serializer_class = ProviderDetailSerializer

    update_service = update_provider

    delete_service = delete_provider

    update_success_message = "Provider updated successfully."

    def get_object(
        self,
    ):
        """
        Return the requested provider.
        """

        return get_provider_by_id(
            provider_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "ProviderRetrieveUpdateDestroyAPIView",
]
