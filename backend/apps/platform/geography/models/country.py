"""
Country reference model.

Provides global country master data for the DatavionOS platform.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Country(
    BaseModel,
):
    """
    Global country reference data.

    Countries are platform-level master data and are intentionally
    not tenant-scoped.

    Lifecycle behavior is inherited from BaseModel:

        - UUID identity
        - timestamps
        - active/inactive state
        - soft deletion

    Country records should normally be deactivated rather than
    physically removed.
    """

    code = models.CharField(
        _("Country Code"),
        max_length=2,
        unique=True,
        help_text=_(
            "ISO 3166-1 alpha-2 country code.",
        ),
    )

    name = models.CharField(
        _("Country Name"),
        max_length=100,
        unique=True,
        db_index=True,
        help_text=_(
            "Canonical country name.",
        ),
    )

    iso3 = models.CharField(
        _("ISO 3 Code"),
        max_length=3,
        unique=True,
        help_text=_(
            "ISO 3166-1 alpha-3 country code.",
        ),
    )

    phone_code = models.CharField(
        _("Phone Code"),
        max_length=10,
        blank=True,
        help_text=_(
            "International telephone dialing code.",
        ),
    )

    sort_order = models.PositiveIntegerField(
        _("Sort Order"),
        default=0,
        help_text=_(
            "Display ordering for country selectors.",
        ),
    )

    class Meta:
        db_table = "geography_countries"

        verbose_name = _("Country")

        verbose_name_plural = _("Countries")

        ordering = (
            "sort_order",
            "name",
        )

        indexes = [
            models.Index(
                fields=(
                    "is_active",
                    "name",
                ),
                name="idx_geo_country_active_name",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the canonical country name.
        """

        return self.name


__all__: tuple[str, ...] = ("Country",)
