"""
Feature flag registry for DatavionOS.

Maintains registered feature definitions and provides lookup
capabilities for the feature flag evaluation framework.

The registry is infrastructure-level only.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.common.feature_flags.exceptions import (
    FeatureFlagAlreadyRegisteredError,
    FeatureFlagNotFoundError,
)
from apps.common.feature_flags.models import (
    FeatureFlag,
)
from apps.common.feature_flags.types import (
    FeatureKey,
)


class FeatureFlagRegistry:
    """
    Central feature flag registry.

    Supports:

    - Feature registration
    - Feature lookup
    - Feature discovery
    - Duplicate protection
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize registry.
        """

        self._features: dict[
            FeatureKey,
            FeatureFlag,
        ] = {}

    def register(
        self,
        feature: FeatureFlag,
    ) -> None:
        """
        Register a feature flag.

        Raises:
            FeatureFlagAlreadyRegisteredError:
                If feature already exists.
        """

        if feature.key in self._features:
            raise FeatureFlagAlreadyRegisteredError(
                (f"Feature flag '{feature.key}' is already registered."),
            )

        self._features[feature.key] = feature

    def unregister(
        self,
        key: FeatureKey,
    ) -> None:
        """
        Remove a feature flag registration.
        """

        self._features.pop(
            key,
            None,
        )

    def get(
        self,
        key: FeatureKey,
    ) -> FeatureFlag:
        """
        Return a registered feature.

        Raises:
            FeatureFlagNotFoundError:
                If feature does not exist.
        """

        feature = self._features.get(
            key,
        )

        if feature is None:
            raise FeatureFlagNotFoundError(
                (f"Feature flag '{key}' does not exist."),
            )

        return feature

    def has(
        self,
        key: FeatureKey,
    ) -> bool:
        """
        Check whether a feature exists.
        """

        return key in self._features

    def all(
        self,
    ) -> Iterable[FeatureFlag]:
        """
        Return all registered features.
        """

        return self._features.values()

    def clear(
        self,
    ) -> None:
        """
        Remove all registered features.
        """

        self._features.clear()


feature_flag_registry = FeatureFlagRegistry()


__all__: tuple[str, ...] = (
    "FeatureFlagRegistry",
    "feature_flag_registry",
)
