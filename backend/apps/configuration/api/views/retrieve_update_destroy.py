"""
API views for retrieving, updating, and deleting configurations.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.api.base_generics import BaseRetrieveUpdateDestroyAPIView
from apps.configuration.api.serializers.detail import (
    ConfigurationDetailSerializer,
)
from apps.configuration.api.serializers.update import (
    UpdateConfigurationSerializer,
)
from apps.configuration.selectors.configuration import (
    get_configuration_by_key,
)
from apps.configuration.services.configuration import (
    delete_configuration,
    update_configuration,
)


@extend_schema(tags=["Configuration"])
class ConfigurationRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, and delete configurations.
    """

    permission_classes = (IsAuthenticated,)

    lookup_field = "key"

    def get_object(self):
        """
        Return the requested configuration.
        """

        return get_configuration_by_key(
            key=self.kwargs[self.lookup_field],
        )

    def get_serializer_class(self):
        """
        Return the serializer for the current request.
        """

        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return UpdateConfigurationSerializer

        return ConfigurationDetailSerializer

    def update(self, request, *args, **kwargs):
        """
        Update a configuration.
        """

        configuration = self.get_object()

        serializer = self.get_serializer(
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        configuration = update_configuration(
            configuration=configuration,
            **serializer.validated_data,
        )

        response_serializer = ConfigurationDetailSerializer(
            configuration,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a configuration.
        """

        configuration = self.get_object()

        delete_configuration(
            configuration=configuration,
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
