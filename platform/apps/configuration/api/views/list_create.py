"""
API views for listing and creating configurations.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.configuration.api.serializers.create import (
    CreateConfigurationSerializer,
)
from apps.configuration.api.serializers.detail import (
    ConfigurationDetailSerializer,
)
from apps.configuration.api.serializers.list import (
    ConfigurationListSerializer,
)
from apps.configuration.selectors.configuration import (
    get_configurations,
)
from apps.configuration.services.configuration import (
    create_configuration,
)


@extend_schema(tags=["Configuration"])
class ConfigurationListCreateAPIView(BaseListCreateAPIView):
    """
    List and create configurations.
    """

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Return all active configurations.
        """

        return get_configurations()

    def get_serializer_class(self):
        """
        Return the serializer for the current request.
        """

        if self.request.method == "POST":
            return CreateConfigurationSerializer

        return ConfigurationListSerializer

    def perform_create(self, serializer):
        """
        Create a configuration.
        """

        return create_configuration(
            **serializer.validated_data,
        )

    def create(self, request, *args, **kwargs):
        """
        Create a configuration.
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        configuration = self.perform_create(
            serializer,
        )

        response_serializer = ConfigurationDetailSerializer(
            configuration,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
