"""
Reusable service mixins for the Datavion AI platform.

These mixins connect DRF generic views with the application's
service layer while keeping business logic outside the API layer.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from django.core.exceptions import ImproperlyConfigured
from rest_framework.serializers import BaseSerializer

type Service = Callable[..., Any]


class BaseServiceMixin:
    """
    Base mixin for invoking application services.
    """

    create_service: Service | None = None

    update_service: Service | None = None

    delete_service: Service | None = None

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

    @staticmethod
    def _require_service(
        service: Service | None,
        *,
        name: str,
    ) -> Service:
        """
        Return the configured service or raise an error.
        """

        if service is None:
            raise ImproperlyConfigured(
                f"{name} must be configured.",
            )

        return service


class CreateServiceMixin(
    BaseServiceMixin,
):
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

        service = self._require_service(
            self.create_service,
            name="create_service",
        )

        serializer.instance = service(
            **self.get_create_service_kwargs(
                serializer,
            ),
        )


class UpdateServiceMixin(
    BaseServiceMixin,
):
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

        service = self._require_service(
            self.update_service,
            name="update_service",
        )

        serializer.instance = service(
            **self.get_update_service_kwargs(
                serializer,
            ),
        )


class DestroyServiceMixin(
    BaseServiceMixin,
):
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

        service = self._require_service(
            self.delete_service,
            name="delete_service",
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
