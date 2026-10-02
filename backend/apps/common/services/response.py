"""
DatavionAI Service Response.

Standardized service response objects.

Design Principles
-----------------
- Framework agnostic
- Immutable
- Type-safe
- Serialization friendly
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypeVar

T = TypeVar("T")


@dataclass(
    frozen=True,
    slots=True,
)
class ServiceResponse[T]:
    """
    Standard service response.
    """

    success: bool

    data: T | None = None

    message: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def failed(
        self,
    ) -> bool:
        """
        Convenience property.
        """

        return not self.success


def success[T](
    data: T | None = None,
    *,
    message: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> ServiceResponse[T]:
    """
    Create a successful service response.
    """

    return ServiceResponse(
        success=True,
        data=data,
        message=message,
        metadata=metadata or {},
    )


def failure(
    *,
    message: str,
    metadata: dict[str, Any] | None = None,
) -> ServiceResponse[None]:
    """
    Create a failed service response.

    Normally services raise exceptions instead of
    returning failures. This helper exists for
    workflows where failures are expected.
    """

    return ServiceResponse(
        success=False,
        data=None,
        message=message,
        metadata=metadata or {},
    )


__all__ = (
    "ServiceResponse",
    "failure",
    "success",
)
