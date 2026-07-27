"""
Reusable timestamp model.

Provides automatic lifecycle timestamps for DatavionOS
business entities.

This model is part of the core persistence layer and should
be inherited by domain models requiring creation and update
tracking.
"""

from __future__ import annotations

from django.db import models


class TimeStampedModel(
    models.Model,
):
    """
    Abstract timestamp model.

    Provides standardized lifecycle tracking fields.

    Fields:
        created_at:
            UTC timestamp generated when the record is created.

        updated_at:
            UTC timestamp automatically updated whenever the
            record changes.

    Design goals:
        - Consistent auditability
        - Reporting support
        - Event ordering
        - Healthcare compliance tracking

    Business models should inherit from this model instead of
    declaring timestamp fields independently.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        db_index=True,
        verbose_name="Created At",
        help_text=("Timestamp when the record was created."),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        db_index=True,
        verbose_name="Updated At",
        help_text=("Timestamp when the record was last updated."),
    )

    class Meta:
        """
        Django model metadata.
        """

        abstract = True


__all__: tuple[str, ...] = ("TimeStampedModel",)
