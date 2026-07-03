"""
Tests for configuration models.
"""

from __future__ import annotations

from django.test import TestCase

from apps.configuration.constants import (
    CONFIGURATION_CATEGORY_GENERAL,
    CONFIGURATION_TYPE_STRING,
    DEFAULT_PLATFORM_NAME,
    FEATURE_AI_ASSISTANT,
)
from apps.configuration.models import (
    Configuration,
    FeatureFlag,
)


class ConfigurationModelTestCase(TestCase):
    """
    Tests for the Configuration model.
    """

    def test_configuration_string_representation(self):
        """
        __str__ should return the configuration name and key.
        """

        configuration = Configuration.objects.create(
            key="PLATFORM_NAME",
            category=CONFIGURATION_CATEGORY_GENERAL,
            name="Platform Name",
            description="Platform display name.",
            value=DEFAULT_PLATFORM_NAME,
            value_type=CONFIGURATION_TYPE_STRING,
        )

        self.assertEqual(
            str(configuration),
            "Platform Name (PLATFORM_NAME)",
        )

    def test_configuration_defaults(self):
        """
        Configuration should use the expected default values.
        """

        configuration = Configuration.objects.create(
            key="PLATFORM_NAME",
            name="Platform Name",
            value=DEFAULT_PLATFORM_NAME,
        )

        self.assertEqual(
            configuration.category,
            CONFIGURATION_CATEGORY_GENERAL,
        )

        self.assertEqual(
            configuration.value_type,
            CONFIGURATION_TYPE_STRING,
        )

        self.assertTrue(
            configuration.is_editable,
        )

        self.assertTrue(
            configuration.is_active,
        )


class FeatureFlagModelTestCase(TestCase):
    """
    Tests for the FeatureFlag model.
    """

    def test_feature_flag_string_representation(self):
        """
        __str__ should indicate the feature status.
        """

        feature = FeatureFlag.objects.create(
            key=FEATURE_AI_ASSISTANT,
            name="AI Assistant",
            is_enabled=True,
        )

        self.assertEqual(
            str(feature),
            "AI Assistant (Enabled)",
        )

    def test_feature_flag_defaults(self):
        """
        FeatureFlag should use the expected default values.
        """

        feature = FeatureFlag.objects.create(
            key=FEATURE_AI_ASSISTANT,
            name="AI Assistant",
        )

        self.assertFalse(
            feature.is_enabled,
        )

        self.assertTrue(
            feature.is_active,
        )
