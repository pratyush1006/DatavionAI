"""
Feature flag type definitions for DatavionOS.

Provides reusable type aliases shared across the feature flag
framework.
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
)
from typing import (
    Any,
    TypeAlias,
)

###############################################################################
# Feature Identity
###############################################################################

FeatureKey: TypeAlias = str

FeatureName: TypeAlias = str


###############################################################################
# Feature Value
###############################################################################

FeatureValue: TypeAlias = bool | str | int | float | None


###############################################################################
# Evaluation Context
###############################################################################

FeatureContext: TypeAlias = Mapping[
    str,
    Any,
]


###############################################################################
# Tenant / Organization Identifiers
###############################################################################

TenantID: TypeAlias = str | int

OrganizationID: TypeAlias = str | int


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "FeatureContext",
    "FeatureKey",
    "FeatureName",
    "FeatureValue",
    "OrganizationID",
    "TenantID",
)
