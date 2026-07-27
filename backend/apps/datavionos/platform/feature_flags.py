"""
Platform feature flag contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class FeatureScope(
    StrEnum,
):
    """
    Feature evaluation scope.
    """

    GLOBAL = "global"
    ENVIRONMENT = "environment"
    TENANT = "tenant"
    ORGANIZATION = "organization"
    SUBSCRIPTION = "subscription"
    USER = "user"


@dataclass(
    frozen=True,
    slots=True,
)
class FeatureContext:
    """
    Context used during feature
    evaluation.
    """

    tenant_id: str | None = None

    organization_id: str | None = None

    subscription: str | None = None

    user_id: str | None = None

    environment: str | None = None

    metadata: dict[str, Any] | None = None


@runtime_checkable
class FeatureFlagService(
    Protocol,
):
    """
    Platform feature flag abstraction.
    """

    def is_enabled(
        self,
        feature: str,
        *,
        context: FeatureContext | None = None,
    ) -> bool:
        """
        Determine whether a feature
        is enabled.
        """

    def get_value(
        self,
        feature: str,
        default: Any = None,
        *,
        context: FeatureContext | None = None,
    ) -> Any:
        """
        Return a feature value.

        Supports non-boolean flags
        such as rollout percentages,
        limits, or configuration.
        """

    def exists(
        self,
        feature: str,
    ) -> bool:
        """
        Determine whether a feature
        is defined.
        """

    def invalidate_cache(
        self,
    ) -> None:
        """
        Clear any cached feature
        evaluations.
        """


__all__ = [
    "FeatureScope",
    "FeatureContext",
    "FeatureFlagService",
]
