"""
Capability contract definitions.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
)

from apps.datavionos.constants import CapabilityCategory, CapabilityStatus
from apps.datavionos.contracts.base import BaseContract


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class CapabilityContract(BaseContract):
    """
    Immutable capability definition.

    A capability represents reusable platform functionality
    that can be shared across multiple modules.
    """

    display_name: str

    category: CapabilityCategory

    version: str = "1.0.0"

    description: str = ""

    enabled: bool = True

    public: bool = False

    system: bool = True

    singleton: bool = True

    tags: tuple[str, ...] = ()

    dependencies: tuple[str, ...] = ()

    feature_flags: tuple[str, ...] = ()

    permissions: tuple[str, ...] = ()

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    status: CapabilityStatus = CapabilityStatus.ACTIVE

    owner: str = ""

    documentation: str = ""

    def validate(self) -> None:
        """
        Validate the capability.
        """

        super().validate()

        if not self.display_name.strip():
            raise ValueError(
                "display_name cannot be empty.",
            )

        if not self.version.strip():
            raise ValueError(
                "version cannot be empty.",
            )

        if self.identifier in self.dependencies:
            raise ValueError(
                "A capability cannot depend on itself.",
            )

    @property
    def dependency_count(self) -> int:
        """
        Number of required dependencies.
        """

        return len(self.dependencies)

    @property
    def permission_count(self) -> int:
        """
        Number of permissions.
        """

        return len(self.permissions)

    @property
    def feature_flag_count(self) -> int:
        """
        Number of feature flags.
        """

        return len(self.feature_flags)

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
        Whether the capability is active.
        """

        return self.status is CapabilityStatus.ACTIVE

    @property
    def is_disabled(self) -> bool:
        """
        Whether the capability is disabled.
        """

        return not self.enabled

    @property
    def is_public(self) -> bool:
        """
        Whether the capability is publicly available.
        """

        return self.public

    @property
    def has_dependencies(self) -> bool:
        """
        Whether dependencies exist.
        """

        return bool(self.dependencies)

    @property
    def qualified_name(self) -> str:
        """
        Qualified capability name.
        """

        return f"{self.identifier}:{self.version}"

    def with_enabled(
        self,
        enabled: bool,
    ) -> CapabilityContract:
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
        status: CapabilityStatus,
    ) -> CapabilityContract:
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
    ) -> CapabilityContract:
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
    ) -> CapabilityContract:
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
        Serialize the capability.
        """

        return {
            "identifier": self.identifier,
            "name": self.name,
            "display_name": self.display_name,
            "category": self.category.value,
            "version": self.version,
            "description": self.description,
            "enabled": self.enabled,
            "public": self.public,
            "system": self.system,
            "singleton": self.singleton,
            "tags": list(self.tags),
            "dependencies": list(self.dependencies),
            "feature_flags": list(self.feature_flags),
            "permissions": list(self.permissions),
            "metadata": dict(self.metadata),
            "status": self.status.value,
            "owner": self.owner,
            "documentation": self.documentation,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> CapabilityContract:
        """
        Create a capability contract from a dictionary.
        """

        return cls(
            identifier=data["identifier"],
            name=data["name"],
            display_name=data["display_name"],
            category=CapabilityCategory(
                data["category"],
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
            public=data.get(
                "public",
                False,
            ),
            system=data.get(
                "system",
                True,
            ),
            singleton=data.get(
                "singleton",
                True,
            ),
            tags=tuple(
                data.get(
                    "tags",
                    [],
                ),
            ),
            dependencies=tuple(
                data.get(
                    "dependencies",
                    [],
                ),
            ),
            feature_flags=tuple(
                data.get(
                    "feature_flags",
                    [],
                ),
            ),
            permissions=tuple(
                data.get(
                    "permissions",
                    [],
                ),
            ),
            metadata=data.get(
                "metadata",
                {},
            ),
            status=CapabilityStatus(
                data.get(
                    "status",
                    CapabilityStatus.ACTIVE.value,
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
            f"version={self.version!r}, "
            f"enabled={self.enabled!r})"
        )


__all__ = [
    "CapabilityContract",
]
