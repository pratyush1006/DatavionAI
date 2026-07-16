"""
API views for listing and uploading storage assets.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.storage.api.serializers.create import CreateAssetSerializer
from apps.storage.api.serializers.detail import AssetDetailSerializer
from apps.storage.api.serializers.list import AssetListSerializer
from apps.storage.selectors.asset import (
    get_organization_assets,
)
from apps.storage.services.upload import (
    upload_asset,
)


@extend_schema(tags=["Storage"])
class AssetListCreateAPIView(BaseListCreateAPIView):
    """
    List and upload storage assets.
    """

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Return assets for the current organization.
        """

        return get_organization_assets(
            organization=self.request.user.organization,
        )

    def get_serializer_class(self):
        """
        Return the appropriate serializer.
        """

        if self.request.method == "POST":
            return CreateAssetSerializer

        return AssetListSerializer

    def perform_create(self, serializer):
        """
        Upload an asset.
        """

        return upload_asset(
            organization=self.request.user.organization,
            uploaded_by=self.request.user,
            file=serializer.validated_data["file"],
            original_name=serializer.validated_data["file"].name,
            mime_type=serializer.validated_data["file"].content_type,
            category=serializer.validated_data["category"],
            folder=serializer.validated_data.get("folder"),
            visibility=serializer.validated_data["visibility"],
        )

    def create(self, request, *args, **kwargs):
        """
        Upload an asset.
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        asset = self.perform_create(
            serializer,
        )

        response_serializer = AssetDetailSerializer(
            asset,
        )

        return Response(
            response_serializer.data,
            status=201,
        )
