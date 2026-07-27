"""
DatavionAI Common Validators.

Reusable validators shared across the platform.
"""

from __future__ import annotations

from collections.abc import Collection
from typing import Any

from apps.common.exceptions.base import ValidationException

from .base import BaseValidator
from .messages import get_message


class RequiredValidator(
    BaseValidator[Any],
):
    """
    Ensure a value is provided.
    """

    @classmethod
    def check(
        cls,
        value: Any,
        **kwargs: Any,
    ) -> None:
        if value is None:
            raise ValidationException(
                message=get_message("required"),
            )


class NotBlankValidator(
    BaseValidator[str],
):
    """
    Ensure a string is not blank.
    """

    @classmethod
    def check(
        cls,
        value: str,
        **kwargs: Any,
    ) -> None:
        if not value.strip():
            raise ValidationException(
                message=get_message("blank"),
            )


class MinLengthValidator(
    BaseValidator[str],
):
    """
    Validate minimum string length.
    """

    @classmethod
    def check(
        cls,
        value: str,
        *,
        min_length: int,
        **kwargs: Any,
    ) -> None:
        if len(value) < min_length:
            raise ValidationException(
                message=get_message(
                    "min_length",
                    min_length=min_length,
                ),
            )


class MaxLengthValidator(
    BaseValidator[str],
):
    """
    Validate maximum string length.
    """

    @classmethod
    def check(
        cls,
        value: str,
        *,
        max_length: int,
        **kwargs: Any,
    ) -> None:
        if len(value) > max_length:
            raise ValidationException(
                message=get_message(
                    "max_length",
                    max_length=max_length,
                ),
            )


class MinValueValidator(
    BaseValidator[int | float],
):
    """
    Validate minimum numeric value.
    """

    @classmethod
    def check(
        cls,
        value: int | float,
        *,
        min_value: int | float,
        **kwargs: Any,
    ) -> None:
        if value < min_value:
            raise ValidationException(
                message=get_message(
                    "min_value",
                    min_value=min_value,
                ),
            )


class MaxValueValidator(
    BaseValidator[int | float],
):
    """
    Validate maximum numeric value.
    """

    @classmethod
    def check(
        cls,
        value: int | float,
        *,
        max_value: int | float,
        **kwargs: Any,
    ) -> None:
        if value > max_value:
            raise ValidationException(
                message=get_message(
                    "max_value",
                    max_value=max_value,
                ),
            )


class ChoiceValidator(
    BaseValidator[Any],
):
    """
    Validate allowed choices.
    """

    @classmethod
    def check(
        cls,
        value: Any,
        *,
        choices: Collection[Any],
        **kwargs: Any,
    ) -> None:
        if value not in choices:
            raise ValidationException(
                message=get_message(
                    "invalid_choice",
                ),
            )


class RangeValidator(
    BaseValidator[int | float],
):
    """
    Validate numeric range.
    """

    @classmethod
    def check(
        cls,
        value: int | float,
        *,
        minimum: int | float,
        maximum: int | float,
        **kwargs: Any,
    ) -> None:
        if value < minimum or value > maximum:
            raise ValidationException(
                message=get_message(
                    "invalid",
                ),
            )


__all__ = (
    "ChoiceValidator",
    "MaxLengthValidator",
    "MaxValueValidator",
    "MinLengthValidator",
    "MinValueValidator",
    "NotBlankValidator",
    "RangeValidator",
    "RequiredValidator",
)
