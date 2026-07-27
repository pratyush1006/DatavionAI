"""
Audit registry for DatavionOS.

Maintains registered audit processors and handlers.

The registry keeps the audit framework extensible without
coupling to storage or external compliance systems.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from apps.common.audit.exceptions import (
    AuditAlreadyRegisteredError,
    AuditNotFoundError,
)


class AuditHandler(
    Protocol,
):
    """
    Contract for audit handlers.
    """

    name: str

    def handle(
        self,
        record: object,
    ) -> None:
        """
        Process an audit record.
        """


class AuditRegistry:
    """
    Central audit handler registry.

    Supports:

    - Handler registration
    - Handler lookup
    - Handler discovery
    - Duplicate protection
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize registry.
        """

        self._handlers: dict[
            str,
            AuditHandler,
        ] = {}

    def register(
        self,
        handler: AuditHandler,
    ) -> None:
        """
        Register audit handler.

        Raises:
            AuditAlreadyRegisteredError:
                If handler already exists.
        """

        if handler.name in self._handlers:
            raise AuditAlreadyRegisteredError(
                (f"Audit handler '{handler.name}' already registered."),
            )

        self._handlers[handler.name] = handler

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove audit handler.
        """

        self._handlers.pop(
            name,
            None,
        )

    def get(
        self,
        name: str,
    ) -> AuditHandler:
        """
        Return audit handler.

        Raises:
            AuditNotFoundError:
                If handler does not exist.
        """

        handler = self._handlers.get(
            name,
        )

        if handler is None:
            raise AuditNotFoundError(
                (f"Audit handler '{name}' does not exist."),
            )

        return handler

    def has(
        self,
        name: str,
    ) -> bool:
        """
        Check whether handler exists.
        """

        return name in self._handlers

    def all(
        self,
    ) -> Iterable[AuditHandler]:
        """
        Return all handlers.
        """

        return self._handlers.values()

    def clear(
        self,
    ) -> None:
        """
        Remove all handlers.
        """

        self._handlers.clear()


audit_registry = AuditRegistry()


__all__: tuple[str, ...] = (
    "AuditHandler",
    "AuditRegistry",
    "audit_registry",
)
