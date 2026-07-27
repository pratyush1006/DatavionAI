"""
API views for retrieving, updating, and deleting providers.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.clinical.providers.api.serializers import (
    ProviderDetailSerializer,
    ProviderUpdateSerializer,
)
from apps.clinical.providers.permissions import (
    CanDeleteProvider,
    CanUpdateProvider,
    CanViewProvider,
)
from apps.clinical.providers.selectors import (
    ProviderSelector,
)
from apps.clinical.providers.services import (
    ProviderService,
)
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
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

    update_service = ProviderService.update

    delete_service = ProviderService.delete

    update_success_message = "Provider updated successfully."

    def get_object(
        self,
    ):
        """
        Return the requested provider.
        """

        return ProviderSelector.get(
            provider_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "ProviderRetrieveUpdateDestroyAPIView",
]
