"""
Tests for configuration services.
"""

from __future__ import annotations

from django.test import TestCase

from apps.configuration.constants import (
    CONFIGURATION_CATEGORY_GENERAL,
    CONFIGURATION_TYPE_BOOLEAN,
    CONFIGURATION_TYPE_FLOAT,
    CONFIGURATION_TYPE_INTEGER,
    CONFIGURATION_TYPE_JSON,
    CONFIGURATION_TYPE_STRING,
    FEATURE_AI_ASSISTANT,
)
from apps.configuration.models import (
    Configuration,
    FeatureFlag,
)
from apps.configuration.services.configuration import (
    create_configuration,
    delete_configuration,
    get_configuration,
    is_feature_enabled,
    set_configuration,
    update_configuration,
)


class ConfigurationServiceTestCase(TestCase):
    """
    Tests for configuration services.
    """

    def test_create_configuration(self):
        """
        Configuration should be created successfully.
        """

        configuration = create_configuration(
            key="PLATFORM_NAME",
            category=CONFIGURATION_CATEGORY_GENERAL,
            name="Platform Name",
            description="Platform name.",
            value="Datavion AI",
            value_type=CONFIGURATION_TYPE_STRING,
            is_editable=True,
        )

        self.assertIsInstance(
            configuration,
            Configuration,
        )

        self.assertEqual(
            configuration.key,
            "PLATFORM_NAME",
        )

    def test_update_configuration(self):
        """
        Configuration should be updated.
        """

        configuration = Configuration.objects.create(
            key="PLATFORM_NAME",
            category=CONFIGURATION_CATEGORY_GENERAL,
            name="Platform Name",
            value="Datavion AI",
            value_type=CONFIGURATION_TYPE_STRING,
        )

        update_configuration(
            configuration=configuration,
            value="Datavion Platform",
            name="Platform",
        )

        configuration.refresh_from_db()

        self.assertEqual(
            configuration.value,
            "Datavion Platform",
        )

        self.assertEqual(
            configuration.name,
            "Platform",
        )

    def test_delete_configuration(self):
        """
        Configuration should be soft deleted.
        """

        configuration = Configuration.objects.create(
            key="PLATFORM_NAME",
            category=CONFIGURATION_CATEGORY_GENERAL,
            name="Platform Name",
            value="Datavion AI",
            value_type=CONFIGURATION_TYPE_STRING,
        )

        delete_configuration(
            configuration=configuration,
        )

        configuration.refresh_from_db()

        self.assertFalse(
            configuration.is_active,
        )

    def test_get_string_configuration(self):
        """
        String configuration should be returned as string.
        """

        Configuration.objects.create(
            key="PLATFORM_NAME",
            category=CONFIGURATION_CATEGORY_GENERAL,
            name="Platform Name",
            value="Datavion AI",
            value_type=CONFIGURATION_TYPE_STRING,
        )

        value = get_configuration(
            key="PLATFORM_NAME",
        )

        self.assertEqual(
            value,
            "Datavion AI",
        )

    def test_get_integer_configuration(self):
        """
        Integer configuration should be converted.
        """

        Configuration.objects.create(
            key="SESSION_TIMEOUT",
            category=CONFIGURATION_CATEGORY_GENERAL,
            name="Session Timeout",
            value="30",
            value_type=CONFIGURATION_TYPE_INTEGER,
        )

        value = get_configuration(
            key="SESSION_TIMEOUT",
        )

        self.assertEqual(
            value,
            30,
        )

    def test_get_boolean_configuration(self):
        """
        Boolean configuration should be converted.
        """

        Configuration.objects.create(
            key="ENABLE_AI",
            category=CONFIGURATION_CATEGORY_GENERAL,
            name="Enable AI",
            value="true",
            value_type=CONFIGURATION_TYPE_BOOLEAN,
        )

        value = get_configuration(
            key="ENABLE_AI",
        )

        self.assertTrue(
            value,
        )

    def test_get_float_configuration(self):
        """
        Float configuration should be converted.
        """

        Configuration.objects.create(
            key="VAT_RATE",
            category=CONFIGURATION_CATEGORY_GENERAL,
            name="VAT Rate",
            value="18.5",
            value_type=CONFIGURATION_TYPE_FLOAT,
        )

        value = get_configuration(
            key="VAT_RATE",
        )

        self.assertEqual(
            value,
            18.5,
        )

    def test_get_json_configuration(self):
        """
        JSON configuration should be converted.
        """

        Configuration.objects.create(
            key="SUPPORTED_LANGUAGES",
            category=CONFIGURATION_CATEGORY_GENERAL,
            name="Languages",
            value='["en", "fr"]',
            value_type=CONFIGURATION_TYPE_JSON,
        )

        value = get_configuration(
            key="SUPPORTED_LANGUAGES",
        )

        self.assertEqual(
            value,
            [
                "en",
                "fr",
            ],
        )

    def test_get_default_configuration(self):
        """
        Default value should be returned when configuration does not exist.
        """

        value = get_configuration(
            key="UNKNOWN_KEY",
            default="default",
        )

        self.assertEqual(
            value,
            "default",
        )

    def test_set_configuration(self):
        """
        Configuration should be created or updated.
        """

        set_configuration(
            key="PLATFORM_NAME",
            value="Datavion AI",
        )

        value = get_configuration(
            key="PLATFORM_NAME",
        )

        self.assertEqual(
            value,
            "Datavion AI",
        )

    def test_feature_flag_enabled(self):
        """
        Enabled feature flag should return True.
        """

        FeatureFlag.objects.create(
            key=FEATURE_AI_ASSISTANT,
            name="AI Assistant",
            is_enabled=True,
        )

        self.assertTrue(
            is_feature_enabled(
                key=FEATURE_AI_ASSISTANT,
            )
        )

    def test_feature_flag_disabled(self):
        """
        Disabled feature flag should return False.
        """

        FeatureFlag.objects.create(
            key=FEATURE_AI_ASSISTANT,
            name="AI Assistant",
            is_enabled=False,
        )

        self.assertFalse(
            is_feature_enabled(
                key=FEATURE_AI_ASSISTANT,
            )
        )
