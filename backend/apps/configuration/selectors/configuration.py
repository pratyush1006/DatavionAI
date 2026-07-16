"""
Configuration selectors.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.common.exceptions import ResourceNotFoundException
from apps.configuration.models import (
    Configuration,
    FeatureFlag,
)


def get_configuration_by_key(
    *,
    key: str,
) -> Configuration:
    """
    Return a configuration by its key.
    """

    try:
        return Configuration.objects.active().get(
            key=key,
        )
    except Configuration.DoesNotExist as exc:
        raise ResourceNotFoundException(
            message=f"Configuration '{key}' not found.",
        ) from exc


def get_configurations() -> QuerySet[Configuration]:
    """
    Return all active configurations.
    """

    return Configuration.objects.active().order_by(
        "category",
        "name",
    )


def get_configurations_by_category(
    *,
    category: str,
) -> QuerySet[Configuration]:
    """
    Return configurations for a category.
    """

    return (
        Configuration.objects.active()
        .filter(
            category=category,
        )
        .order_by(
            "name",
        )
    )


def get_feature_flag(
    *,
    key: str,
) -> FeatureFlag:
    """
    Return a feature flag by its key.
    """

    try:
        return FeatureFlag.objects.active().get(
            key=key,
        )
    except FeatureFlag.DoesNotExist as exc:
        raise ResourceNotFoundException(
            message=f"Feature flag '{key}' not found.",
        ) from exc


def get_feature_flags() -> QuerySet[FeatureFlag]:
    """
    Return all active feature flags.
    """

    return FeatureFlag.objects.active().order_by(
        "name",
    )


def get_enabled_feature_flags() -> QuerySet[FeatureFlag]:
    """
    Return all enabled feature flags.
    """

    return (
        FeatureFlag.objects.active()
        .filter(
            is_enabled=True,
        )
        .order_by(
            "name",
        )
    )
