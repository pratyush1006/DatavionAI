"""
Reusable active/inactive model mixin.
"""

from __future__ import annotations

from django.db import models


class ActiveMixin(models.Model):
    """
    Abstract model providing an active/inactive flag.

    Models inheriting from this mixin can be enabled or
    disabled without being deleted.
    """

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        abstract = True
