"""
Organization settings model.

Stores organization-level configuration used by
DatavionOS applications.

This model contains organization-specific preferences
for localization, notifications, security, and
dashboard behavior.
"""

from __future__ import annotations

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class OrganizationSettings(
    BaseModel,
):
    """
    Configuration settings for an organization.

    Relationship:

        Organization
              │
              ▼
    OrganizationSettings

    One organization owns exactly one settings record.
    """

    # ------------------------------------------------------------------
    # Organization
    # ------------------------------------------------------------------

    organization = models.OneToOneField(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="settings",
        verbose_name=_("Organization"),
        help_text=_(
            "Organization these settings belong to.",
        ),
    )

    # ------------------------------------------------------------------
    # Localization
    # ------------------------------------------------------------------

    language = models.CharField(
        max_length=20,
        default="en",
        db_index=True,
        verbose_name=_("Language"),
        help_text=_(
            "Default language for the organization.",
        ),
    )

    timezone = models.CharField(
        max_length=100,
        default="Asia/Kolkata",
        db_index=True,
        verbose_name=_("Timezone"),
        help_text=_(
            "Default organization timezone.",
        ),
    )

    currency = models.CharField(
        max_length=10,
        default="INR",
        db_index=True,
        verbose_name=_("Currency"),
        help_text=_(
            "Default organization currency.",
        ),
    )

    date_format = models.CharField(
        max_length=50,
        default="DD-MM-YYYY",
        verbose_name=_("Date Format"),
        help_text=_(
            "Default date display format.",
        ),
    )

    time_format = models.CharField(
        max_length=50,
        default="24H",
        verbose_name=_("Time Format"),
        help_text=_(
            "Default time display format.",
        ),
    )

    # ------------------------------------------------------------------
    # Notifications
    # ------------------------------------------------------------------

    email_notifications = models.BooleanField(
        default=True,
        verbose_name=_("Email Notifications"),
        help_text=_(
            "Enable email notifications.",
        ),
    )

    sms_notifications = models.BooleanField(
        default=True,
        verbose_name=_("SMS Notifications"),
        help_text=_(
            "Enable SMS notifications.",
        ),
    )

    push_notifications = models.BooleanField(
        default=True,
        verbose_name=_("Push Notifications"),
        help_text=_(
            "Enable push notifications.",
        ),
    )

    # ------------------------------------------------------------------
    # Security
    # ------------------------------------------------------------------

    session_timeout_minutes = models.PositiveIntegerField(
        default=60,
        validators=[
            MinValueValidator(5),
            MaxValueValidator(1440),
        ],
        verbose_name=_("Session Timeout"),
        help_text=_(
            "User session timeout in minutes.",
        ),
    )

    mfa_required = models.BooleanField(
        default=False,
        verbose_name=_("MFA Required"),
        help_text=_(
            "Require multi-factor authentication for organization users.",
        ),
    )

    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------

    default_dashboard = models.CharField(
        max_length=100,
        default="main",
        verbose_name=_("Default Dashboard"),
        help_text=_(
            "Default dashboard configuration identifier.",
        ),
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_settings"

        verbose_name = _(
            "Organization Settings",
        )

        verbose_name_plural = _(
            "Organization Settings",
        )

        ordering = ("organization",)

    def __str__(
        self,
    ) -> str:
        """
        Return the string representation.
        """

        return f"Settings - {self.organization}"


__all__ = ("OrganizationSettings",)
