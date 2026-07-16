"""
Organization admin registrations.
"""

from .organization import OrganizationAdmin
from .organization_hierarchy import (
    OrganizationHierarchyAdmin,
)

__all__ = [
    "OrganizationAdmin",
    "OrganizationHierarchyAdmin",
]
