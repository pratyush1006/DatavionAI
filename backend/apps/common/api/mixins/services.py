"""
Reusable service mixins for the DatavionOS platform.

Connects DRF generic views with application
service layers.

Responsibilities:

- Service execution
- Request context injection
- Tenant propagation
- Organization propagation
- Lifecycle hooks
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeAlias

from django.core.exceptions import ImproperlyConfigured
from rest_framework.serializers import BaseSerializer

Service: TypeAlias = Callable[..., Any]


class BaseServiceMixin:
    """
    Base service execution mixin.
    """

    create_service: Service | None = None
    update_service: Service | None = None
    delete_service: Service | None = None

    @staticmethod
    def _require_service(
        service: Service | None,
        *,
        name: str,
    ) -> Service:
        """
        Validate service configuration.
        """

        if service is None:
            raise ImproperlyConfigured(
                f"'{name}' must be configured.",
            )

        return service

    @staticmethod
    def _execute_service(
        service: Service,
        **kwargs: Any,
    ) -> Any:
        """
        Execute configured service.
        """

        return service(
            **kwargs,
        )

    def get_service_context(
        self,
    ) -> dict[str, Any]:
        """
        Return common DatavionOS request context.
        """

        request = getattr(
            self,
            "request",
            None,
        )

        return {
            "request_user": getattr(
                request,
                "user",
                None,
            ),
            "tenant": getattr(
                request,
                "tenant",
                None,
            ),
            "organization": getattr(
                request,
                "organization",
                None,
            ),
        }

    # ==========================================================
    # Lifecycle hooks
    # ==========================================================

    def before_create(
        self,
        serializer: BaseSerializer,
    ) -> None:
        """
        Hook executed before create service.
        """

    def after_create(
        self,
        instance: Any,
        serializer: BaseSerializer,
    ) -> None:
        """
        Hook executed after create service.
        """

    def before_update(
        self,
        serializer: BaseSerializer,
    ) -> None:
        """
        Hook executed before update service.
        """

    def after_update(
        self,
        instance: Any,
        serializer: BaseSerializer,
    ) -> None:
        """
        Hook executed after update service.
        """

    def before_destroy(
        self,
        instance: Any,
    ) -> None:
        """
        Hook executed before delete service.
        """

    def after_destroy(
        self,
        instance: Any,
    ) -> None:
        """
        Hook executed after delete service.
        """

    # ==========================================================
    # Service arguments
    # ==========================================================

    def get_create_service_kwargs(
        self,
        serializer: BaseSerializer,
    ) -> dict[str, Any]:
        """
        Build arguments for create services.

        Standard service signature:

            create_xxx(
                *,
                validated_data,
                request_user,
                tenant,
                organization,
            )
        """

        return {
            "validated_data": serializer.validated_data,
            **self.get_service_context(),
        }

    def get_update_service_kwargs(
        self,
        serializer: BaseSerializer,
    ) -> dict[str, Any]:
        """
        Build arguments for update services.

        Standard service signature:

            update_xxx(
                *,
                instance,
                validated_data,
                request_user,
                tenant,
                organization,
            )
        """

        return {
            "instance": self.get_object(),
            "validated_data": serializer.validated_data,
            **self.get_service_context(),
        }

    def get_delete_service_kwargs(
        self,
        instance: Any,
    ) -> dict[str, Any]:
        """
        Build arguments for delete services.

        Standard service signature:

            delete_xxx(
                *,
                instance,
                request_user,
                tenant,
                organization,
            )
        """

        return {
            "instance": instance,
            **self.get_service_context(),
        }


class CreateServiceMixin(
    BaseServiceMixin,
):
    """
    Execute create operations using the configured service layer.
    """

    def perform_create(
        self,
        serializer: BaseSerializer,
    ) -> None:
        self.before_create(
            serializer,
        )

        service = self._require_service(
            type(self).create_service,
            name="create_service",
        )

        instance = self._execute_service(
            service,
            **self.get_create_service_kwargs(
                serializer,
            ),
        )

        serializer.instance = instance

        self.after_create(
            instance,
            serializer,
        )


class UpdateServiceMixin(
    BaseServiceMixin,
):
    """
    Execute update operations using the configured service layer.
    """

    def perform_update(
        self,
        serializer: BaseSerializer,
    ) -> None:
        self.before_update(
            serializer,
        )

        service = self._require_service(
            type(self).update_service,
            name="update_service",
        )

        instance = self._execute_service(
            service,
            **self.get_update_service_kwargs(
                serializer,
            ),
        )

        serializer.instance = instance

        self.after_update(
            instance,
            serializer,
        )


class DestroyServiceMixin(
    BaseServiceMixin,
):
    """
    Execute delete operations using the configured service layer.
    """

    def perform_destroy(
        self,
        instance: Any,
    ) -> None:
        self.before_destroy(
            instance,
        )

        service = self._require_service(
            type(self).delete_service,
            name="delete_service",
        )

        self._execute_service(
            service,
            **self.get_delete_service_kwargs(
                instance,
            ),
        )

        self.after_destroy(
            instance,
        )


__all__: tuple[str, ...] = (
    "BaseServiceMixin",
    "CreateServiceMixin",
    "DestroyServiceMixin",
    "UpdateServiceMixin",
)
