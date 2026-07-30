"""
Department settings model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel


class DepartmentSetting(BaseModel):
    """
    Department configuration.
    """

    department = models.OneToOneField(
        "departments.Department",
        on_delete=models.CASCADE,
        related_name="department_settings",
    )

    configuration = models.JSONField(
        default=dict,
        blank=True,
    )

    is_locked = models.BooleanField(
        default=False,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    def __str__(self):
        return f"Settings - {self.department}"


__all__ = ("DepartmentSetting",)
