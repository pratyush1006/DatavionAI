"""
Permission model for the RBAC app.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import TimeStampedModel


class Permission(TimeStampedModel):
    """
    Represents a permission that can be assigned to a role.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    code = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"

    def __str__(self) -> str:
        """
        Return the string representation of the permission.
        """
        return self.name
