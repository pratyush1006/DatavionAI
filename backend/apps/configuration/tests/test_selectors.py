"""
Tests for configuration selectors.
"""

from __future__ import annotations

from django.test import TestCase

from apps.configuration.constants import (
    CONFIGURATION_CATEGORY_GENERAL,
    CONFIGURATION_CATEGORY_SECURITY,
    CONFIGURATION_TYPE_STRING,
    FEATURE_AI_ASSISTANT,
    FEATURE_STORAGE,
)
from apps.configuration.models import (
    Configuration,
    FeatureFlag,
)
from apps.configuration.selectors.configuration import (
    get_configuration_by_key,
    get_configurations,
    get_configurations_by_category,
    get_enabled_feature_flags,
    get_feature_flag,
    get_feature_flags,
)


class ConfigurationSelectorTestCase(TestCase):
    """
    Tests for configuration selectors.
    """

    def setUp(self):
        self.configuration = Configuration.objects.create(
            key="PLATFORM_NAME",
            category=CONFIGURATION_CATEGORY_GENERAL,
            name="Platform Name",
            value="Datavion AI",
            value_type=CONFIGURATION_TYPE_STRING,
        )

        self.security_configuration = Configuration.objects.create(
            key="SESSION_TIMEOUT",
            category=CONFIGURATION_CATEGORY_SECURITY,
            name="Session Timeout",
            value="30",
            value_type=CONFIGURATION_TYPE_STRING,
        )

        self.enabled_feature = FeatureFlag.objects.create(
            key=FEATURE_AI_ASSISTANT,
            name="AI Assistant",
            is_enabled=True,
        )

        self.disabled_feature = FeatureFlag.objects.create(
            key=FEATURE_STORAGE,
            name="Storage",
            is_enabled=False,
        )

    def test_get_configuration_by_key(self):
        """
        Should return the requested configuration.
        """

        configuration = get_configuration_by_key(
            key="PLATFORM_NAME",
        )

        self.assertEqual(
            configuration,
            self.configuration,
        )

    def test_get_configurations(self):
        """
        Should return all active configurations.
        """

        queryset = get_configurations()

        self.assertEqual(
            queryset.count(),
            2,
        )

        self.assertIn(
            self.configuration,
            queryset,
        )

    def test_get_configurations_by_category(self):
        """
        Should return configurations for a category.
        """

        queryset = get_configurations_by_category(
            category=CONFIGURATION_CATEGORY_GENERAL,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            self.configuration,
            queryset,
        )

    def test_get_feature_flag(self):
        """
        Should return a feature flag by key.
        """

        feature = get_feature_flag(
            key=FEATURE_AI_ASSISTANT,
        )

        self.assertEqual(
            feature,
            self.enabled_feature,
        )

    def test_get_feature_flags(self):
        """
        Should return all feature flags.
        """

        queryset = get_feature_flags()

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_get_enabled_feature_flags(self):
        """
        Should return only enabled feature flags.
        """

        queryset = get_enabled_feature_flags()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            self.enabled_feature,
            queryset,
        )

        self.assertNotIn(
            self.disabled_feature,
            queryset,
        )

    def test_inactive_configuration_not_returned(self):
        """
        Inactive configurations should not be returned.
        """

        self.configuration.is_active = False
        self.configuration.save()

        queryset = get_configurations()

        self.assertNotIn(
            self.configuration,
            queryset,
        )

    def test_inactive_feature_flag_not_returned(self):
        """
        Inactive feature flags should not be returned.
        """

        self.enabled_feature.is_active = False
        self.enabled_feature.save()

        queryset = get_feature_flags()

        self.assertNotIn(
            self.enabled_feature,
            queryset,
        )
