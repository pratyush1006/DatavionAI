"""
DatavionOS Canonical Effective Capability Intersection
VERSION: 1.0.0

This module is the canonical final capability gate.

Authority inputs:

    1. Subscription / entitlement capability
    2. RBAC capability
    3. Organization module override

The intersection is intentionally fail-closed.

A capability is effective only when it survives every authority boundary
that explicitly participates in the runtime context.

This module contains no database writes.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

AUTHORITY_KEYS = (
    "subscription_capabilities",
    "entitlement_capabilities",
    "rbac_capabilities",
    "organization_capabilities",
    "module_capabilities",
    "enabled_modules",
    "effective_capabilities",
)


def _normalise_capabilities(value: Any) -> set[str] | None:
    if value is None:
        return None

    if isinstance(value, Mapping):
        if "capabilities" in value:
            return _normalise_capabilities(value["capabilities"])

        if "permissions" in value:
            return _normalise_capabilities(value["permissions"])

        if "modules" in value:
            return _normalise_capabilities(value["modules"])

        return {str(key) for key, enabled in value.items() if bool(enabled)}

    if isinstance(value, str):
        return {value}

    if isinstance(value, Iterable):
        return {str(item) for item in value if item is not None}

    return None


def _first_present(
    context: Mapping[str, Any],
    keys: tuple[str, ...],
) -> set[str] | None:
    for key in keys:
        if key not in context:
            continue

        capabilities = _normalise_capabilities(context[key])

        if capabilities is not None:
            return capabilities

    return None


def resolve_canonical_intersection(
    context: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Resolve the final DatavionOS capability set.

    The resolver does not invent authority.

    Missing optional authority collections are preserved as missing rather
    than silently treated as unrestricted.

    When multiple explicit authority collections exist, the result is their
    set intersection.

    Organization/module disablement is fail-closed.
    """

    result = dict(context)

    subscription = _first_present(
        context,
        (
            "subscription_capabilities",
            "entitlement_capabilities",
        ),
    )

    rbac = _first_present(
        context,
        (
            "rbac_capabilities",
            "permissions",
            "permission_codes",
        ),
    )

    organization = _first_present(
        context,
        (
            "organization_capabilities",
            "module_capabilities",
            "enabled_modules",
        ),
    )

    effective = _first_present(
        context,
        ("effective_capabilities",),
    )

    authority_sets = [
        capabilities
        for capabilities in (
            subscription,
            rbac,
            organization,
            effective,
        )
        if capabilities is not None
    ]

    if not authority_sets:
        result["effective_capabilities"] = set()
        result["canonical_authority_intersection"] = {
            "subscription": False,
            "rbac": False,
            "organization": False,
            "effective": False,
            "fail_closed": True,
        }
        return result

    intersection = set(authority_sets[0])

    for capability_set in authority_sets[1:]:
        intersection.intersection_update(capability_set)

    result["effective_capabilities"] = intersection

    result["canonical_authority_intersection"] = {
        "subscription": subscription is not None,
        "rbac": rbac is not None,
        "organization": organization is not None,
        "effective": effective is not None,
        "fail_closed": False,
    }

    return result


def apply_canonical_intersection(
    value: Any,
) -> Any:
    """
    Apply the canonical intersection to a builder result.

    Mapping results are enriched with the canonical effective capability
    collection.

    Non-mapping results are returned unchanged because changing their type
    would violate the existing service contract.
    """

    if not isinstance(value, Mapping):
        return value

    return resolve_canonical_intersection(value)
