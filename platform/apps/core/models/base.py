"""
Base model classes shared across Datavion AI.
"""

from __future__ import annotations

from .active import ActiveMixin
from .timestamp import TimeStampedModel
from .uuid import UUIDModel


class BaseModel(
    UUIDModel,
    TimeStampedModel,
    ActiveMixin,
):
    """
    Base abstract model for all business entities.

    Combines:
    - UUID primary key
    - Created/updated timestamps
    - Active/inactive flag
    """

    class Meta:
        abstract = True
