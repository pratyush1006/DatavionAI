"""
Permission group builder.
"""

from __future__ import annotations

import re


class PermissionGroupBuilder:
    """
    Builder for permission groups.
    """

    @staticmethod
    def build_code(
        *,
        name: str,
    ) -> str:
        """
        Build a normalized permission group code.
        """

        code = name.strip().lower().replace("&", "and")

        code = re.sub(
            r"[^a-z0-9]+",
            "_",
            code,
        )

        return code.strip("_")

    @staticmethod
    def build_name(
        *,
        code: str,
    ) -> str:
        """
        Build a display name from a permission group code.
        """

        return code.replace(
            "_",
            " ",
        ).title()

    @staticmethod
    def build_display_order(
        *,
        code: str,
    ) -> int:
        """
        Build the default sort order.

        Reserved for future customization.
        """

        return 0


__all__ = [
    "PermissionGroupBuilder",
]
