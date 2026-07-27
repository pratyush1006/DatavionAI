"""
DatavionAI Service Validation.

Reusable validation helpers for enterprise services.

Design Principles
-----------------
- Framework agnostic
- Stateless
- Exception framework integration
- Reusable across all services
"""

from __future__ import annotations

from collections.abc import Collection
from typing import Any

from apps.common.exceptions.builders import (
    resource_not_found,
    validation_error,
)


class ValidationService:
    """
    Shared validation helpers for services.
    """

    @staticmethod
    def require(
        condition: bool,
        *,
        message: str,
        detail: Any = None,
    ) -> None:
        """
        Ensure a condition is True.
        """

        if not condition:
            raise validation_error(
                message=message,
                detail=detail,
            )

    @staticmethod
    def require_not_none(
        value: Any,
        *,
        message: str,
    ) -> Any:
        """
        Ensure a value is not None.
        """

        if value is None:
            raise validation_error(
                message=message,
            )

        return value

    @staticmethod
    def require_not_empty(
        value: Collection[Any] | str,
        *,
        message: str,
    ) -> Collection[Any] | str:
        """
        Ensure a collection or string is not empty.
        """

        if not value:
            raise validation_error(
                message=message,
            )

        return value

    @staticmethod
    def require_resource(
        resource: Any,
        *,
        resource_name: str,
        identifier: str | int | None = None,
    ) -> Any:
        """
        Ensure a resource exists.
        """

        if resource is None:
            raise resource_not_found(
                resource=resource_name,
                identifier=identifier,
            )

        return resource

    @staticmethod
    def require_true(
        condition: bool,
        *,
        message: str,
    ) -> None:
        """
        Alias for require().
        """

        ValidationService.require(
            condition,
            message=message,
        )

    @staticmethod
    def require_false(
        condition: bool,
        *,
        message: str,
    ) -> None:
        """
        Ensure a condition is False.
        """

        ValidationService.require(
            not condition,
            message=message,
        )


__all__ = ("ValidationService",)
