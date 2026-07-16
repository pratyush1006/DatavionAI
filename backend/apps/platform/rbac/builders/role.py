"""
Role builder.
"""

from __future__ import annotations

import re
from typing import Final

from apps.platform.rbac.constants import (
    DEFAULT_DISPLAY_ORDER,
    DEFAULT_ROLE_PRIORITY,
)


class RoleBuilder:
    """
    Enterprise builder for Role.

    Responsible for generating and normalizing derived role values.
    This class must not perform database operations.
    """

    _CODE_PATTERN: Final[re.Pattern[str]] = re.compile(
        r"[^a-z0-9]+",
    )

    @classmethod
    def normalize_name(
        cls,
        *,
        name: str,
    ) -> str:
        """
        Normalize a role name.
        """

        return " ".join(
            name.strip().split(),
        )

    @classmethod
    def build_code(
        cls,
        *,
        name: str,
    ) -> str:
        """
        Build a normalized role code.
        """

        normalized = cls.normalize_name(
            name=name,
        ).lower()

        normalized = normalized.replace(
            "&",
            " and ",
        )

        normalized = cls._CODE_PATTERN.sub(
            "_",
            normalized,
        )

        return normalized.strip(
            "_",
        )

    @classmethod
    def build_name(
        cls,
        *,
        code: str,
    ) -> str:
        """
        Build a human-readable role name.
        """

        return code.replace(
            "_",
            " ",
        ).title()

    @classmethod
    def build(
        cls,
        *,
        name: str,
    ) -> str:
        """
        Build and return the normalized role code.

        This method is kept for backward compatibility.
        """

        return cls.build_code(
            name=name,
        )

    @classmethod
    def build_metadata(
        cls,
        *,
        name: str,
        priority: int | None = None,
        display_order: int | None = None,
    ) -> dict[str, object]:
        """
        Build complete role metadata.

        Intended for services and serializers.
        """

        normalized_name = cls.normalize_name(
            name=name,
        )

        return {
            "name": normalized_name,
            "code": cls.build_code(
                name=normalized_name,
            ),
            "priority": (priority if priority is not None else DEFAULT_ROLE_PRIORITY),
            "display_order": (
                display_order if display_order is not None else DEFAULT_DISPLAY_ORDER
            ),
        }


__all__ = [
    "RoleBuilder",
]
