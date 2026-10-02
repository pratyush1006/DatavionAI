"""
Reusable active state model.

Provides an abstract active/inactive lifecycle flag for
DatavionOS business entities.
"""

from __future__ import annotations

from django.db import models


class ActiveModel(
    models.Model,
):
    """
    Abstract model providing active state management.

    Active state represents operational availability.

    This is independent from:
        - Soft deletion
        - Archiving
        - Suspension
        - Compliance retention

    Examples:

        Active:
            Entity can participate in business operations.

        Inactive:
            Entity is temporarily unavailable but retained.

    Business models should inherit from this model instead of
    defining their own active flag.
    """

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Active",
        help_text=("Indicates whether the entity is available for normal operations."),
    )

    class Meta:
        """
        Django model metadata.
        """

        abstract = True


__all__: tuple[str, ...] = ("ActiveModel",)
