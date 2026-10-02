"""
City reference model.

Provides global city master data for the DatavionOS platform.
"""

from __future__ import annotations

from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.platform.geography.models.country import Country
from apps.platform.geography.models.region import AdministrativeRegion


class City(
    BaseModel,
):
    """
    Global city reference data.

    Cities are platform-level master data and are intentionally
    not tenant-scoped.

    City names are descriptive attributes and are therefore not
    unique.

    Stable source identity is represented by:

        source + source_id

    A city belongs to a country and may optionally belong to a
    first-level administrative region.

    Lifecycle behavior is inherited from BaseModel:

        - UUID identity
        - timestamps
        - active/inactive state
        - soft deletion
    """

    source = models.CharField(
        _("Source"),
        max_length=50,
        default="countries-states-cities",
        help_text=_(
            "Identifier of the upstream geography data source.",
        ),
    )

    source_id = models.CharField(
        _("Source ID"),
        max_length=100,
        help_text=_(
            "Stable identifier assigned by the upstream data source.",
        ),
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="cities",
        verbose_name=_("Country"),
        help_text=_(
            "Country to which this city belongs.",
        ),
    )

    region = models.ForeignKey(
        AdministrativeRegion,
        on_delete=models.PROTECT,
        related_name="cities",
        null=True,
        blank=True,
        verbose_name=_("Administrative Region"),
        help_text=_(
            "First-level administrative region containing the city.",
        ),
    )

    name = models.CharField(
        _("City Name"),
        max_length=150,
        db_index=True,
        help_text=_(
            "Canonical city name.",
        ),
    )

    latitude = models.DecimalField(
        _("Latitude"),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(
                Decimal("-90"),
            ),
            MaxValueValidator(
                Decimal("90"),
            ),
        ],
        help_text=_(
            "Geographic latitude in decimal degrees.",
        ),
    )

    longitude = models.DecimalField(
        _("Longitude"),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(
                Decimal("-180"),
            ),
            MaxValueValidator(
                Decimal("180"),
            ),
        ],
        help_text=_(
            "Geographic longitude in decimal degrees.",
        ),
    )

    timezone = models.CharField(
        _("Timezone"),
        max_length=100,
        blank=True,
        help_text=_(
            "IANA timezone identifier for the city.",
        ),
    )

    sort_order = models.PositiveIntegerField(
        _("Sort Order"),
        default=0,
        help_text=_(
            "Display ordering within the administrative region.",
        ),
    )

    class Meta:
        db_table = "geography_cities"

        verbose_name = _("City")

        verbose_name_plural = _("Cities")

        ordering = (
            "country",
            "region",
            "sort_order",
            "name",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "source",
                    "source_id",
                ),
                name="uq_geo_city_source_source_id",
            ),
        ]

        indexes = [
            models.Index(
                fields=(
                    "country",
                    "is_active",
                ),
                name="idx_geo_city_country_active",
            ),
            models.Index(
                fields=(
                    "region",
                    "is_active",
                ),
                name="idx_geo_city_region_active",
            ),
            models.Index(
                fields=(
                    "country",
                    "name",
                ),
                name="idx_geo_city_country_name",
            ),
            models.Index(
                fields=(
                    "region",
                    "name",
                ),
                name="idx_geo_city_region_name",
            ),
            models.Index(
                fields=(
                    "source",
                    "source_id",
                ),
                name="idx_geo_city_source_id",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the human-readable city name.
        """

        return self.name


__all__: tuple[str, ...] = ("City",)
