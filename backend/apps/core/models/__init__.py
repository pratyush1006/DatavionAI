"""
Public model exports for the DatavionOS platform.

This module defines the stable public API for the
``apps.core.models`` package.

Applications should import models, managers and querysets
from this module instead of importing implementation modules
directly.
"""

from __future__ import annotations

# ============================================================================
# Base Models
# ============================================================================
from .active import ActiveModel
from .base import BaseModel

# ============================================================================
# Managers
# ============================================================================
from .managers import (
    ActiveManager,
    AllObjectsManager,
    BaseManager,
    DeletedObjectsManager,
    SoftDeleteManager,
)

# ============================================================================
# QuerySets
# ============================================================================
from .querysets import (
    ActiveQuerySet,
    BaseQuerySet,
    DeleteResult,
    SoftDeleteQuerySet,
)
from .soft_delete import SoftDeleteModel
from .timestamp import TimeStampedModel
from .uuid import UUIDModel

__all__: tuple[str, ...] = (
    # ------------------------------------------------------------------
    # Base Models
    # ------------------------------------------------------------------
    "ActiveModel",
    "BaseModel",
    "SoftDeleteModel",
    "TimeStampedModel",
    "UUIDModel",
    # ------------------------------------------------------------------
    # Managers
    # ------------------------------------------------------------------
    "ActiveManager",
    "AllObjectsManager",
    "BaseManager",
    "DeletedObjectsManager",
    "SoftDeleteManager",
    # ------------------------------------------------------------------
    # QuerySets
    # ------------------------------------------------------------------
    "ActiveQuerySet",
    "BaseQuerySet",
    "DeleteResult",
    "SoftDeleteQuerySet",
)
