"""
Core model exports.

Provides the public model API shared across the Datavion AI
platform.
"""

from __future__ import annotations

from .active import ActiveModel
from .base import BaseModel
from .managers import (
    ActiveManager,
    AllObjectsManager,
    BaseManager,
    DeletedObjectsManager,
    SoftDeleteManager,
)
from .querysets import (
    ActiveQuerySet,
    BaseQuerySet,
    SoftDeleteQuerySet,
)
from .soft_delete import SoftDeleteModel
from .timestamp import TimeStampedModel
from .uuid import UUIDModel

__all__ = [
    # Base models
    "ActiveModel",
    "BaseModel",
    "SoftDeleteModel",
    "TimeStampedModel",
    "UUIDModel",
    # Managers
    "ActiveManager",
    "AllObjectsManager",
    "BaseManager",
    "DeletedObjectsManager",
    "SoftDeleteManager",
    # QuerySets
    "ActiveQuerySet",
    "BaseQuerySet",
    "SoftDeleteQuerySet",
]
