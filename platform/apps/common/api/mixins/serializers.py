"""
Serializer-related API mixins.
"""

from __future__ import annotations

from django.core.exceptions import ImproperlyConfigured
from rest_framework.serializers import BaseSerializer


class SerializerMapMixin:
    """
    Provide serializer classes for CRUD operations.
    """

    list_serializer_class: type[BaseSerializer] | None = None
    detail_serializer_class: type[BaseSerializer] | None = None
    create_serializer_class: type[BaseSerializer] | None = None
    update_serializer_class: type[BaseSerializer] | None = None

    @staticmethod
    def _require(
        serializer: type[BaseSerializer] | None,
        attribute: str,
    ) -> type[BaseSerializer]:
        """
        Ensure a serializer class has been configured.
        """

        if serializer is None:
            raise ImproperlyConfigured(f"{attribute} must be configured.")

        return serializer

    def get_list_serializer_class(
        self,
    ) -> type[BaseSerializer]:
        """
        Return serializer used for list endpoints.
        """

        return self._require(
            self.list_serializer_class,
            "list_serializer_class",
        )

    def get_detail_serializer_class(
        self,
    ) -> type[BaseSerializer]:
        """
        Return serializer used for retrieve endpoints.
        """

        return self._require(
            self.detail_serializer_class,
            "detail_serializer_class",
        )

    def get_create_serializer_class(
        self,
    ) -> type[BaseSerializer]:
        """
        Return serializer used for create endpoints.
        """

        return self._require(
            self.create_serializer_class,
            "create_serializer_class",
        )

    def get_update_serializer_class(
        self,
    ) -> type[BaseSerializer]:
        """
        Return serializer used for update endpoints.
        """

        return self._require(
            self.update_serializer_class,
            "update_serializer_class",
        )

    def get_serializer_class(
        self,
    ) -> type[BaseSerializer]:
        """
        Automatically resolve the serializer based on the HTTP method.
        """

        if self.request.method == "GET":
            if (
                getattr(
                    self,
                    "action",
                    None,
                )
                == "list"
            ):
                return self.get_list_serializer_class()

            return self.get_detail_serializer_class()

        if self.request.method == "POST":
            return self.get_create_serializer_class()

        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return self.get_update_serializer_class()

        return super().get_serializer_class()


__all__ = [
    "SerializerMapMixin",
]
