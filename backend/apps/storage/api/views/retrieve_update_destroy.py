"""
API views for retrieving, updating, and deleting storage assets.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.storage.api.serializers.detail import (
    AssetDetailSerializer,
)
from apps.storage.api.serializers.update import (
    UpdateAssetSerializer,
)
from apps.storage.selectors.asset import (
    get_asset,
)
from apps.storage.services.asset import (
    update_asset,
)
from apps.storage.services.delete import (
    delete_asset,
)


@extend_schema(tags=["Storage"])
class AssetRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, and delete storage assets.
    """

    permission_classes = (IsAuthenticated,)

    lookup_url_kwarg = "pk"

    def get_object(self):
        """
        Return the requested asset.
        """

        return get_asset(
            asset_id=self.kwargs[self.lookup_url_kwarg],
            organization=self.request.user.organization,
        )

    def get_serializer_class(self):
        """
        Return the serializer for the current request.
        """

        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return UpdateAssetSerializer

        return AssetDetailSerializer

    def retrieve(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Retrieve an asset.
        """

        asset = self.get_object()

        serializer = AssetDetailSerializer(
            asset,
            context=self.get_serializer_context(),
        )

        return self.success_response(
            data=serializer.data,
            message="Asset retrieved successfully.",
        )

    def update(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Update asset metadata.
        """

        asset = self.get_object()

        serializer = self.get_serializer(
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        asset = update_asset(
            asset=asset,
            **serializer.validated_data,
        )

        response_serializer = AssetDetailSerializer(
            asset,
            context=self.get_serializer_context(),
        )

        return self.success_response(
            data=response_serializer.data,
            message="Asset updated successfully.",
        )

    def destroy(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Delete an asset.
        """

        asset = self.get_object()

        delete_asset(
            asset=asset,
        )

        return self.no_content_response()


__all__ = [
    "AssetRetrieveUpdateDestroyAPIView",
]
