"""
Platform configuration contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    TypeVar,
    runtime_checkable,
)

T = TypeVar("T")


class ConfigurationScope(
    StrEnum,
):
    """
    Configuration resolution scope.
    """

    GLOBAL = "global"
    ENVIRONMENT = "environment"
    TENANT = "tenant"
    ORGANIZATION = "organization"
    MODULE = "module"
    USER = "user"


@dataclass(
    frozen=True,
    slots=True,
)
class ConfigurationContext:
    """
    Configuration resolution context.
    """

    environment: str | None = None

    tenant_id: str | None = None

    organization_id: str | None = None

    module: str | None = None

    user_id: str | None = None


@runtime_checkable
class ConfigurationProvider(
    Protocol,
):
    """
    Platform configuration abstraction.
    """

    def exists(
        self,
        key: str,
        *,
        context: ConfigurationContext | None = None,
    ) -> bool:
        """
        Determine whether a configuration
        key exists.
        """

    def get(
        self,
        key: str,
        default: T | None = None,
        *,
        context: ConfigurationContext | None = None,
    ) -> T | None:
        """
        Return a typed configuration
        value.
        """

    def get_required(
        self,
        key: str,
        *,
        context: ConfigurationContext | None = None,
    ) -> Any:
        """
        Return a required configuration
        value.

        Raises ConfigurationProviderError
        if the value cannot be resolved.
        """

    def get_section(
        self,
        section: str,
        *,
        context: ConfigurationContext | None = None,
    ) -> dict[str, Any]:
        """
        Return a configuration section.
        """

    def reload(
        self,
    ) -> None:
        """
        Reload configuration from
        underlying providers.
        """


__all__ = [
    "ConfigurationScope",
    "ConfigurationContext",
    "ConfigurationProvider",
]
