"""
Tests for the geography import management command.

Coverage includes:

    - country creation
    - region creation
    - city creation
    - city coordinates
    - city timezone
    - idempotent imports
    - country updates
    - region updates
    - city updates
    - duplicate region names with different codes
    - duplicate region codes
    - duplicate city source IDs
    - invalid city coordinates
    - dry-run behavior
    - soft-delete restoration
    - invalid country codes
    - invalid country ISO3 codes
    - missing country names
    - missing region names
    - missing region codes
    - missing city names
    - missing city IDs
    - unknown country references
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from apps.platform.geography.models import (
    AdministrativeRegion,
    City,
    Country,
)


class ImportGeographyCommandTests(TestCase):
    """
    Test Geography import behavior.
    """

    def setUp(self) -> None:
        """
        Create an isolated temporary source directory.
        """

        self._temporary_directory = tempfile.TemporaryDirectory(
            prefix="datavion-geography-",
        )

        self._test_source_path = (
            Path(
                self._temporary_directory.name,
            )
            / "geography.json"
        )

    def tearDown(self) -> None:
        """
        Remove the temporary source directory.
        """

        self._temporary_directory.cleanup()

        super().tearDown()

    def _write_dataset(
        self,
        payload: Any,
    ) -> Path:
        """
        Write a JSON dataset to the temporary source path.
        """

        self._test_source_path.write_text(
            json.dumps(payload),
            encoding="utf-8",
        )

        return self._test_source_path

    def _run_import(
        self,
        *,
        dry_run: bool = False,
    ) -> None:
        """
        Execute the geography import command.
        """

        call_command(
            "import_geography",
            source=str(
                self._test_source_path,
            ),
            dry_run=dry_run,
        )

    def _india_dataset(
        self,
        *,
        country_name: str = "India",
        region_name: str = "Bihar",
        city_name: str = "Patna",
        city_id: int = 1001,
        city_timezone: str = "Asia/Kolkata",
        latitude: str = "25.59410000",
        longitude: str = "85.13760000",
    ) -> list[dict[str, Any]]:
        """
        Build a small realistic India dataset for tests.
        """

        return [
            {
                "id": 1,
                "name": country_name,
                "iso2": "IN",
                "iso3": "IND",
                "phone_code": "+91",
                "states": [
                    {
                        "id": 101,
                        "name": region_name,
                        "iso2": "BR",
                        "type": "state",
                        "cities": [
                            {
                                "id": city_id,
                                "name": city_name,
                                "latitude": latitude,
                                "longitude": longitude,
                                "timezone": city_timezone,
                            },
                        ],
                    },
                ],
            },
        ]

    def test_import_creates_country_region_and_city(self) -> None:
        """
        A valid dataset creates country, region, and city records.
        """

        source = self._write_dataset(
            self._india_dataset(),
        )

        call_command(
            "import_geography",
            source=str(source),
        )

        country = Country.objects.get(
            code="IN",
        )

        self.assertEqual(
            country.name,
            "India",
        )

        self.assertEqual(
            country.iso3,
            "IND",
        )

        self.assertEqual(
            country.phone_code,
            "+91",
        )

        region = AdministrativeRegion.objects.get(
            country=country,
            code="BR",
        )

        self.assertEqual(
            region.name,
            "Bihar",
        )

        self.assertEqual(
            region.region_type,
            "state",
        )

        self.assertTrue(
            region.is_active,
        )

        city = City.objects.get(
            source="countries-states-cities",
            source_id="1001",
        )

        self.assertEqual(
            city.country,
            country,
        )

        self.assertEqual(
            city.region,
            region,
        )

        self.assertEqual(
            city.name,
            "Patna",
        )

        self.assertEqual(
            str(city.latitude),
            "25.594100",
        )

        self.assertEqual(
            str(city.longitude),
            "85.137600",
        )

        self.assertEqual(
            city.timezone,
            "Asia/Kolkata",
        )

        self.assertTrue(
            city.is_active,
        )

    def test_import_is_idempotent(self) -> None:
        """
        Importing the same dataset twice does not create duplicates.
        """

        source = self._write_dataset(
            self._india_dataset(),
        )

        call_command(
            "import_geography",
            source=str(source),
        )

        call_command(
            "import_geography",
            source=str(source),
        )

        self.assertEqual(
            Country.objects.count(),
            1,
        )

        self.assertEqual(
            AdministrativeRegion.objects.count(),
            1,
        )

        self.assertEqual(
            City.objects.count(),
            1,
        )

        city = City.objects.get(
            source="countries-states-cities",
            source_id="1001",
        )

        self.assertEqual(
            city.name,
            "Patna",
        )

    def test_import_updates_existing_country_region_and_city(self) -> None:
        """
        Re-importing changed source data updates existing records.
        """

        source = self._write_dataset(
            self._india_dataset(),
        )

        self._run_import()

        source = self._write_dataset(
            self._india_dataset(
                country_name="Republic of India",
                region_name="Bihar State",
                city_name="Patna City",
                city_timezone="Asia/Kolkata",
                latitude="25.60000000",
                longitude="85.15000000",
            ),
        )

        self._run_import()

        country = Country.objects.get(
            code="IN",
        )

        region = AdministrativeRegion.objects.get(
            country=country,
            code="BR",
        )

        city = City.objects.get(
            source="countries-states-cities",
            source_id="1001",
        )

        self.assertEqual(
            country.name,
            "Republic of India",
        )

        self.assertEqual(
            region.name,
            "Bihar State",
        )

        self.assertEqual(
            city.name,
            "Patna City",
        )

        self.assertEqual(
            str(city.latitude),
            "25.600000",
        )

        self.assertEqual(
            str(city.longitude),
            "85.150000",
        )

        self.assertEqual(
            city.timezone,
            "Asia/Kolkata",
        )

        self.assertEqual(
            Country.objects.count(),
            1,
        )

        self.assertEqual(
            AdministrativeRegion.objects.count(),
            1,
        )

        self.assertEqual(
            City.objects.count(),
            1,
        )

    def test_import_restores_soft_deleted_country(self) -> None:
        """
        A country present in the upstream source is restored when it was
        previously soft-deleted.
        """

        self._write_dataset(
            self._india_dataset(),
        )

        self._run_import()

        country = Country.objects.get(
            code="IN",
        )

        country.soft_delete()

        deleted_country = Country.all_objects.get(
            code="IN",
        )

        self.assertTrue(
            deleted_country.is_deleted,
        )

        self.assertFalse(
            Country.objects.filter(
                code="IN",
            ).exists(),
        )

        self._run_import()

        restored_country = Country.all_objects.get(
            code="IN",
        )

        self.assertFalse(
            restored_country.is_deleted,
        )

        self.assertTrue(
            restored_country.is_active,
        )

        self.assertIsNone(
            restored_country.deleted_at,
        )

        self.assertEqual(
            restored_country.name,
            "India",
        )

        self.assertTrue(
            Country.objects.filter(
                code="IN",
            ).exists(),
        )

    def test_import_restores_soft_deleted_region(self) -> None:
        """
        A region present in the upstream source is restored when it was
        previously soft-deleted.
        """

        self._write_dataset(
            self._india_dataset(),
        )

        self._run_import()

        country = Country.objects.get(
            code="IN",
        )

        region = AdministrativeRegion.objects.get(
            country=country,
            code="BR",
        )

        region.soft_delete()

        deleted_region = AdministrativeRegion.all_objects.get(
            country=country,
            code="BR",
        )

        self.assertTrue(
            deleted_region.is_deleted,
        )

        self.assertFalse(
            AdministrativeRegion.objects.filter(
                country=country,
                code="BR",
            ).exists(),
        )

        self._run_import()

        restored_region = AdministrativeRegion.all_objects.get(
            country=country,
            code="BR",
        )

        self.assertFalse(
            restored_region.is_deleted,
        )

        self.assertTrue(
            restored_region.is_active,
        )

        self.assertIsNone(
            restored_region.deleted_at,
        )

        self.assertEqual(
            restored_region.name,
            "Bihar",
        )

        self.assertTrue(
            AdministrativeRegion.objects.filter(
                country=country,
                code="BR",
            ).exists(),
        )

    def test_import_restores_soft_deleted_city(self) -> None:
        """
        A city present in the upstream source is restored when it was
        previously soft-deleted.
        """

        self._write_dataset(
            self._india_dataset(),
        )

        self._run_import()

        city = City.objects.get(
            source="countries-states-cities",
            source_id="1001",
        )

        city.soft_delete()

        deleted_city = City.all_objects.get(
            source="countries-states-cities",
            source_id="1001",
        )

        self.assertTrue(
            deleted_city.is_deleted,
        )

        self.assertFalse(
            City.objects.filter(
                source="countries-states-cities",
                source_id="1001",
            ).exists(),
        )

        self._run_import()

        restored_city = City.all_objects.get(
            source="countries-states-cities",
            source_id="1001",
        )

        self.assertFalse(
            restored_city.is_deleted,
        )

        self.assertTrue(
            restored_city.is_active,
        )

        self.assertIsNone(
            restored_city.deleted_at,
        )

        self.assertEqual(
            restored_city.name,
            "Patna",
        )

        self.assertEqual(
            restored_city.timezone,
            "Asia/Kolkata",
        )

        self.assertEqual(
            str(restored_city.latitude),
            "25.594100",
        )

        self.assertEqual(
            str(restored_city.longitude),
            "85.137600",
        )

        self.assertTrue(
            City.objects.filter(
                source="countries-states-cities",
                source_id="1001",
            ).exists(),
        )

    def test_duplicate_region_names_are_allowed_when_codes_differ(
        self,
    ) -> None:
        """
        Region names do not need to be unique within a country.

        Region identity is country + code.
        """

        source = self._write_dataset(
            [
                {
                    "id": 1,
                    "name": "Azerbaijan",
                    "iso2": "AZ",
                    "iso3": "AZE",
                    "phone_code": "+994",
                    "states": [
                        {
                            "id": 101,
                            "name": "Lankaran",
                            "iso2": "LA",
                            "type": "region",
                            "cities": [],
                        },
                        {
                            "id": 102,
                            "name": "Lankaran",
                            "iso2": "LB",
                            "type": "region",
                            "cities": [],
                        },
                    ],
                },
            ],
        )

        self._run_import()

        country = Country.objects.get(
            code="AZ",
        )

        regions = AdministrativeRegion.objects.filter(
            country=country,
            name="Lankaran",
        )

        self.assertEqual(
            regions.count(),
            2,
        )

        self.assertSetEqual(
            set(
                regions.values_list(
                    "code",
                    flat=True,
                ),
            ),
            {
                "LA",
                "LB",
            },
        )

    def test_duplicate_region_code_fails(self) -> None:
        """
        Duplicate country + region code combinations are rejected.
        """

        source = self._write_dataset(
            [
                {
                    "id": 1,
                    "name": "Test Country",
                    "iso2": "TC",
                    "iso3": "TST",
                    "phone_code": "+999",
                    "states": [
                        {
                            "id": 101,
                            "name": "Region One",
                            "iso2": "RG",
                            "type": "state",
                            "cities": [],
                        },
                        {
                            "id": 102,
                            "name": "Region Two",
                            "iso2": "RG",
                            "type": "state",
                            "cities": [],
                        },
                    ],
                },
            ],
        )

        with self.assertRaises(
            CommandError,
        ) as context:
            self._run_import()

        self.assertIn(
            "Duplicate region code",
            str(
                context.exception,
            ),
        )

        self.assertEqual(
            Country.objects.count(),
            0,
        )

        self.assertEqual(
            AdministrativeRegion.objects.count(),
            0,
        )

        self.assertEqual(
            City.objects.count(),
            0,
        )

    def test_duplicate_city_source_id_fails(self) -> None:
        """
        A city source + source ID combination must be unique.
        """

        source = self._write_dataset(
            [
                {
                    "id": 1,
                    "name": "India",
                    "iso2": "IN",
                    "iso3": "IND",
                    "phone_code": "+91",
                    "states": [
                        {
                            "id": 101,
                            "name": "Bihar",
                            "iso2": "BR",
                            "type": "state",
                            "cities": [
                                {
                                    "id": 1001,
                                    "name": "Patna",
                                    "latitude": "25.59410000",
                                    "longitude": "85.13760000",
                                    "timezone": "Asia/Kolkata",
                                },
                                {
                                    "id": 1001,
                                    "name": "Another Patna",
                                    "latitude": "25.60000000",
                                    "longitude": "85.15000000",
                                    "timezone": "Asia/Kolkata",
                                },
                            ],
                        },
                    ],
                },
            ],
        )

        with self.assertRaises(
            CommandError,
        ) as context:
            self._run_import()

        self.assertIn(
            "Duplicate city source identity",
            str(
                context.exception,
            ),
        )

        self.assertEqual(
            Country.objects.count(),
            0,
        )

        self.assertEqual(
            AdministrativeRegion.objects.count(),
            0,
        )

        self.assertEqual(
            City.objects.count(),
            0,
        )

    def test_city_coordinates_are_imported(self) -> None:
        """
        City latitude and longitude are imported accurately.
        """

        self._write_dataset(
            self._india_dataset(
                latitude="11.70000000",
                longitude="92.71667000",
            ),
        )

        self._run_import()

        city = City.objects.get(
            source_id="1001",
        )

        self.assertEqual(
            str(city.latitude),
            "11.700000",
        )

        self.assertEqual(
            str(city.longitude),
            "92.716670",
        )

    def test_city_timezone_is_imported(self) -> None:
        """
        City timezone metadata is imported from the upstream dataset.
        """

        self._write_dataset(
            self._india_dataset(
                city_timezone="Asia/Kolkata",
            ),
        )

        self._run_import()

        city = City.objects.get(
            source_id="1001",
        )

        self.assertEqual(
            city.timezone,
            "Asia/Kolkata",
        )

    def test_invalid_city_latitude_fails(self) -> None:
        """
        City latitude must be within -90 and 90 degrees.
        """

        self._write_dataset(
            self._india_dataset(
                latitude="91.00000000",
            ),
        )

        with self.assertRaises(
            CommandError,
        ):
            self._run_import()

        self.assertEqual(
            Country.objects.count(),
            0,
        )

        self.assertEqual(
            AdministrativeRegion.objects.count(),
            0,
        )

        self.assertEqual(
            City.objects.count(),
            0,
        )

    def test_invalid_city_longitude_fails(self) -> None:
        """
        City longitude must be within -180 and 180 degrees.
        """

        self._write_dataset(
            self._india_dataset(
                longitude="181.00000000",
            ),
        )

        with self.assertRaises(
            CommandError,
        ):
            self._run_import()

        self.assertEqual(
            Country.objects.count(),
            0,
        )

        self.assertEqual(
            AdministrativeRegion.objects.count(),
            0,
        )

        self.assertEqual(
            City.objects.count(),
            0,
        )

    def test_missing_city_name_fails(self) -> None:
        """
        City records must contain a name.
        """

        self._write_dataset(
            self._india_dataset(
                city_name="",
            ),
        )

        with self.assertRaises(
            CommandError,
        ):
            self._run_import()

        self.assertEqual(
            Country.objects.count(),
            0,
        )

        self.assertEqual(
            AdministrativeRegion.objects.count(),
            0,
        )

        self.assertEqual(
            City.objects.count(),
            0,
        )

    def test_missing_city_id_fails(self) -> None:
        """
        City records must contain a stable upstream ID.
        """

        self._write_dataset(
            [
                {
                    "id": 1,
                    "name": "India",
                    "iso2": "IN",
                    "iso3": "IND",
                    "phone_code": "+91",
                    "states": [
                        {
                            "id": 101,
                            "name": "Bihar",
                            "iso2": "BR",
                            "type": "state",
                            "cities": [
                                {
                                    "name": "Patna",
                                    "latitude": "25.59410000",
                                    "longitude": "85.13760000",
                                    "timezone": "Asia/Kolkata",
                                },
                            ],
                        },
                    ],
                },
            ],
        )

        with self.assertRaises(
            CommandError,
        ):
            self._run_import()

        self.assertEqual(
            Country.objects.count(),
            0,
        )

        self.assertEqual(
            AdministrativeRegion.objects.count(),
            0,
        )

        self.assertEqual(
            City.objects.count(),
            0,
        )

    def test_dry_run_does_not_persist(self) -> None:
        """
        Dry-run validates data without writing to the database.
        """

        self._write_dataset(
            self._india_dataset(),
        )

        self._run_import(
            dry_run=True,
        )

        self.assertEqual(
            Country.objects.count(),
            0,
        )

        self.assertEqual(
            AdministrativeRegion.objects.count(),
            0,
        )

        self.assertEqual(
            City.objects.count(),
            0,
        )

    def test_invalid_country_code_fails(self) -> None:
        """
        ISO2 country codes must contain exactly two characters.
        """

        self._write_dataset(
            [
                {
                    "id": 1,
                    "name": "Invalid Country",
                    "iso2": "XXX",
                    "iso3": "INV",
                    "phone_code": "+999",
                    "states": [],
                },
            ],
        )

        with self.assertRaises(
            CommandError,
        ):
            self._run_import()

        self.assertEqual(
            Country.objects.count(),
            0,
        )

    def test_invalid_country_iso3_fails(self) -> None:
        """
        ISO3 country codes must contain exactly three characters.
        """

        self._write_dataset(
            [
                {
                    "id": 1,
                    "name": "Invalid Country",
                    "iso2": "IC",
                    "iso3": "INVALID",
                    "phone_code": "+999",
                    "states": [],
                },
            ],
        )

        with self.assertRaises(
            CommandError,
        ):
            self._run_import()

        self.assertEqual(
            Country.objects.count(),
            0,
        )

    def test_missing_country_name_fails(self) -> None:
        """
        Country records must contain a name.
        """

        self._write_dataset(
            [
                {
                    "id": 1,
                    "name": "",
                    "iso2": "IN",
                    "iso3": "IND",
                    "phone_code": "+91",
                    "states": [],
                },
            ],
        )

        with self.assertRaises(
            CommandError,
        ):
            self._run_import()

        self.assertEqual(
            Country.objects.count(),
            0,
        )

    def test_missing_region_name_fails(self) -> None:
        """
        Region records must contain a name.
        """

        self._write_dataset(
            [
                {
                    "id": 1,
                    "name": "India",
                    "iso2": "IN",
                    "iso3": "IND",
                    "phone_code": "+91",
                    "states": [
                        {
                            "id": 101,
                            "name": "",
                            "iso2": "BR",
                            "type": "state",
                            "cities": [],
                        },
                    ],
                },
            ],
        )

        with self.assertRaises(
            CommandError,
        ):
            self._run_import()

        self.assertEqual(
            Country.objects.count(),
            0,
        )

        self.assertEqual(
            AdministrativeRegion.objects.count(),
            0,
        )

    def test_missing_region_code_fails(self) -> None:
        """
        Region records must have a stable code or upstream ID.
        """

        self._write_dataset(
            [
                {
                    "id": 1,
                    "name": "India",
                    "iso2": "IN",
                    "iso3": "IND",
                    "phone_code": "+91",
                    "states": [
                        {
                            "name": "Bihar",
                            "type": "state",
                            "cities": [],
                        },
                    ],
                },
            ],
        )

        with self.assertRaises(
            CommandError,
        ):
            self._run_import()

        self.assertEqual(
            Country.objects.count(),
            0,
        )

        self.assertEqual(
            AdministrativeRegion.objects.count(),
            0,
        )

        self.assertEqual(
            City.objects.count(),
            0,
        )

    def test_unknown_region_country_reference_fails(self) -> None:
        """
        A region cannot reference a country absent from the dataset.

        This test exercises the validation layer directly because the
        importer derives region country codes from their parent country.
        """

        command = __import__(
            "apps.platform.geography.management.commands.import_geography",
            fromlist=[
                "Command",
            ],
        ).Command

        countries = [
            {
                "code": "IN",
                "name": "India",
                "iso3": "IND",
                "phone_code": "+91",
                "sort_order": 1,
            },
        ]

        regions = [
            {
                "country_code": "XX",
                "code": "RG",
                "name": "Unknown Region",
                "region_type": "state",
                "sort_order": 1,
            },
        ]

        cities: list[dict[str, Any]] = []

        with self.assertRaises(
            CommandError,
        ):
            command._validate_prepared_data(
                countries,
                regions,
                cities,
            )

        self.assertEqual(
            Country.objects.count(),
            0,
        )

        self.assertEqual(
            AdministrativeRegion.objects.count(),
            0,
        )

        self.assertEqual(
            City.objects.count(),
            0,
        )
