"""
Administrative region reference model.

Provides global first-level administrative-region master data
for the DatavionOS platform.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.platform.geography.constants import (
    AdministrativeRegionType,
)
from apps.platform.geography.models.country import Country


class AdministrativeRegion(
    BaseModel,
):
    """
    Global administrative-region reference data.

    Regions are platform-level master data and are intentionally
    not tenant-scoped.

    Region identity is defined by:

        country + code

    Region names are descriptive attributes and are therefore not
    required to be unique within a country.
    """

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="regions",
        verbose_name=_("Country"),
        help_text=_(
            "Country to which this administrative region belongs.",
        ),
    )

    code = models.CharField(
        _("Region Code"),
        max_length=20,
        help_text=_(
            "Stable administrative-region code.",
        ),
    )

    name = models.CharField(
        _("Region Name"),
        max_length=150,
        help_text=_(
            "Canonical administrative-region name.",
        ),
    )

    region_type = models.CharField(
        _("Region Type"),
        max_length=30,
        choices=AdministrativeRegionType.choices,
        default=AdministrativeRegionType.STATE,
        help_text=_(
            "Administrative classification of the region.",
        ),
    )

    sort_order = models.PositiveIntegerField(
        _("Sort Order"),
        default=0,
        help_text=_(
            "Display ordering within the country.",
        ),
    )

    class Meta:
        db_table = "geography_regions"

        verbose_name = _("Administrative Region")

        verbose_name_plural = _("Administrative Regions")

        ordering = (
            "country",
            "sort_order",
            "name",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "country",
                    "code",
                ),
                name="uq_geo_region_country_code",
            ),
        ]

        indexes = [
            models.Index(
                fields=(
                    "country",
                    "is_active",
                ),
                name="idx_geo_region_country_active",
            ),
            models.Index(
                fields=(
                    "country",
                    "region_type",
                ),
                name="idx_geo_region_country_type",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the human-readable region name.
        """

        return self.name


__all__: tuple[str, ...] = ("AdministrativeRegion",)
