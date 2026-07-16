"""
Base model classes shared across the Datavion AI platform.
"""

from __future__ import annotations

from .active import ActiveModel
from .soft_delete import SoftDeleteModel
from .timestamp import TimeStampedModel
from .uuid import UUIDModel


class BaseModel(
    UUIDModel,
    TimeStampedModel,
    ActiveModel,
    SoftDeleteModel,
):
    """
    Base abstract model for business entities.

    Combines:

    - UUID primary key
    - Automatic timestamps
    - Active/inactive state
    - Soft delete support
    """

    class Meta:
        """
        Django model metadata.
        """

        abstract = True


__all__ = [
    "BaseModel",
]
