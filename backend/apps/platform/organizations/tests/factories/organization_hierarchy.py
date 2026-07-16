"""
OrganizationHierarchy test factories.
"""

from __future__ import annotations

from apps.platform.organizations.constants import (
    OrganizationHierarchyRelationshipType,
    OrganizationHierarchyStatus,
)
from apps.platform.organizations.models import (
    Organization,
    OrganizationHierarchy,
)

from .organization import (
    create_organization,
)


def create_organization_hierarchy(
    *,
    parent_organization: Organization | None = None,
    child_organization: Organization | None = None,
    **kwargs,
) -> OrganizationHierarchy:
    """
    Create an organization hierarchy for testing.
    """

    if parent_organization is None:
        parent_organization = create_organization()

    if child_organization is None:
        child_organization = create_organization()

    defaults = {
        "parent_organization": parent_organization,
        "child_organization": child_organization,
        "relationship_type": (OrganizationHierarchyRelationshipType.SUBSIDIARY),
        "status": (OrganizationHierarchyStatus.ACTIVE),
        "display_order": 1,
    }

    defaults.update(
        kwargs,
    )

    return OrganizationHierarchy.objects.create(
        **defaults,
    )


__all__ = [
    "create_organization_hierarchy",
]
