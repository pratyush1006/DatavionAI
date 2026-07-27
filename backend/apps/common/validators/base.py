"""
DatavionAI Validation Framework.

Base validator infrastructure.

Design Principles
-----------------
- Framework agnostic
- Stateless
- Reusable
- Type-safe
- Enterprise ready
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BaseValidator(
    ABC,
    Generic[T],
):
    """
    Base class for all validators.

    Validators should raise an exception when
    validation fails.

    They should return the validated value
    when validation succeeds.
    """

    @classmethod
    def validate(
        cls,
        value: T,
        **kwargs: Any,
    ) -> T:
        """
        Validate a value.
        """

        cls.check(
            value,
            **kwargs,
        )

        return value

    @classmethod
    @abstractmethod
    def check(
        cls,
        value: T,
        **kwargs: Any,
    ) -> None:
        """
        Perform validation.

        Raise ValidationException when invalid.
        """

        raise NotImplementedError
