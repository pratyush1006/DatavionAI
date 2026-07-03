"""
Reusable UUID primary key model.

Provides a UUID primary key for all business models.
"""

from __future__ import annotations

import uuid

from django.db import models


class UUIDModel(models.Model):
    """
    Abstract model providing a UUID primary key.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True
