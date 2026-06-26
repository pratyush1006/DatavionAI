from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from apps.core.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    """
    Custom User model for Datavion AI.
    """

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    employee_id = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    department = models.CharField(
        max_length=100,
        blank=True,
    )

    designation = models.CharField(
        max_length=100,
        blank=True,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    is_active_employee = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.username


class OrganizationRole(models.Model):
    """
    Maps Django Groups to an Organization.
    """

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="roles",
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            "organization",
            "group",
        )

    def __str__(self):
        return f"{self.organization} - {self.group.name}"
