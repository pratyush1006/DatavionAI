"""
Base generic API views used across the Datavion AI platform.
"""

from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from apps.common.api.mixins.services import (
    CreateServiceMixin,
    DestroyServiceMixin,
    UpdateServiceMixin,
)
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

    @property
    def current_user(
        self,
    ):
        """
        Return the authenticated user.
        """

        return self.request.user

    def get_permissions(
        self,
    ) -> list[BasePermission]:
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
    ) -> type[Serializer]:
        """
        Return the serializer class for the current request.

        Resolution order:

        1. Action-specific serializer attributes
        2. serializer_classes mapping
        3. serializer_class
        4. DRF default implementation
        """

        method = self.request.method

        #
        # GET
        #
        if method == "GET":
            if isinstance(
                self,
                ListCreateAPIView,
            ) and hasattr(
                self,
                "list_serializer_class",
            ):
                serializer = self.list_serializer_class

                if serializer is not None:
                    return serializer

            if isinstance(
                self,
                RetrieveUpdateDestroyAPIView,
            ) and hasattr(
                self,
                "detail_serializer_class",
            ):
                serializer = self.detail_serializer_class

                if serializer is not None:
                    return serializer

        #
        # POST
        #
        elif method == "POST":
            serializer = getattr(
                self,
                "create_serializer_class",
                None,
            )

            if serializer is not None:
                return serializer

        #
        # PUT / PATCH
        #
        elif method in (
            "PUT",
            "PATCH",
        ):
            serializer = getattr(
                self,
                "update_serializer_class",
                None,
            )

            if serializer is not None:
                return serializer

        #
        # serializer_classes mapping
        #
        serializer_classes = getattr(
            self,
            "serializer_classes",
            None,
        )

        if serializer_classes:
            serializer = serializer_classes.get(
                method,
            )

            if serializer is not None:
                return serializer

            #
            # Schema generation fallback.
            #
            serializer = serializer_classes.get(
                "GET",
            )

            if serializer is None:
                serializer = next(
                    iter(
                        serializer_classes.values(),
                    ),
                    None,
                )

            if serializer is not None:
                return serializer

        #
        # Single serializer
        #
        serializer = getattr(
            self,
            "serializer_class",
            None,
        )

        if serializer is not None:
            return serializer

        return super().get_serializer_class()


class BaseGenericAPIView(
    BaseAPIViewMixin,
    GenericAPIView,
):
    """
    Base class shared by all generic API views.
    """

    def success_response(
        self,
        **kwargs,
    ) -> Response:
        """
        Return a standardized success response.
        """

        return success_response(
            **kwargs,
        )

    def created_response(
        self,
        **kwargs,
    ) -> Response:
        """
        Return a standardized created response.
        """

        return created_response(
            **kwargs,
        )

    def error_response(
        self,
        **kwargs,
    ) -> Response:
        """
        Return a standardized error response.
        """

        return error_response(
            **kwargs,
        )

    def no_content_response(
        self,
    ) -> Response:
        """
        Return a standardized no-content response.
        """

        return no_content_response()


class BaseListCreateAPIView(
    CreateServiceMixin,
    BaseGenericAPIView,
    ListCreateAPIView,
):
    """
    Base class for list/create endpoints.
    """


class BaseRetrieveUpdateDestroyAPIView(
    UpdateServiceMixin,
    DestroyServiceMixin,
    BaseGenericAPIView,
    RetrieveUpdateDestroyAPIView,
):
    """
    Base class for retrieve/update/delete endpoints.
    """


__all__ = [
    "BaseGenericAPIView",
    "BaseListCreateAPIView",
    "BaseRetrieveUpdateDestroyAPIView",
]
