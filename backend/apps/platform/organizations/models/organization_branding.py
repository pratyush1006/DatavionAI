"""
Organization branding model.

Stores organization-level branding configuration
for the DatavionAI platform.
"""

from __future__ import annotations

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.platform.organizations.constants import (
    DEFAULT_ORGANIZATION_BRANDING_FONT_FAMILY,
    DEFAULT_ORGANIZATION_BRANDING_PRIMARY_COLOR,
    DEFAULT_ORGANIZATION_BRANDING_THEME_MODE,
    OrganizationBrandingThemeMode,
)
from apps.platform.organizations.managers import (
    OrganizationBrandingManager,
)

hex_color_validator = RegexValidator(
    regex=r"^#[0-9A-Fa-f]{6}$",
    message="Enter a valid HEX color value.",
)


class OrganizationBranding(
    BaseModel,
):
    """
    Organization branding configuration.

    Each organization can customize:
    - Logo
    - Colors
    - Typography
    - Theme preference
    """

    organization = models.OneToOneField(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="branding",
        verbose_name=_("Organization"),
    )

    logo = models.ImageField(
        upload_to="organizations/branding/logos/",
        null=True,
        blank=True,
        verbose_name=_("Logo"),
    )

    favicon = models.ImageField(
        upload_to="organizations/branding/favicons/",
        null=True,
        blank=True,
        verbose_name=_("Favicon"),
    )

    primary_color = models.CharField(
        max_length=7,
        default=(DEFAULT_ORGANIZATION_BRANDING_PRIMARY_COLOR),
        validators=[
            hex_color_validator,
        ],
        verbose_name=_("Primary color"),
    )

    font_family = models.CharField(
        max_length=100,
        default=(DEFAULT_ORGANIZATION_BRANDING_FONT_FAMILY),
        verbose_name=_("Font family"),
    )

    theme_mode = models.CharField(
        max_length=20,
        choices=(OrganizationBrandingThemeMode.choices()),
        default=(DEFAULT_ORGANIZATION_BRANDING_THEME_MODE),
        verbose_name=_("Theme mode"),
    )

    custom_css = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Custom CSS"),
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Metadata"),
    )

    objects = OrganizationBrandingManager()

    class Meta:
        """
        Model metadata.
        """

        db_table = "organization_branding"

        verbose_name = "Organization branding"

        verbose_name_plural = "Organization brandings"

        ordering = ("-created_at",)

    def __str__(
        self,
    ) -> str:
        return f"{self.organization.name} branding"


__all__: tuple[str, ...] = ("OrganizationBranding",)
