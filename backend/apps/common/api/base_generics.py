"""
Base generic API views used across the DatavionOS platform.

Provides enterprise API foundations:

- Authentication defaults
- Permission handling
- Object-level permissions
- Tenant context
- Organization context
- Filtering
- Searching
- Ordering
- Pagination
- Dynamic serializers
- Standardized responses
- Service-layer integration
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, ClassVar, Final

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from apps.common.api.filters import (
    DatavionFilterBackend,
    DatavionOrderingFilter,
    DatavionSearchFilter,
)
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
from apps.common.permissions import IsAuthenticatedAndActive

HTTP_GET: Final[str] = "GET"

HTTP_POST: Final[str] = "POST"

HTTP_PUT: Final[str] = "PUT"

HTTP_PATCH: Final[str] = "PATCH"


class BaseAPIViewMixin:
    """
    Common defaults shared by all DatavionOS API views.

    Every API endpoint automatically receives:

    - Authentication
    - Permission handling
    - Object permission handling
    - Filtering
    - Searching
    - Ordering
    - Pagination
    - Tenant context
    - Organization context
    """

    permission_classes: ClassVar[tuple[type[BasePermission], ...]] = (
        IsAuthenticatedAndActive,
    )

    pagination_class: ClassVar[type[DatavionPagination]] = DatavionPagination

    filter_backends: ClassVar[tuple[type[Any], ...]] = (
        DatavionFilterBackend,
        DatavionSearchFilter,
        DatavionOrderingFilter,
    )

    permission_classes_map: ClassVar[
        dict[
            str,
            tuple[type[BasePermission], ...],
        ]
    ] = {}

    list_serializer_class: ClassVar[type[Serializer] | None] = None

    detail_serializer_class: ClassVar[type[Serializer] | None] = None

    create_serializer_class: ClassVar[type[Serializer] | None] = None

    update_serializer_class: ClassVar[type[Serializer] | None] = None

    serializer_classes: ClassVar[dict[str, type[Serializer]] | None] = None

    selector: ClassVar[Callable[..., Any] | None] = None

    @property
    def current_user(
        self,
    ) -> AbstractBaseUser | AnonymousUser:
        """
        Return authenticated user.
        """

        return getattr(
            self.request,
            "user",
            AnonymousUser(),
        )

    @property
    def current_tenant(
        self,
    ):
        """
        Return current tenant context.
        """

        return getattr(
            self.request,
            "tenant",
            None,
        )

    @property
    def current_organization(
        self,
    ):
        """
        Return current organization context.
        """

        return getattr(
            self.request,
            "organization",
            None,
        )

    def get_permissions(
        self,
    ) -> list[BasePermission]:
        """
        Return permission instances.

        Supports HTTP method based permissions.
        """

        permission_classes = self.permission_classes_map.get(
            self.request.method,
            self.permission_classes,
        )

        return [permission() for permission in permission_classes]

    def check_object_permissions(
        self,
        obj: Any,
    ) -> None:
        """
        Execute object-level permissions.

        Required because DatavionOS uses
        selector-based object retrieval instead
        of always relying on DRF get_object().
        """

        for permission in self.get_permissions():
            if hasattr(
                permission,
                "has_object_permission",
            ):
                allowed = permission.has_object_permission(
                    self.request,
                    self,
                    obj,
                )

                if not allowed:
                    raise PermissionDenied(
                        detail=("You do not have permission to access this resource."),
                    )

    def _get_action_serializer(
        self,
    ) -> type[Serializer] | None:
        """
        Resolve serializer based on HTTP action.
        """

        method = self.request.method

        if method == HTTP_GET:
            lookup = getattr(
                self,
                "lookup_url_kwarg",
                None,
            )

            if (
                lookup is not None
                and lookup in self.kwargs
                and self.detail_serializer_class is not None
            ):
                return self.detail_serializer_class

            return self.list_serializer_class

        if method == HTTP_POST:
            return self.create_serializer_class

        if method in (
            HTTP_PUT,
            HTTP_PATCH,
        ):
            return self.update_serializer_class

        return None

    def _get_mapping_serializer(
        self,
    ) -> type[Serializer] | None:
        """
        Resolve serializer from mapping.
        """

        if not self.serializer_classes:
            return None

        return (
            self.serializer_classes.get(
                self.request.method,
            )
            or self.serializer_classes.get(
                HTTP_GET,
            )
            or next(
                iter(
                    self.serializer_classes.values(),
                ),
                None,
            )
        )

    def _resolve_serializer_class(
        self,
    ) -> type[Serializer] | None:
        """
        Resolve serializer class.
        """

        return (
            self._get_action_serializer()
            or self._get_mapping_serializer()
            or getattr(
                self,
                "serializer_class",
                None,
            )
        )

    def get_serializer_class(
        self,
    ) -> type[Serializer]:
        """
        Return serializer class.
        """

        serializer = self._resolve_serializer_class()

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
        **kwargs: Any,
    ) -> Response:
        return success_response(
            request=self.request,
            **kwargs,
        )

    def created_response(
        self,
        **kwargs: Any,
    ) -> Response:
        return created_response(
            request=self.request,
            **kwargs,
        )

    def error_response(
        self,
        **kwargs: Any,
    ) -> Response:
        return error_response(
            request=self.request,
            **kwargs,
        )

    def no_content_response(
        self,
    ) -> Response:
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

    def get_object(
        self,
    ):
        """
        Retrieve object and enforce object permissions.
        """

        obj = super().get_object()

        self.check_object_permissions(
            obj,
        )

        return obj


__all__: tuple[str, ...] = (
    "BaseGenericAPIView",
    "BaseListCreateAPIView",
    "BaseRetrieveUpdateDestroyAPIView",
)
