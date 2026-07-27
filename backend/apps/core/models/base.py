"""
Base model classes shared across the DatavionOS platform.

Provides the standard persistence foundation used by all
business entities.
"""

from __future__ import annotations

from .active import ActiveModel
from .soft_delete import SoftDeleteModel
from .timestamp import TimeStampedModel
from .uuid import UUIDModel


class BaseModel(
    UUIDModel,
    TimeStampedModel,
    SoftDeleteModel,
    ActiveModel,
):
    """
    Enterprise persistence base model.

    Provides:

        - UUID identity
        - Creation timestamp
        - Update timestamp
        - Soft deletion
        - Active/inactive lifecycle

    Design principles:

        - Keep framework concerns isolated
        - Avoid domain-specific fields
        - Support multi-tenant SaaS architecture
        - Preserve healthcare auditability

    Domain-specific capabilities should be added using
    dedicated abstract models.

    Examples:

        TenantAwareModel
        AuditableModel
        VersionedModel
        SearchableModel
    """

    class Meta:
        """
        Django model metadata.
        """

        abstract = True


__all__: tuple[str, ...] = ("BaseModel",)
