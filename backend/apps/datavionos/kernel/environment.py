"""
DatavionOS Kernel Environment.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path


@unique
class EnvironmentType(
    Enum,
):
    """
    Supported runtime environments.
    """

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

    def __str__(
        self,
    ) -> str:
        return self.value


@dataclass(
    frozen=True,
    slots=True,
)
class KernelEnvironment:
    """
    Represents the runtime execution
    environment for DatavionOS.
    """

    environment: EnvironmentType

    application_root: Path

    configuration_directory: Path

    data_directory: Path

    logs_directory: Path

    temporary_directory: Path

    @classmethod
    def discover(
        cls,
    ) -> KernelEnvironment:
        """
        Discover the runtime environment
        from the operating system.
        """

        environment = EnvironmentType(
            os.getenv(
                "DATAVION_ENVIRONMENT",
                EnvironmentType.DEVELOPMENT.value,
            ),
        )

        root = Path.cwd()

        return cls(
            environment=environment,
            application_root=root,
            configuration_directory=root / "config",
            data_directory=root / "data",
            logs_directory=root / "logs",
            temporary_directory=root / "tmp",
        )

    @property
    def is_development(
        self,
    ) -> bool:
        return self.environment is EnvironmentType.DEVELOPMENT

    @property
    def is_testing(
        self,
    ) -> bool:
        return self.environment is EnvironmentType.TESTING

    @property
    def is_staging(
        self,
    ) -> bool:
        return self.environment is EnvironmentType.STAGING

    @property
    def is_production(
        self,
    ) -> bool:
        return self.environment is EnvironmentType.PRODUCTION

    @property
    def application_name(
        self,
    ) -> str:
        """
        Application directory name.
        """

        return self.application_root.name

    def resolve_path(
        self,
        *parts: str,
    ) -> Path:
        """
        Resolve a path relative to the
        application root.
        """

        return self.application_root.joinpath(
            *parts,
        )

    def __repr__(
        self,
    ) -> str:
        return (
            "KernelEnvironment("
            f"environment={self.environment}, "
            f"root={self.application_root})"
        )


__all__ = [
    "EnvironmentType",
    "KernelEnvironment",
]
