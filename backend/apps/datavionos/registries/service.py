"""
Service registry for DatavionOS.

This module manages platform services responsible for providing
business logic throughout the platform.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.datavionos.exceptions import RegistryError
from apps.datavionos.types import Identifier

from ..contracts.service import ServiceContract
from .registry import Registry


class ServiceRegistry(
    Registry[
        Identifier,
        ServiceContract,
    ],
):
    """
    Registry of platform services.

    Every business service is registered here before it becomes
    available through the DatavionOS runtime.
    """

    def __init__(self) -> None:
        super().__init__(
            name="services",
        )

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_service(
        self,
        service: ServiceContract,
    ) -> ServiceContract:
        """
        Register a service.
        """
        return self.register(
            key=service.identifier,
            value=service,
        )

    def register_services(
        self,
        services: Iterable[ServiceContract],
    ) -> None:
        """
        Register multiple services.
        """
        for service in services:
            self.register_service(
                service,
            )

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get_service(
        self,
        identifier: Identifier,
    ) -> ServiceContract | None:
        """
        Retrieve a service.
        """
        return self.get(
            identifier,
        )

    def require_service(
        self,
        identifier: Identifier,
    ) -> ServiceContract:
        """
        Retrieve a required service.
        """
        return self.require(
            identifier,
        )

    def unregister_service(
        self,
        identifier: Identifier,
    ) -> ServiceContract:
        """
        Remove a service.
        """
        return self.unregister(
            identifier,
        )

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def enabled_services(
        self,
    ) -> list[ServiceContract]:
        """
        Return enabled services.
        """
        return [service for service in self.values() if service.enabled]

    def disabled_services(
        self,
    ) -> list[ServiceContract]:
        """
        Return disabled services.
        """
        return [service for service in self.values() if not service.enabled]

    def singleton_services(
        self,
    ) -> list[ServiceContract]:
        """
        Return singleton services.
        """
        return [service for service in self.values() if service.singleton]

    def transient_services(
        self,
    ) -> list[ServiceContract]:
        """
        Return transient services.
        """
        return [service for service in self.values() if not service.singleton]

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate_registration(
        self,
        *,
        key: Identifier,
        value: ServiceContract,
    ) -> None:
        """
        Validate service registration.
        """
        super()._validate_registration(
            key=key,
            value=value,
        )

        if value.identifier != key:
            raise RegistryError(
                message=("Service identifier does not match registry key."),
                error_code="SERVICE_IDENTIFIER_MISMATCH",
            )

        if not value.name.strip():
            raise RegistryError(
                message="Service name cannot be empty.",
                error_code="SERVICE_NAME_REQUIRED",
            )

        if not value.version.strip():
            raise RegistryError(
                message="Service version cannot be empty.",
                error_code="SERVICE_VERSION_REQUIRED",
            )

        if self.exists(key):
            existing = self.require(key)

            if existing.version == value.version:
                raise RegistryError(
                    message=(
                        f"Service '{value.name}' "
                        f"version '{value.version}' "
                        "is already registered."
                    ),
                    error_code="SERVICE_ALREADY_REGISTERED",
                )

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @property
    def total_services(
        self,
    ) -> int:
        """
        Return the total number of registered services.
        """
        return self.size

    @property
    def total_enabled(
        self,
    ) -> int:
        """
        Return the number of enabled services.
        """
        return len(
            self.enabled_services(),
        )

    @property
    def total_disabled(
        self,
    ) -> int:
        """
        Return the number of disabled services.
        """
        return len(
            self.disabled_services(),
        )

    @property
    def total_singleton(
        self,
    ) -> int:
        """
        Return the number of singleton services.
        """
        return len(
            self.singleton_services(),
        )

    @property
    def total_transient(
        self,
    ) -> int:
        """
        Return the number of transient services.
        """
        return len(
            self.transient_services(),
        )

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def enable_service(
        self,
        identifier: Identifier,
    ) -> ServiceContract:
        """
        Enable a service.
        """
        service = self.require_service(
            identifier,
        )

        service.enabled = True

        return service

    def disable_service(
        self,
        identifier: Identifier,
    ) -> ServiceContract:
        """
        Disable a service.
        """
        service = self.require_service(
            identifier,
        )

        service.enabled = False

        return service

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def as_dict(
        self,
    ) -> dict[
        Identifier,
        ServiceContract,
    ]:
        """
        Export all registered services.
        """
        return self.copy()

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """
        return (
            f"{type(self).__name__}("
            f"services={self.total_services}, "
            f"enabled={self.total_enabled}, "
            f"singleton={self.total_singleton})"
        )


__all__ = [
    "ServiceRegistry",
]
