"""
Reusable timestamp model.

Provides automatic creation and modification timestamps
for business models across the Datavion AI platform.
"""

from __future__ import annotations

from django.db import models


class TimeStampedModel(
    models.Model,
):
    """
    Abstract model providing automatic timestamp fields.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        """
        Django model metadata.
        """

        abstract = True


__all__ = [
    "TimeStampedModel",
]
