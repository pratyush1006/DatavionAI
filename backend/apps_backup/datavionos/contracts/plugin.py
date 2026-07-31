"""
Plugin contract definitions.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
)

from apps.datavionos.constants import PluginStatus
from apps.datavionos.contracts.base import BaseContract


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PluginContract(BaseContract):
    """
    Immutable plugin definition.

    A plugin represents an installable extension for
    DatavionOS that can provide modules, services,
    capabilities, workflows, AI agents and integrations.
    """

    display_name: str

    version: str = "1.0.0"

    description: str = ""

    author: str = ""

    organization: str = ""

    homepage: str = ""

    repository: str = ""

    documentation: str = ""

    license: str = ""

    enabled: bool = True

    installed: bool = False

    system: bool = False

    signed: bool = False

    verified: bool = False

    auto_start: bool = True

    priority: int = 0

    dependencies: tuple[str, ...] = ()

    optional_dependencies: tuple[str, ...] = ()

    modules: tuple[str, ...] = ()

    capabilities: tuple[str, ...] = ()

    services: tuple[str, ...] = ()

    feature_flags: tuple[str, ...] = ()

    tags: tuple[str, ...] = ()

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    status: PluginStatus = PluginStatus.ACTIVE

    def validate(self) -> None:
        """
        Validate the plugin contract.
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

        if self.priority < 0:
            raise ValueError(
                "priority cannot be negative.",
            )

        if self.identifier in self.dependencies:
            raise ValueError(
                "A plugin cannot depend on itself.",
            )

    @property
    def dependency_count(self) -> int:
        """
        Number of required dependencies.
        """

        return len(self.dependencies)

    @property
    def optional_dependency_count(self) -> int:
        """
        Number of optional dependencies.
        """

        return len(self.optional_dependencies)

    @property
    def module_count(self) -> int:
        """
        Number of exported modules.
        """

        return len(self.modules)

    @property
    def capability_count(self) -> int:
        """
        Number of exported capabilities.
        """

        return len(self.capabilities)

    @property
    def service_count(self) -> int:
        """
        Number of exported services.
        """

        return len(self.services)

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
        Whether the plugin is active.
        """

        return self.status is PluginStatus.ACTIVE

    @property
    def is_enabled(self) -> bool:
        """
        Whether the plugin is enabled.
        """

        return self.enabled

    @property
    def is_installed(self) -> bool:
        """
        Whether the plugin is installed.
        """

        return self.installed

    @property
    def is_verified(self) -> bool:
        """
        Whether the plugin has been verified.
        """

        return self.verified

    @property
    def has_dependencies(self) -> bool:
        """
        Whether required dependencies exist.
        """

        return bool(self.dependencies)

    @property
    def qualified_name(self) -> str:
        """
        Qualified plugin name.
        """

        return f"{self.identifier}:{self.version}"

    @property
    def supports_auto_start(self) -> bool:
        """
        Whether the plugin should automatically start.
        """

        return self.auto_start

    @property
    def is_system_plugin(self) -> bool:
        """
        Whether this is a system plugin.
        """

        return self.system

    @property
    def is_signed(self) -> bool:
        """
        Whether the plugin package is digitally signed.
        """

        return self.signed

    def with_enabled(
        self,
        enabled: bool,
    ) -> PluginContract:
        """
        Return a copy with a new enabled state.
        """

        from dataclasses import replace

        return replace(
            self,
            enabled=enabled,
        )

    def with_installed(
        self,
        installed: bool,
    ) -> PluginContract:
        """
        Return a copy with a new installation state.
        """

        from dataclasses import replace

        return replace(
            self,
            installed=installed,
        )

    def with_status(
        self,
        status: PluginStatus,
    ) -> PluginContract:
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
    ) -> PluginContract:
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
    ) -> PluginContract:
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
        Serialize the plugin contract.
        """

        return {
            "identifier": self.identifier,
            "name": self.name,
            "display_name": self.display_name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "organization": self.organization,
            "homepage": self.homepage,
            "repository": self.repository,
            "documentation": self.documentation,
            "license": self.license,
            "enabled": self.enabled,
            "installed": self.installed,
            "system": self.system,
            "signed": self.signed,
            "verified": self.verified,
            "auto_start": self.auto_start,
            "priority": self.priority,
            "dependencies": list(self.dependencies),
            "optional_dependencies": list(
                self.optional_dependencies,
            ),
            "modules": list(self.modules),
            "capabilities": list(self.capabilities),
            "services": list(self.services),
            "feature_flags": list(self.feature_flags),
            "tags": list(self.tags),
            "metadata": dict(self.metadata),
            "status": self.status.value,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> PluginContract:
        """
        Create a plugin contract from a dictionary.
        """

        return cls(
            identifier=data["identifier"],
            name=data["name"],
            display_name=data["display_name"],
            version=data.get(
                "version",
                "1.0.0",
            ),
            description=data.get(
                "description",
                "",
            ),
            author=data.get(
                "author",
                "",
            ),
            organization=data.get(
                "organization",
                "",
            ),
            homepage=data.get(
                "homepage",
                "",
            ),
            repository=data.get(
                "repository",
                "",
            ),
            documentation=data.get(
                "documentation",
                "",
            ),
            license=data.get(
                "license",
                "",
            ),
            enabled=data.get(
                "enabled",
                True,
            ),
            installed=data.get(
                "installed",
                False,
            ),
            system=data.get(
                "system",
                False,
            ),
            signed=data.get(
                "signed",
                False,
            ),
            verified=data.get(
                "verified",
                False,
            ),
            auto_start=data.get(
                "auto_start",
                True,
            ),
            priority=data.get(
                "priority",
                0,
            ),
            dependencies=tuple(
                data.get(
                    "dependencies",
                    [],
                ),
            ),
            optional_dependencies=tuple(
                data.get(
                    "optional_dependencies",
                    [],
                ),
            ),
            modules=tuple(
                data.get(
                    "modules",
                    [],
                ),
            ),
            capabilities=tuple(
                data.get(
                    "capabilities",
                    [],
                ),
            ),
            services=tuple(
                data.get(
                    "services",
                    [],
                ),
            ),
            feature_flags=tuple(
                data.get(
                    "feature_flags",
                    [],
                ),
            ),
            tags=tuple(
                data.get(
                    "tags",
                    [],
                ),
            ),
            metadata=data.get(
                "metadata",
                {},
            ),
            status=PluginStatus(
                data.get(
                    "status",
                    PluginStatus.ACTIVE.value,
                ),
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
            f"installed={self.installed!r}, "
            f"enabled={self.enabled!r})"
        )


__all__ = [
    "PluginContract",
]
