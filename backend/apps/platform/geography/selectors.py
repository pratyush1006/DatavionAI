"""
Read-only selectors for the Geography application.

Geography is platform-level reference data.

Selectors are intentionally read-only and provide optimized access
for APIs, forms, workflows, and other platform services.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet

from apps.platform.geography.models import (
    AdministrativeRegion,
    City,
    Country,
)

type CountryQuerySet = QuerySet[Country]
type AdministrativeRegionQuerySet = QuerySet[AdministrativeRegion]
type CityQuerySet = QuerySet[City]


COUNTRY_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "code",
    "name",
    "iso3",
    "phone_code",
    "sort_order",
    "is_active",
)

REGION_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "country",
    "code",
    "name",
    "region_type",
    "sort_order",
    "is_active",
)

CITY_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "source",
    "source_id",
    "country",
    "region",
    "name",
    "latitude",
    "longitude",
    "timezone",
    "sort_order",
    "is_active",
)


def get_countries(
    *,
    include_inactive: bool = False,
) -> CountryQuerySet:
    """
    Return countries ordered for user-facing selection.
    """

    queryset = Country.objects.only(
        *COUNTRY_LIST_FIELDS,
    )

    if not include_inactive:
        queryset = queryset.filter(
            is_active=True,
        )

    return queryset.order_by(
        "sort_order",
        "name",
    )


def get_country_by_id(
    country_id,
) -> Country:
    """
    Return a country by primary key.
    """

    return get_countries().get(
        pk=country_id,
    )


def get_regions(
    *,
    country_id=None,
    include_inactive: bool = False,
) -> AdministrativeRegionQuerySet:
    """
    Return administrative regions.

    When ``country_id`` is supplied, results are restricted to
    that country.
    """

    queryset = AdministrativeRegion.objects.select_related(
        "country",
    ).only(
        *REGION_LIST_FIELDS,
        "country__id",
        "country__name",
        "country__code",
    )

    if country_id is not None:
        queryset = queryset.filter(
            country_id=country_id,
        )

    if not include_inactive:
        queryset = queryset.filter(
            is_active=True,
        )

    return queryset.order_by(
        "sort_order",
        "name",
    )


def get_region_by_id(
    region_id,
) -> AdministrativeRegion:
    """
    Return an administrative region by primary key.
    """

    return get_regions().get(
        pk=region_id,
    )


def get_cities(
    *,
    country_id=None,
    region_id=None,
    include_inactive: bool = False,
) -> CityQuerySet:
    """
    Return cities.

    Region filtering takes precedence when supplied.
    Country filtering can also be used independently.
    """

    queryset = City.objects.select_related(
        "country",
        "region",
    ).only(
        *CITY_LIST_FIELDS,
        "country__id",
        "country__name",
        "country__code",
        "region__id",
        "region__name",
        "region__code",
    )

    if country_id is not None:
        queryset = queryset.filter(
            country_id=country_id,
        )

    if region_id is not None:
        queryset = queryset.filter(
            region_id=region_id,
        )

    if not include_inactive:
        queryset = queryset.filter(
            is_active=True,
        )

    return queryset.order_by(
        "sort_order",
        "name",
    )


def get_city_by_id(
    city_id,
) -> City:
    """
    Return a city by primary key.
    """

    return get_cities().get(
        pk=city_id,
    )


__all__: tuple[str, ...] = (
    "AdministrativeRegionQuerySet",
    "CityQuerySet",
    "CountryQuerySet",
    "get_cities",
    "get_city_by_id",
    "get_countries",
    "get_country_by_id",
    "get_region_by_id",
    "get_regions",
)
