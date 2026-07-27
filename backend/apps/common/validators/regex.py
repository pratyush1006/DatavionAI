"""
DatavionAI Regex Validators.

Reusable regular expression validation helpers.

Design Principles
-----------------
- Stateless
- Type-safe
- Reusable
- Uses centralized regex constants
"""

from __future__ import annotations

import re
from re import Pattern

from apps.common.exceptions.base import ValidationException

from .messages import get_message


class RegexValidator:
    """
    Generic regular expression validator.
    """

    @classmethod
    def validate(
        cls,
        value: str,
        *,
        pattern: str | Pattern[str],
        message: str | None = None,
    ) -> str:
        """
        Validate a string using a regular expression.

        Args:
            value: Value to validate.
            pattern: Compiled or raw regular expression.
            message: Optional custom error message.

        Returns:
            The validated value.

        Raises:
            ValidationException:
                If the value does not match the pattern.
        """

        compiled_pattern = re.compile(pattern) if isinstance(pattern, str) else pattern

        if not compiled_pattern.fullmatch(value):
            raise ValidationException(
                message=message or get_message("invalid_format"),
            )

        return value


__all__ = ("RegexValidator",)
