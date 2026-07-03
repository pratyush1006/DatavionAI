"""
Base generic API views used across the Datavion AI platform.
"""

from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from apps.common.api.pagination import DatavionPagination
from apps.common.api.responses import (
    created_response,
    error_response,
    no_content_response,
    success_response,
)


class BaseAPIViewMixin:
    """
    Common defaults shared by all API views.
    """

    permission_classes = (IsAuthenticated,)

    pagination_class = DatavionPagination

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    def get_permissions(
        self,
    ):
        """
        Return permissions for the current HTTP method.
        """

        permission_classes = getattr(
            self,
            "permission_classes_map",
            {},
        ).get(
            self.request.method,
            self.permission_classes,
        )

        return [permission() for permission in permission_classes]

    def get_serializer_class(
        self,
    ):
        """
        Return serializer for the current HTTP method.
        """

        serializer_classes = getattr(
            self,
            "serializer_classes",
            None,
        )

        if serializer_classes:
            serializer = serializer_classes.get(
                self.request.method,
            )

            if serializer is not None:
                return serializer

        return super().get_serializer_class()

    def success_response(
        self,
        **kwargs,
    ):
        """
        Return a standardized success response.
        """

        return success_response(
            **kwargs,
        )

    def created_response(
        self,
        **kwargs,
    ):
        """
        Return a standardized created response.
        """

        return created_response(
            **kwargs,
        )

    def error_response(
        self,
        **kwargs,
    ):
        """
        Return a standardized error response.
        """

        return error_response(
            **kwargs,
        )

    def no_content_response(
        self,
    ):
        """
        Return a standardized no-content response.
        """

        return no_content_response()


class BaseListCreateAPIView(
    BaseAPIViewMixin,
    ListCreateAPIView,
):
    """
    Base class for list/create endpoints.
    """


class BaseRetrieveUpdateDestroyAPIView(
    BaseAPIViewMixin,
    RetrieveUpdateDestroyAPIView,
):
    """
    Base class for retrieve/update/delete endpoints.
    """


__all__ = [
    "BaseListCreateAPIView",
    "BaseRetrieveUpdateDestroyAPIView",
]
