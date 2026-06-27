"""
Base model classes shared across DatavionAI.
"""

from __future__ import annotations

import uuid

from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract model providing automatic timestamp fields.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel):
    """
    Base model for all business entities.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        abstract = True
