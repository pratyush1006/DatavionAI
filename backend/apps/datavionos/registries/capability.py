"""
Capability registry for DatavionOS.

This module manages platform capabilities that can be exposed by
modules, plugins and services.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.datavionos.exceptions import RegistryError
from apps.datavionos.types import CapabilityName

from ..contracts.capability import CapabilityContract
from .registry import Registry


class CapabilityRegistry(
    Registry[
        CapabilityName,
        CapabilityContract,
    ],
):
    """
    Registry for platform capabilities.

    Capabilities represent reusable features that may be provided
    by one or more platform components.
    """

    def __init__(self) -> None:
        super().__init__(
            name="capabilities",
        )

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_capability(
        self,
        capability: CapabilityContract,
    ) -> CapabilityContract:
        """
        Register a capability.
        """
        return self.register(
            key=capability.name,
            value=capability,
        )

    def register_capabilities(
        self,
        capabilities: Iterable[CapabilityContract],
    ) -> None:
        """
        Register multiple capabilities.
        """
        for capability in capabilities:
            self.register_capability(
                capability,
            )

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get_capability(
        self,
        name: CapabilityName,
    ) -> CapabilityContract | None:
        """
        Retrieve a capability.
        """
        return self.get(
            name,
        )

    def require_capability(
        self,
        name: CapabilityName,
    ) -> CapabilityContract:
        """
        Retrieve a required capability.
        """
        return self.require(
            name,
        )

    def unregister_capability(
        self,
        name: CapabilityName,
    ) -> CapabilityContract:
        """
        Remove a capability.
        """
        return self.unregister(
            name,
        )

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def enabled_capabilities(
        self,
    ) -> list[CapabilityContract]:
        """
        Return enabled capabilities.
        """
        return [capability for capability in self.values() if capability.enabled]

    def disabled_capabilities(
        self,
    ) -> list[CapabilityContract]:
        """
        Return disabled capabilities.
        """
        return [capability for capability in self.values() if not capability.enabled]

    def public_capabilities(
        self,
    ) -> list[CapabilityContract]:
        """
        Return public capabilities.
        """
        return [capability for capability in self.values() if capability.public]

    def private_capabilities(
        self,
    ) -> list[CapabilityContract]:
        """
        Return private capabilities.
        """
        return [capability for capability in self.values() if not capability.public]

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate_registration(
        self,
        *,
        key: CapabilityName,
        value: CapabilityContract,
    ) -> None:
        """
        Validate capability registration.
        """
        super()._validate_registration(
            key=key,
            value=value,
        )

        if value.name != key:
            raise RegistryError(
                message=("Capability name does not match registry key."),
                error_code="CAPABILITY_NAME_MISMATCH",
            )

        if not value.name.strip():
            raise RegistryError(
                message="Capability name cannot be empty.",
                error_code="CAPABILITY_NAME_REQUIRED",
            )

        if not value.version.strip():
            raise RegistryError(
                message="Capability version cannot be empty.",
                error_code="CAPABILITY_VERSION_REQUIRED",
            )

        if self.exists(key):
            existing = self.require(key)

            if existing.version == value.version:
                raise RegistryError(
                    message=(
                        f"Capability '{value.name}' "
                        f"version '{value.version}' "
                        "is already registered."
                    ),
                    error_code="CAPABILITY_ALREADY_REGISTERED",
                )

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @property
    def total_capabilities(
        self,
    ) -> int:
        """
        Return the total number of registered capabilities.
        """
        return self.size

    @property
    def total_enabled(
        self,
    ) -> int:
        """
        Return the number of enabled capabilities.
        """
        return len(
            self.enabled_capabilities(),
        )

    @property
    def total_disabled(
        self,
    ) -> int:
        """
        Return the number of disabled capabilities.
        """
        return len(
            self.disabled_capabilities(),
        )

    @property
    def total_public(
        self,
    ) -> int:
        """
        Return the number of public capabilities.
        """
        return len(
            self.public_capabilities(),
        )

    @property
    def total_private(
        self,
    ) -> int:
        """
        Return the number of private capabilities.
        """
        return len(
            self.private_capabilities(),
        )

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def enable_capability(
        self,
        name: CapabilityName,
    ) -> CapabilityContract:
        """
        Enable a capability.
        """
        capability = self.require_capability(
            name,
        )

        capability.enabled = True

        return capability

    def disable_capability(
        self,
        name: CapabilityName,
    ) -> CapabilityContract:
        """
        Disable a capability.
        """
        capability = self.require_capability(
            name,
        )

        capability.enabled = False

        return capability

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def as_dict(
        self,
    ) -> dict[
        CapabilityName,
        CapabilityContract,
    ]:
        """
        Export all registered capabilities.
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
            f"capabilities={self.total_capabilities}, "
            f"enabled={self.total_enabled})"
        )


__all__ = [
    "CapabilityRegistry",
]
