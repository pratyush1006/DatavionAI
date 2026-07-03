"""
Reusable service mixins for Datavion AI.

These mixins connect DRF generic views with the application's
service layer while keeping business logic outside the views.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from django.core.exceptions import ImproperlyConfigured
from rest_framework.serializers import BaseSerializer


class BaseServiceMixin:
    """
    Base mixin for connecting API views with service functions.
    """

    create_service: Callable[..., Any] | None = None

    update_service: Callable[..., Any] | None = None

    delete_service: Callable[..., Any] | None = None

    def get_create_service_kwargs(
        self,
        serializer: BaseSerializer,
    ) -> dict[str, Any]:
        """
        Return keyword arguments passed to the create service.
        """

        return {
            "validated_data": serializer.validated_data,
        }

    def get_update_service_kwargs(
        self,
        serializer: BaseSerializer,
    ) -> dict[str, Any]:
        """
        Return keyword arguments passed to the update service.
        """

        return {
            "instance": self.get_object(),
            "validated_data": serializer.validated_data,
        }

    def get_delete_service_kwargs(
        self,
        instance: Any,
    ) -> dict[str, Any]:
        """
        Return keyword arguments passed to the delete service.
        """

        return {
            "instance": instance,
        }


class CreateServiceMixin(BaseServiceMixin):
    """
    Execute the configured create service.
    """

    def perform_create(
        self,
        serializer: BaseSerializer,
    ) -> None:
        """
        Create an object using the configured service.
        """

        service = type(self).create_service

        if service is None:
            raise ImproperlyConfigured(
                "create_service must be configured.",
            )

        service(
            **self.get_create_service_kwargs(
                serializer,
            ),
        )


class UpdateServiceMixin(BaseServiceMixin):
    """
    Execute the configured update service.
    """

    def perform_update(
        self,
        serializer: BaseSerializer,
    ) -> None:
        """
        Update an object using the configured service.
        """

        service = type(self).update_service

        if service is None:
            raise ImproperlyConfigured(
                "update_service must be configured.",
            )

        service(
            **self.get_update_service_kwargs(
                serializer,
            ),
        )


class DestroyServiceMixin(BaseServiceMixin):
    """
    Execute the configured delete service.
    """

    def perform_destroy(
        self,
        instance: Any,
    ) -> None:
        """
        Delete an object using the configured service.
        """

        service = type(self).delete_service

        if service is None:
            raise ImproperlyConfigured(
                "delete_service must be configured.",
            )

        service(
            **self.get_delete_service_kwargs(
                instance,
            ),
        )


__all__ = [
    "BaseServiceMixin",
    "CreateServiceMixin",
    "UpdateServiceMixin",
    "DestroyServiceMixin",
]
