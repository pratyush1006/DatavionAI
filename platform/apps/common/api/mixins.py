"""
Reusable mixins for Datavion API views.

These mixins remove duplicated CRUD boilerplate while keeping
business logic inside services and read operations inside selectors.

Responsibilities
----------------
PermissionMapMixin
    Select permissions based on HTTP method.

SerializerMapMixin
    Select serializer based on HTTP method.

SelectorMixin
    Delegate queryset and object retrieval to selectors.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from rest_framework.permissions import BasePermission
from rest_framework.serializers import BaseSerializer


class PermissionMapMixin:
    """
    Map HTTP methods to permission classes.

    Example:
        permission_map = {
            "GET": (
                IsAuthenticated,
                CanViewOrganizations,
            ),
            "POST": (
                IsAuthenticated,
                CanAddOrganizations,
            ),
        }
    """

    permission_map: dict[
        str,
        tuple[type[BasePermission], ...],
    ] = {}

    def get_permissions(self) -> list[BasePermission]:
        """
        Return instantiated permission classes for the current request.
        """

        permission_classes = self.permission_map.get(
            self.request.method,
            (),
        )

        return [permission() for permission in permission_classes]


class SerializerMapMixin:
    """
    Provide serializer classes for CRUD operations.
    """

    list_serializer_class: type[BaseSerializer] | None = None
    detail_serializer_class: type[BaseSerializer] | None = None
    create_serializer_class: type[BaseSerializer] | None = None
    update_serializer_class: type[BaseSerializer] | None = None

    def get_list_serializer_class(
        self,
    ) -> type[BaseSerializer]:
        """
        Return the serializer used for list endpoints.
        """

        if self.list_serializer_class is None:
            raise ImproperlyConfigured("list_serializer_class must be configured.")

        return self.list_serializer_class

    def get_detail_serializer_class(
        self,
    ) -> type[BaseSerializer]:
        """
        Return the serializer used for detail endpoints.
        """

        if self.detail_serializer_class is None:
            raise ImproperlyConfigured("detail_serializer_class must be configured.")

        return self.detail_serializer_class

    def get_create_serializer_class(
        self,
    ) -> type[BaseSerializer]:
        """
        Return the serializer used for create endpoints.
        """

        if self.create_serializer_class is None:
            raise ImproperlyConfigured("create_serializer_class must be configured.")

        return self.create_serializer_class

    def get_update_serializer_class(
        self,
    ) -> type[BaseSerializer]:
        """
        Return the serializer used for update endpoints.
        """

        if self.update_serializer_class is None:
            raise ImproperlyConfigured("update_serializer_class must be configured.")

        return self.update_serializer_class


class SelectorMixin:
    """
    Delegate read operations to selector functions.
    """

    queryset_selector: (
        Callable[
            ...,
            QuerySet[Any],
        ]
        | None
    ) = None

    lookup_selector: (
        Callable[
            [Any],
            Any,
        ]
        | None
    ) = None

    lookup_url_kwarg: str = "pk"

    def get_queryset(self) -> QuerySet[Any]:
        """
        Return the queryset provided by the configured selector.
        """

        if self.queryset_selector is None:
            raise ImproperlyConfigured("queryset_selector must be configured.")

        return self.queryset_selector()

    def get_object(self) -> Any:
        """
        Return an object using the configured lookup selector.
        """

        if self.lookup_selector is None:
            raise ImproperlyConfigured("lookup_selector must be configured.")

        lookup_value = self.kwargs[self.lookup_url_kwarg]

        return self.lookup_selector(
            lookup_value,
        )
