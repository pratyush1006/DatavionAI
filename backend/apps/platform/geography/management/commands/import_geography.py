"""
Import geography master data into DatavionOS.

The importer accepts the Country State City Database JSON export
and imports the following normalized platform reference layers:

    Country
        |
        +-- AdministrativeRegion
                |
                +-- City

The upstream dataset remains the source authority.

DatavionOS maintains its own normalized reference tables and
uses stable upstream identities for idempotent synchronization.

Supported source formats:

    - JSON
    - JSON.GZ

Import behavior:

    - validates the complete dataset before database writes
    - imports countries first
    - imports regions second
    - imports cities third
    - performs all writes inside one database transaction
    - is idempotent
    - reactivates records present in the current source
    - never deletes records missing from the source
    - supports dry-run validation
"""

from __future__ import annotations

import gzip
import json
from collections.abc import Iterable
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.platform.geography.constants import (
    AdministrativeRegionType,
)
from apps.platform.geography.models import (
    AdministrativeRegion,
    City,
    Country,
)

DEFAULT_CITY_SOURCE = "countries-states-cities"

MAX_CITY_SOURCE_ID_LENGTH = 100
MAX_CITY_TIMEZONE_LENGTH = 100


class Command(
    BaseCommand,
):
    """
    Import countries, administrative regions, and cities.
    """

    help = (
        "Import country, administrative-region, and city master data "
        "from a JSON or JSON.GZ geography dataset."
    )

    def add_arguments(
        self,
        parser,
    ) -> None:
        parser.add_argument(
            "--source",
            required=True,
            help=("Path to the geography JSON or JSON.GZ dataset."),
        )

        parser.add_argument(
            "--dry-run",
            action="store_true",
            help=("Validate the dataset without writing to the database."),
        )

    def handle(
        self,
        *args,
        **options,
    ) -> None:
        source = Path(
            options["source"],
        )

        dry_run = bool(
            options.get("dry_run"),
        )

        self._validate_source(
            source,
        )

        self.stdout.write(
            f"Loading geography dataset: {source}",
        )

        payload = self._load_json(
            source,
        )

        countries = self._extract_countries(
            payload,
        )

        prepared_countries = self._prepare_countries(
            countries,
        )

        prepared_regions = self._prepare_regions(
            countries,
        )

        prepared_cities = self._prepare_cities(
            countries,
        )

        self._validate_prepared_data(
            prepared_countries,
            prepared_regions,
            prepared_cities,
        )

        if dry_run:
            self._write_dry_run_summary(
                prepared_countries,
                prepared_regions,
                prepared_cities,
            )
            return

        (
            country_stats,
            region_stats,
            city_stats,
        ) = self._persist(
            prepared_countries,
            prepared_regions,
            prepared_cities,
        )

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Geography import completed successfully. "
                    f"countries(created={country_stats['created']}, "
                    f"updated={country_stats['updated']}), "
                    f"regions(created={region_stats['created']}, "
                    f"updated={region_stats['updated']}), "
                    f"cities(created={city_stats['created']}, "
                    f"updated={city_stats['updated']})"
                ),
            ),
        )

    # ------------------------------------------------------------------
    # Source loading
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_source(
        source: Path,
    ) -> None:
        """
        Validate the source file before loading it.
        """

        if not source.exists():
            raise CommandError(
                f"Geography source file does not exist: {source}",
            )

        if not source.is_file():
            raise CommandError(
                f"Geography source is not a file: {source}",
            )

        if source.suffix.lower() not in {
            ".json",
            ".gz",
        }:
            raise CommandError(
                "Unsupported geography source format. Expected .json or .json.gz.",
            )

    @staticmethod
    def _load_json(
        source: Path,
    ) -> Any:
        """
        Load a JSON or gzip-compressed JSON source.
        """

        if source.name.lower().endswith(
            ".json.gz",
        ):
            with gzip.open(
                source,
                mode="rt",
                encoding="utf-8",
            ) as file:
                return json.load(
                    file,
                )

        with source.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            return json.load(
                file,
            )

    @staticmethod
    def _extract_countries(
        payload: Any,
    ) -> list[dict[str, Any]]:
        """
        Extract the country collection from supported JSON envelopes.
        """

        if isinstance(
            payload,
            list,
        ):
            countries = payload

        elif isinstance(
            payload,
            dict,
        ):
            countries = payload.get(
                "countries",
            )

            if countries is None:
                countries = payload.get(
                    "data",
                )

        else:
            countries = None

        if not isinstance(
            countries,
            list,
        ):
            raise CommandError(
                "Invalid geography dataset: expected a country list.",
            )

        normalized: list[dict[str, Any]] = []

        for index, country in enumerate(
            countries,
            start=1,
        ):
            if not isinstance(
                country,
                dict,
            ):
                raise CommandError(
                    f"Invalid country record at index {index}.",
                )

            normalized.append(
                country,
            )

        return normalized

    # ------------------------------------------------------------------
    # Country preparation
    # ------------------------------------------------------------------

    @classmethod
    def _prepare_countries(
        cls,
        countries: Iterable[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Translate upstream country records into DatavionOS fields.
        """

        prepared: list[dict[str, Any]] = []

        for position, country in enumerate(
            countries,
            start=1,
        ):
            code = cls._clean(
                country.get(
                    "iso2",
                ),
            ).upper()

            iso3 = cls._clean(
                country.get(
                    "iso3",
                ),
            ).upper()

            name = cls._clean(
                country.get(
                    "name",
                ),
            )

            # The actual Country State City Database export uses
            # "phonecode". Keep "phone_code" as a compatibility
            # fallback for synthetic/test datasets.
            phone_code = cls._clean(
                country.get(
                    "phonecode",
                ),
            )

            if not phone_code:
                phone_code = cls._clean(
                    country.get(
                        "phone_code",
                    ),
                )

            if not code:
                raise CommandError(
                    f"Country record {position} is missing iso2.",
                )

            if len(code) != 2:
                raise CommandError(
                    (
                        f"Country record {position} has invalid iso2 "
                        f"'{code}'. Expected exactly two characters."
                    ),
                )

            if not name:
                raise CommandError(
                    f"Country record {position} is missing name.",
                )

            if not iso3:
                raise CommandError(
                    f"Country '{code}' is missing iso3.",
                )

            if len(iso3) != 3:
                raise CommandError(
                    (
                        f"Country '{code}' has invalid iso3 '{iso3}'. "
                        "Expected exactly three characters."
                    ),
                )

            if len(phone_code) > 10:
                raise CommandError(
                    (f"Country '{code}' phone code exceeds 10 characters."),
                )

            prepared.append(
                {
                    "code": code,
                    "name": name,
                    "iso3": iso3,
                    "phone_code": phone_code,
                    "sort_order": position,
                },
            )

        return prepared

    # ------------------------------------------------------------------
    # Region preparation
    # ------------------------------------------------------------------

    @classmethod
    def _prepare_regions(
        cls,
        countries: Iterable[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Translate upstream state records into DatavionOS regions.

        Region identity is:

            country + stable upstream region code

        Region names are descriptive and may repeat.
        """

        prepared: list[dict[str, Any]] = []

        sort_orders: dict[str, int] = {}

        for country in countries:
            country_code = cls._clean(
                country.get(
                    "iso2",
                ),
            ).upper()

            if not country_code:
                continue

            states = country.get(
                "states",
            )

            if not isinstance(
                states,
                list,
            ):
                continue

            sort_orders.setdefault(
                country_code,
                0,
            )

            for state in states:
                if not isinstance(
                    state,
                    dict,
                ):
                    raise CommandError(
                        (f"Invalid region record for country '{country_code}'."),
                    )

                name = cls._clean(
                    state.get(
                        "name",
                    ),
                )

                if not name:
                    raise CommandError(
                        (f"Region for country '{country_code}' is missing name."),
                    )

                code = cls._region_code(
                    state,
                )

                if not code:
                    raise CommandError(
                        (
                            f"Region '{name}' for country "
                            f"'{country_code}' has no usable code."
                        ),
                    )

                if len(code) > 20:
                    raise CommandError(
                        (
                            f"Region code '{code}' for country "
                            f"'{country_code}' exceeds 20 characters."
                        ),
                    )

                sort_orders[country_code] += 1

                prepared.append(
                    {
                        "country_code": country_code,
                        "code": code,
                        "name": name,
                        "region_type": cls._region_type(
                            state.get(
                                "type",
                            ),
                        ),
                        "sort_order": sort_orders[country_code],
                    },
                )

        return prepared

    # ------------------------------------------------------------------
    # City preparation
    # ------------------------------------------------------------------

    @classmethod
    def _prepare_cities(
        cls,
        countries: Iterable[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Translate upstream city records into DatavionOS fields.

        The Country State City Database stores cities nested under
        their first-level administrative region.

        City identity is:

            source + source_id

        City names are descriptive and are not unique.
        """

        prepared: list[dict[str, Any]] = []

        city_sort_orders: dict[
            tuple[str, str],
            int,
        ] = {}

        for country in countries:
            country_code = cls._clean(
                country.get(
                    "iso2",
                ),
            ).upper()

            if not country_code:
                continue

            states = country.get(
                "states",
            )

            if not isinstance(
                states,
                list,
            ):
                continue

            for state in states:
                if not isinstance(
                    state,
                    dict,
                ):
                    raise CommandError(
                        (
                            f"Invalid region record for city import "
                            f"under country '{country_code}'."
                        ),
                    )

                region_code = cls._region_code(
                    state,
                )

                if not region_code:
                    raise CommandError(
                        (
                            f"Region '{state.get('name', '')}' for "
                            f"country '{country_code}' has no usable "
                            "code and therefore cannot own cities."
                        ),
                    )

                cities = state.get(
                    "cities",
                )

                if cities is None:
                    continue

                if not isinstance(
                    cities,
                    list,
                ):
                    raise CommandError(
                        (
                            f"Cities for region '{state.get('name', '')}' "
                            f"in country '{country_code}' must be a list."
                        ),
                    )

                region_key = (
                    country_code,
                    region_code.casefold(),
                )

                city_sort_orders.setdefault(
                    region_key,
                    0,
                )

                for city in cities:
                    if not isinstance(
                        city,
                        dict,
                    ):
                        raise CommandError(
                            (
                                f"Invalid city record for region "
                                f"'{state.get('name', '')}' in country "
                                f"'{country_code}'."
                            ),
                        )

                    source_id = cls._clean(
                        city.get(
                            "id",
                        ),
                    )

                    if not source_id:
                        raise CommandError(
                            (
                                f"City under region "
                                f"'{state.get('name', '')}' in country "
                                f"'{country_code}' is missing id."
                            ),
                        )

                    if len(source_id) > MAX_CITY_SOURCE_ID_LENGTH:
                        raise CommandError(
                            (
                                f"City source id '{source_id}' exceeds "
                                f"{MAX_CITY_SOURCE_ID_LENGTH} characters."
                            ),
                        )

                    name = cls._clean(
                        city.get(
                            "name",
                        ),
                    )

                    if not name:
                        raise CommandError(
                            (
                                f"City '{source_id}' under region "
                                f"'{state.get('name', '')}' in country "
                                f"'{country_code}' is missing name."
                            ),
                        )

                    latitude = cls._coordinate(
                        city.get(
                            "latitude",
                        ),
                        minimum=Decimal("-90"),
                        maximum=Decimal("90"),
                        field_name="latitude",
                        city_name=name,
                        source_id=source_id,
                    )

                    longitude = cls._coordinate(
                        city.get(
                            "longitude",
                        ),
                        minimum=Decimal("-180"),
                        maximum=Decimal("180"),
                        field_name="longitude",
                        city_name=name,
                        source_id=source_id,
                    )

                    timezone = cls._clean(
                        city.get(
                            "timezone",
                        ),
                    )

                    if len(timezone) > MAX_CITY_TIMEZONE_LENGTH:
                        raise CommandError(
                            (
                                f"Timezone '{timezone}' for city "
                                f"'{name}' exceeds "
                                f"{MAX_CITY_TIMEZONE_LENGTH} characters."
                            ),
                        )

                    city_sort_orders[region_key] += 1

                    prepared.append(
                        {
                            "source": DEFAULT_CITY_SOURCE,
                            "source_id": source_id,
                            "country_code": country_code,
                            "region_code": region_code,
                            "name": name,
                            "latitude": latitude,
                            "longitude": longitude,
                            "timezone": timezone,
                            "sort_order": city_sort_orders[region_key],
                        },
                    )

        return prepared

    # ------------------------------------------------------------------
    # Dataset validation
    # ------------------------------------------------------------------

    @classmethod
    def _validate_prepared_data(
        cls,
        countries: list[dict[str, Any]],
        regions: list[dict[str, Any]],
        cities: list[dict[str, Any]],
    ) -> None:
        """
        Validate complete dataset integrity before database writes.

        Country identity:

            ISO2

        Region identity:

            country + region code

        City identity:

            source + source id

        City names may repeat.
        """

        country_codes: set[str] = set()
        country_names: set[str] = set()
        country_iso3: set[str] = set()

        for country in countries:
            code = country["code"]
            name = country["name"]
            iso3 = country["iso3"]

            if code in country_codes:
                raise CommandError(
                    f"Duplicate country code in dataset: {code}",
                )

            if name.casefold() in country_names:
                raise CommandError(
                    f"Duplicate country name in dataset: {name}",
                )

            if iso3 in country_iso3:
                raise CommandError(
                    f"Duplicate country iso3 in dataset: {iso3}",
                )

            country_codes.add(
                code,
            )

            country_names.add(
                name.casefold(),
            )

            country_iso3.add(
                iso3,
            )

        region_keys: set[tuple[str, str]] = set()

        for region in regions:
            country_code = region["country_code"]
            code = region["code"]

            if country_code not in country_codes:
                raise CommandError(
                    (
                        f"Region '{region['name']}' references "
                        f"unknown country '{country_code}'."
                    ),
                )

            key = (
                country_code,
                code.casefold(),
            )

            if key in region_keys:
                raise CommandError(
                    (f"Duplicate region code '{code}' for country '{country_code}'."),
                )

            region_keys.add(
                key,
            )

        city_keys: set[tuple[str, str]] = set()

        for city in cities:
            source = city["source"]
            source_id = city["source_id"]

            country_code = city["country_code"]
            region_code = city["region_code"]

            if country_code not in country_codes:
                raise CommandError(
                    (
                        f"City '{city['name']}' references unknown "
                        f"country '{country_code}'."
                    ),
                )

            region_key = (
                country_code,
                region_code.casefold(),
            )

            if region_key not in region_keys:
                raise CommandError(
                    (
                        f"City '{city['name']}' references unknown "
                        f"region '{region_code}' for country "
                        f"'{country_code}'."
                    ),
                )

            city_key = (
                source,
                source_id.casefold(),
            )

            if city_key in city_keys:
                raise CommandError(
                    (f"Duplicate city source identity '{source}:{source_id}'."),
                )

            city_keys.add(
                city_key,
            )

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    @staticmethod
    def _persist(
        countries: list[dict[str, Any]],
        regions: list[dict[str, Any]],
        cities: list[dict[str, Any]],
    ) -> tuple[
        dict[str, int],
        dict[str, int],
        dict[str, int],
    ]:
        """
        Persist countries, regions, and cities atomically.

        Uses all_objects so soft-deleted reference records can be
        reactivated when they are present in the current upstream source.
        """

        country_stats = {
            "created": 0,
            "updated": 0,
        }

        region_stats = {
            "created": 0,
            "updated": 0,
        }

        city_stats = {
            "created": 0,
            "updated": 0,
        }

        with transaction.atomic():
            country_map: dict[str, Country] = {}

            for item in countries:
                country, created = Country.all_objects.update_or_create(
                    code=item["code"],
                    defaults={
                        "name": item["name"],
                        "iso3": item["iso3"],
                        "phone_code": item["phone_code"],
                        "sort_order": item["sort_order"],
                        "is_active": True,
                    },
                )

                if not created and country.is_deleted:
                    country.restore()

                country_map[country.code] = country

                if created:
                    country_stats["created"] += 1
                else:
                    country_stats["updated"] += 1

            region_map: dict[
                tuple[str, str],
                AdministrativeRegion,
            ] = {}

            for item in regions:
                country = country_map[item["country_code"]]

                region, created = AdministrativeRegion.all_objects.update_or_create(
                    country=country,
                    code=item["code"],
                    defaults={
                        "name": item["name"],
                        "region_type": item["region_type"],
                        "sort_order": item["sort_order"],
                        "is_active": True,
                    },
                )

                if not created and region.is_deleted:
                    region.restore()

                region_map[
                    (
                        country.code,
                        region.code.casefold(),
                    )
                ] = region

                if created:
                    region_stats["created"] += 1
                else:
                    region_stats["updated"] += 1

            for item in cities:
                country = country_map[item["country_code"]]

                region = region_map.get(
                    (
                        item["country_code"],
                        item["region_code"].casefold(),
                    ),
                )

                if region is None:
                    raise CommandError(
                        (
                            f"Unable to resolve region "
                            f"'{item['region_code']}' for country "
                            f"'{item['country_code']}' while persisting "
                            f"city '{item['name']}'."
                        ),
                    )

                city, created = City.all_objects.update_or_create(
                    source=item["source"],
                    source_id=item["source_id"],
                    defaults={
                        "country": country,
                        "region": region,
                        "name": item["name"],
                        "latitude": item["latitude"],
                        "longitude": item["longitude"],
                        "timezone": item["timezone"],
                        "sort_order": item["sort_order"],
                        "is_active": True,
                    },
                )

                if not created and city.is_deleted:
                    city.restore()

                if created:
                    city_stats["created"] += 1
                else:
                    city_stats["updated"] += 1

        return (
            country_stats,
            region_stats,
            city_stats,
        )

    # ------------------------------------------------------------------
    # Dry-run
    # ------------------------------------------------------------------

    def _write_dry_run_summary(
        self,
        countries: list[dict[str, Any]],
        regions: list[dict[str, Any]],
        cities: list[dict[str, Any]],
    ) -> None:
        """
        Write validation-only import statistics.
        """

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Geography dry-run validation passed. "
                    f"countries={len(countries)}, "
                    f"regions={len(regions)}, "
                    f"cities={len(cities)}"
                ),
            ),
        )

    # ------------------------------------------------------------------
    # Region helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _region_code(
        state: dict[str, Any],
    ) -> str:
        """
        Select the most stable available upstream region identifier.
        """

        for field in (
            "iso2",
            "state_code",
        ):
            value = Command._clean(
                state.get(
                    field,
                ),
            )

            if value:
                return value.upper()

        upstream_id = state.get(
            "id",
        )

        if upstream_id is None:
            return ""

        return f"up-{upstream_id}"

    @staticmethod
    def _region_type(
        value: Any,
    ) -> str:
        """
        Normalize upstream region types into DatavionOS choices.
        """

        normalized = Command._clean(
            value,
        ).casefold()

        if not normalized:
            return AdministrativeRegionType.STATE

        mapping = {
            "state": AdministrativeRegionType.STATE,
            "states": AdministrativeRegionType.STATE,
            "province": AdministrativeRegionType.PROVINCE,
            "provinces": AdministrativeRegionType.PROVINCE,
            "territory": AdministrativeRegionType.TERRITORY,
            "territories": AdministrativeRegionType.TERRITORY,
            "region": AdministrativeRegionType.REGION,
            "regions": AdministrativeRegionType.REGION,
            "district": AdministrativeRegionType.DISTRICT,
            "districts": AdministrativeRegionType.DISTRICT,
            "autonomous region": AdministrativeRegionType.REGION,
            "autonomous province": AdministrativeRegionType.PROVINCE,
            "special municipality": AdministrativeRegionType.REGION,
            "metropolitan city": AdministrativeRegionType.REGION,
        }

        return mapping.get(
            normalized,
            AdministrativeRegionType.REGION,
        )

    # ------------------------------------------------------------------
    # City helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _coordinate(
        value: Any,
        *,
        minimum: Decimal,
        maximum: Decimal,
        field_name: str,
        city_name: str,
        source_id: str,
    ) -> Decimal | None:
        """
        Normalize and validate a geographic coordinate.

        Coordinates are stored at six decimal places because the City
        model uses DecimalField(decimal_places=6).
        """

        normalized = Command._clean(
            value,
        )

        if not normalized:
            return None

        try:
            coordinate = Decimal(
                normalized,
            )
        except (
            InvalidOperation,
            ValueError,
        ) as exc:
            raise CommandError(
                (
                    f"City '{city_name}' ({source_id}) has invalid "
                    f"{field_name} '{normalized}'."
                ),
            ) from exc

        if not coordinate.is_finite():
            raise CommandError(
                (
                    f"City '{city_name}' ({source_id}) has non-finite "
                    f"{field_name} '{normalized}'."
                ),
            )

        if coordinate < minimum or coordinate > maximum:
            raise CommandError(
                (
                    f"City '{city_name}' ({source_id}) has {field_name} "
                    f"'{normalized}' outside the valid range "
                    f"{minimum} to {maximum}."
                ),
            )

        return coordinate.quantize(
            Decimal("0.000001"),
        )

    # ------------------------------------------------------------------
    # Generic helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _clean(
        value: Any,
    ) -> str:
        """
        Normalize an arbitrary source value to stripped text.
        """

        if value is None:
            return ""

        return str(
            value,
        ).strip()


__all__ = [
    "Command",
]
