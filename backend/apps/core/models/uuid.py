"""
Reusable UUID primary key model.

Provides an abstract base model with a UUID primary key
for business models across the Datavion AI platform.
"""

from __future__ import annotations

import uuid

from django.db import models


class UUIDModel(
    models.Model,
):
    """
    Abstract model providing a UUID primary key.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        """
        Django model metadata.
        """

        abstract = True


__all__ = [
    "UUIDModel",
]
