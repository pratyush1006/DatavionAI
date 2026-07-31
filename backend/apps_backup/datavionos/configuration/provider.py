"""
Configuration provider contracts.
"""

from __future__ import annotations

from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

from apps.datavionos.configuration.configuration import (
    ConfigurationEntry,
    ConfigurationSnapshot,
)


@runtime_checkable
class ConfigurationProvider(
    Protocol,
):
    """
    Provides configuration values.
    """

    async def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Return a configuration value.
        """

    async def has(
        self,
        key: str,
    ) -> bool:
        """
        Determine whether a configuration value exists.
        """

    async def set(
        self,
        entry: ConfigurationEntry,
    ) -> None:
        """
        Store or update a configuration entry.
        """

    async def remove(
        self,
        key: str,
    ) -> None:
        """
        Remove a configuration entry.
        """

    async def snapshot(
        self,
    ) -> ConfigurationSnapshot:
        """
        Return the current configuration snapshot.
        """

    async def keys(
        self,
    ) -> tuple[str, ...]:
        """
        Return all configuration keys.
        """


__all__ = [
    "ConfigurationProvider",
]
