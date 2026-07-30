"""
Reusable service mixins for the DatavionOS platform.

Connects DRF generic views with application
service layers and workflow orchestration.

Responsibilities:

- Service execution
- Workflow execution delegation
- Request context injection
- Tenant propagation
- Organization propagation
- Lifecycle hooks
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from django.core.exceptions import ImproperlyConfigured
from rest_framework.serializers import BaseSerializer

type Service = Callable[..., Any]


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
        Hook executed before create.
        """

    def after_create(
        self,
        instance: Any,
        serializer: BaseSerializer,
    ) -> None:
        """
        Hook executed after create.
        """

    def before_update(
        self,
        serializer: BaseSerializer,
    ) -> None:
        """
        Hook executed before update.
        """

    def after_update(
        self,
        instance: Any,
        serializer: BaseSerializer,
    ) -> None:
        """
        Hook executed after update.
        """

    def before_destroy(
        self,
        instance: Any,
    ) -> None:
        """
        Hook executed before destroy.
        """

    def after_destroy(
        self,
        instance: Any,
    ) -> None:
        """
        Hook executed after destroy.
        """

    # ==========================================================
    # Service arguments
    # ==========================================================

    def get_create_service_kwargs(
        self,
        serializer: BaseSerializer,
    ) -> dict[str, Any]:
        """
        Build create service arguments.
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
        Build update service arguments.
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
        Build delete service arguments.
        """

        return {
            "instance": instance,
            **self.get_service_context(),
        }


class CreateServiceMixin(
    BaseServiceMixin,
):
    """
    Execute create operations.

    Supports:

    - Workflow execution
    - Service execution
    """

    def perform_create(
        self,
        serializer: BaseSerializer,
    ) -> None:

        self.before_create(
            serializer,
        )

        if (
            hasattr(
                self,
                "has_create_workflow",
            )
            and self.has_create_workflow()
        ):
            self.perform_workflow_create(
                serializer,
            )

            self.after_create(
                serializer.instance,
                serializer,
            )

            return

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
    Execute update operations.

    Supports:

    - Workflow execution
    - Service execution
    """

    def perform_update(
        self,
        serializer: BaseSerializer,
    ) -> None:

        self.before_update(
            serializer,
        )

        if (
            hasattr(
                self,
                "has_update_workflow",
            )
            and self.has_update_workflow()
        ):
            self.perform_workflow_update(
                serializer,
            )

            self.after_update(
                serializer.instance,
                serializer,
            )

            return

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
    Execute delete operations.

    Supports:

    - Workflow execution
    - Service execution
    """

    def perform_destroy(
        self,
        instance: Any,
    ) -> None:

        self.before_destroy(
            instance,
        )

        if (
            hasattr(
                self,
                "has_delete_workflow",
            )
            and self.has_delete_workflow()
        ):
            self.perform_workflow_destroy(
                instance,
            )

            self.after_destroy(
                instance,
            )

            return

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
    "UpdateServiceMixin",
    "DestroyServiceMixin",
)
