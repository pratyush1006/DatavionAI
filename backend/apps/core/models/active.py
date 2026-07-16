"""
Reusable active/inactive model.

Provides an abstract model with an active/inactive flag
for business models across the Datavion AI platform.
"""

from __future__ import annotations

from django.db import models


class ActiveModel(
    models.Model,
):
    """
    Abstract model providing an active/inactive flag.

    Models inheriting from this class can be enabled or
    disabled without being deleted.
    """

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        """
        Django model metadata.
        """

        abstract = True


__all__ = [
    "ActiveModel",
]
