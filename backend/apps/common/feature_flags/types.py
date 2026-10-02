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
)

###############################################################################
# Feature Identity
###############################################################################

type FeatureKey = str

type FeatureName = str


###############################################################################
# Feature Value
###############################################################################

type FeatureValue = bool | str | int | float | None


###############################################################################
# Evaluation Context
###############################################################################

type FeatureContext = Mapping[
    str,
    Any,
]


###############################################################################
# Tenant / Organization Identifiers
###############################################################################

type TenantID = str | int

type OrganizationID = str | int


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
