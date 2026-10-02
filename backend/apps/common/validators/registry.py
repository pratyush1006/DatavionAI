"""
DatavionAI Validator Registry.

Central registry for reusable validators.
"""

from __future__ import annotations

from typing import Any


class ValidatorRegistry:
    """
    Registry for reusable validators.

    Allows validators to be registered and retrieved
    by name throughout the platform.
    """

    _registry: dict[str, Any] = {}

    @classmethod
    def register(
        cls,
        name: str,
        validator: Any,
    ) -> None:
        """
        Register a validator.
        """

        cls._registry[name] = validator

    @classmethod
    def get(
        cls,
        name: str,
    ) -> Any:
        """
        Retrieve a registered validator.

        Raises:
            KeyError: If the validator is not registered.
        """

        return cls._registry[name]

    @classmethod
    def exists(
        cls,
        name: str,
    ) -> bool:
        """
        Return True if the validator exists.
        """

        return name in cls._registry

    @classmethod
    def unregister(
        cls,
        name: str,
    ) -> None:
        """
        Remove a validator if it exists.
        """

        cls._registry.pop(name, None)

    @classmethod
    def clear(
        cls,
    ) -> None:
        """
        Clear all registered validators.
        """

        cls._registry.clear()

    @classmethod
    def all(
        cls,
    ) -> dict[str, Any]:
        """
        Return a copy of the registry.
        """

        return dict(cls._registry)


__all__ = ("ValidatorRegistry",)
