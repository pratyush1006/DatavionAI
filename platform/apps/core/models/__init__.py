"""
Core model exports.
"""

from .active import ActiveMixin
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

# Temporary backward compatibility
TimestampMixin = TimeStampedModel
UUIDMixin = UUIDModel

__all__ = [
    # Base Models
    "ActiveMixin",
    "BaseModel",
    "SoftDeleteModel",
    "TimeStampedModel",
    "UUIDModel",
    # Managers
    "BaseManager",
    "ActiveManager",
    "SoftDeleteManager",
    "AllObjectsManager",
    "DeletedObjectsManager",
    # QuerySets
    "BaseQuerySet",
    "ActiveQuerySet",
    "SoftDeleteQuerySet",
]
