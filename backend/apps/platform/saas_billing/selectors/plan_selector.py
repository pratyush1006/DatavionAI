"""
SaaS Billing Plan selectors.

Read/query layer for subscription plans.

Responsibilities:

- Retrieve public plans
- Retrieve active plans
- Retrieve plan details
- Apply organization/segment filters
- Keep query logic outside APIs and services

Architecture:

API
 |
Selector
 |
Manager
 |
ORM
 |
Database
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import QuerySet

from apps.platform.saas_billing.models import (
    Plan,
)

if TYPE_CHECKING:
    from uuid import UUID


# =============================================================================
# Public Plan Queries
# =============================================================================


def get_public_plans() -> QuerySet[Plan]:
    """
    Return publicly visible active plans.

    Used by:

    - Pricing page
    - Signup flow
    - Organization onboarding
    """

    return Plan.objects.filter(
        is_active=True,
        is_public=True,
    ).order_by(
        "display_order",
        "price",
        "name",
    )


def get_featured_plans() -> QuerySet[Plan]:
    """
    Return featured public plans.
    """

    return get_public_plans().filter(
        is_featured=True,
    )


# =============================================================================
# Plan Detail Queries
# =============================================================================


def get_plan_by_id(
    plan_id: UUID,
) -> Plan | None:
    """
    Retrieve a plan by UUID.

    Returns None if not found.
    """

    return Plan.objects.filter(
        id=plan_id,
        is_active=True,
    ).first()


def get_plan_by_code(
    code: str,
) -> Plan | None:
    """
    Retrieve plan using unique code.
    """

    return Plan.objects.filter(
        code=code,
        is_active=True,
    ).first()


# =============================================================================
# Healthcare Segment Queries
# =============================================================================


def get_plans_for_segment(
    segment: str,
) -> QuerySet[Plan]:
    """
    Return plans available for healthcare segment.

    Examples:

    - CLINIC
    - HOSPITAL
    - LABORATORY
    """

    return get_public_plans().filter(
        healthcare_segment=segment,
    )


# =============================================================================
# Default Plan Resolution
# =============================================================================


def get_default_plan() -> Plan | None:
    """
    Return default signup plan.

    Used during:

    - Organization registration
    - Trial onboarding
    """

    return Plan.objects.filter(
        is_active=True,
        is_default=True,
    ).first()


# =============================================================================
# Admin Queries
# =============================================================================


def get_all_plans() -> QuerySet[Plan]:
    """
    Return all plans.

    Intended for:

    - Admin dashboard
    - Internal management
    """

    return Plan.objects.all().order_by(
        "display_order",
        "price",
        "name",
    )


__all__ = [
    "get_public_plans",
    "get_featured_plans",
    "get_plan_by_id",
    "get_plan_by_code",
    "get_plans_for_segment",
    "get_default_plan",
    "get_all_plans",
]
