"""
Role model for the RBAC app.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import TimeStampedModel


class Role(TimeStampedModel):
    """
    Represents a business role within Datavion AI.
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
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ("name",)

    def __str__(self) -> str:
        """
        Return the string representation of the role.
        """
        return self.name
