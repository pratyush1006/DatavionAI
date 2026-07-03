"""
Reusable service mixins for Datavion AI.

These mixins connect DRF generic views with the application's
service layer while keeping business logic outside the views.
"""

from __future__ import annotations

from collections.abc import Callable

from rest_framework.serializers import BaseSerializer


class BaseServiceMixin:
    """
    Base mixin for connecting API views with service functions.
    """

    create_service: Callable | None = None
    update_service: Callable | None = None
    delete_service: Callable | None = None

    instance = None


class CreateServiceMixin(BaseServiceMixin):
    """
    Execute the configured create service.
    """

    def perform_create(
        self,
        serializer: BaseSerializer,
    ) -> None:
        """
        Create a new object using the configured service.
        """

        if self.create_service is None:
            raise NotImplementedError(
                "create_service must be configured.",
            )

        self.instance = self.create_service(
            validated_data=serializer.validated_data,
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
        Update an existing object using the configured service.
        """

        if self.update_service is None:
            raise NotImplementedError(
                "update_service must be configured.",
            )

        self.instance = self.update_service(
            instance=self.get_object(),
            validated_data=serializer.validated_data,
        )


class DestroyServiceMixin(BaseServiceMixin):
    """
    Execute the configured delete service.
    """

    def perform_destroy(
        self,
        instance,
    ) -> None:
        """
        Delete an object using the configured service.
        """

        if self.delete_service is None:
            raise NotImplementedError(
                "delete_service must be configured.",
            )

        self.delete_service(
            instance=instance,
        )


__all__ = [
    "BaseServiceMixin",
    "CreateServiceMixin",
    "UpdateServiceMixin",
    "DestroyServiceMixin",
]
