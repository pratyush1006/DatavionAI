"""
Organization signal registration.
"""

from __future__ import annotations

from .organization import (
    organization_post_delete,
    organization_post_save,
)

__all__: tuple[str, ...] = (
    "organization_post_delete",
    "organization_post_save",
)
