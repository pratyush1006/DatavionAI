"""
Service contract definitions.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
)

from apps.datavionos.constants import ServiceLifetime, ServiceStatus
from apps.datavionos.contracts.base import BaseContract


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ServiceContract(BaseContract):
    """
    Immutable service definition.

    A service contract describes a dependency injection
    service registered within the DatavionOS service
    container.
    """

    display_name: str

    implementation: str

    lifetime: ServiceLifetime

    version: str = "1.0.0"

    description: str = ""

    enabled: bool = True

    lazy: bool = True

    primary: bool = False

    overridable: bool = True

    system: bool = True

    dependencies: tuple[str, ...] = ()

    tags: tuple[str, ...] = ()

    aliases: tuple[str, ...] = ()

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    status: ServiceStatus = ServiceStatus.ACTIVE

    owner: str = ""

    documentation: str = ""

    def validate(self) -> None:
        """
        Validate the service contract.
        """

        super().validate()

        if not self.display_name.strip():
            raise ValueError(
                "display_name cannot be empty.",
            )

        if not self.implementation.strip():
            raise ValueError(
                "implementation cannot be empty.",
            )

        if not self.version.strip():
            raise ValueError(
                "version cannot be empty.",
            )

        if self.identifier in self.dependencies:
            raise ValueError(
                "A service cannot depend on itself.",
            )

    @property
    def dependency_count(self) -> int:
        """
        Number of dependencies.
        """

        return len(self.dependencies)

    @property
    def alias_count(self) -> int:
        """
        Number of aliases.
        """

        return len(self.aliases)

    @property
    def tag_count(self) -> int:
        """
        Number of tags.
        """

        return len(self.tags)

    @property
    def metadata_count(self) -> int:
        """
        Number of metadata entries.
        """

        return len(self.metadata)

    @property
    def is_active(self) -> bool:
        """
        Whether the service is active.
        """

        return self.status is ServiceStatus.ACTIVE

    @property
    def is_disabled(self) -> bool:
        """
        Whether the service is disabled.
        """

        return not self.enabled

    @property
    def is_singleton(self) -> bool:
        """
        Whether the service is singleton.
        """

        return self.lifetime is ServiceLifetime.SINGLETON

    @property
    def is_scoped(self) -> bool:
        """
        Whether the service is scoped.
        """

        return self.lifetime is ServiceLifetime.SCOPED

    @property
    def is_transient(self) -> bool:
        """
        Whether the service is transient.
        """

        return self.lifetime is ServiceLifetime.TRANSIENT

    @property
    def has_dependencies(self) -> bool:
        """
        Whether dependencies exist.
        """

        return bool(self.dependencies)

    @property
    def qualified_name(self) -> str:
        """
        Qualified service name.
        """

        return f"{self.identifier}:{self.version}"

    @property
    def supports_override(self) -> bool:
        """
        Whether the service can be overridden.
        """

        return self.overridable

    @property
    def is_lazy(self) -> bool:
        """
        Whether the service is lazily initialized.
        """

        return self.lazy

    @property
    def is_primary(self) -> bool:
        """
        Whether this is the primary implementation.
        """

        return self.primary

    def with_enabled(
        self,
        enabled: bool,
    ) -> ServiceContract:
        """
        Return a copy with a new enabled state.
        """

        from dataclasses import replace

        return replace(
            self,
            enabled=enabled,
        )

    def with_status(
        self,
        status: ServiceStatus,
    ) -> ServiceContract:
        """
        Return a copy with a new status.
        """

        from dataclasses import replace

        return replace(
            self,
            status=status,
        )

    def with_version(
        self,
        version: str,
    ) -> ServiceContract:
        """
        Return a copy with a new version.
        """

        from dataclasses import replace

        return replace(
            self,
            version=version,
        )

    def with_metadata(
        self,
        **metadata: Any,
    ) -> ServiceContract:
        """
        Return a copy with merged metadata.
        """

        from dataclasses import replace

        updated_metadata = {
            **self.metadata,
            **metadata,
        }

        return replace(
            self,
            metadata=updated_metadata,
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the service contract.
        """

        return {
            "identifier": self.identifier,
            "name": self.name,
            "display_name": self.display_name,
            "implementation": self.implementation,
            "lifetime": self.lifetime.value,
            "version": self.version,
            "description": self.description,
            "enabled": self.enabled,
            "lazy": self.lazy,
            "primary": self.primary,
            "overridable": self.overridable,
            "system": self.system,
            "dependencies": list(self.dependencies),
            "tags": list(self.tags),
            "aliases": list(self.aliases),
            "metadata": dict(self.metadata),
            "status": self.status.value,
            "owner": self.owner,
            "documentation": self.documentation,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> ServiceContract:
        """
        Create a service contract from a dictionary.
        """

        return cls(
            identifier=data["identifier"],
            name=data["name"],
            display_name=data["display_name"],
            implementation=data["implementation"],
            lifetime=ServiceLifetime(
                data["lifetime"],
            ),
            version=data.get(
                "version",
                "1.0.0",
            ),
            description=data.get(
                "description",
                "",
            ),
            enabled=data.get(
                "enabled",
                True,
            ),
            lazy=data.get(
                "lazy",
                True,
            ),
            primary=data.get(
                "primary",
                False,
            ),
            overridable=data.get(
                "overridable",
                True,
            ),
            system=data.get(
                "system",
                True,
            ),
            dependencies=tuple(
                data.get(
                    "dependencies",
                    [],
                ),
            ),
            tags=tuple(
                data.get(
                    "tags",
                    [],
                ),
            ),
            aliases=tuple(
                data.get(
                    "aliases",
                    [],
                ),
            ),
            metadata=data.get(
                "metadata",
                {},
            ),
            status=ServiceStatus(
                data.get(
                    "status",
                    ServiceStatus.ACTIVE.value,
                ),
            ),
            owner=data.get(
                "owner",
                "",
            ),
            documentation=data.get(
                "documentation",
                "",
            ),
        )

    def __repr__(self) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"identifier={self.identifier!r}, "
            f"name={self.name!r}, "
            f"implementation={self.implementation!r}, "
            f"lifetime={self.lifetime.value!r}, "
            f"enabled={self.enabled!r})"
        )


__all__ = [
    "ServiceContract",
]
