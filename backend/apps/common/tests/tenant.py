"""
Tenant testing utilities.

Provides reusable tenant and organization
context setup for DatavionOS tests.
"""

from __future__ import annotations

from apps.platform.organizations.tests.factories.organization import (
    create_organization,
)


def create_test_tenant_context():
    """
    Create organization context.

    Returns:

        organization
    """

    return create_organization()


__all__ = [
    "create_test_tenant_context",
]
