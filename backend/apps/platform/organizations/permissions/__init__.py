"""
Organization permission exports.

Central permission registry for the
DatavionOS Organizations domain.
"""

from __future__ import annotations

from .domain import (
    CanCreateOrganizationDomain,
    CanDeleteOrganizationDomain,
    CanUpdateOrganizationDomain,
    CanViewOrganizationDomain,
)
from .feature import (
    CanCreateOrganizationFeature,
    CanDeleteOrganizationFeature,
    CanUpdateOrganizationFeature,
    CanViewOrganizationFeature,
)
from .module import (
    CanCreateOrganizationModule,
    CanDeleteOrganizationModule,
    CanUpdateOrganizationModule,
    CanViewOrganizationModule,
)
from .organization import (
    CanCreateOrganization,
    CanDeleteOrganization,
    CanUpdateOrganization,
    CanViewOrganization,
)
from .organization_branding import (
    CanCreateOrganizationBranding,
    CanDeleteOrganizationBranding,
    CanUpdateOrganizationBranding,
    CanViewOrganizationBranding,
)
from .organization_hierarchy import (
    CanCreateOrganizationHierarchy,
    CanDeleteOrganizationHierarchy,
    CanUpdateOrganizationHierarchy,
    CanViewOrganizationHierarchy,
)
from .settings import (
    CanCreateOrganizationSettings,
    CanDeleteOrganizationSettings,
    CanUpdateOrganizationSettings,
    CanViewOrganizationSettings,
)

__all__: tuple[str, ...] = (
    # Organization
    "CanCreateOrganization",
    "CanDeleteOrganization",
    "CanUpdateOrganization",
    "CanViewOrganization",
    # Branding
    "CanCreateOrganizationBranding",
    "CanDeleteOrganizationBranding",
    "CanUpdateOrganizationBranding",
    "CanViewOrganizationBranding",
    # Hierarchy
    "CanCreateOrganizationHierarchy",
    "CanDeleteOrganizationHierarchy",
    "CanUpdateOrganizationHierarchy",
    "CanViewOrganizationHierarchy",
    # Domain
    "CanCreateOrganizationDomain",
    "CanDeleteOrganizationDomain",
    "CanUpdateOrganizationDomain",
    "CanViewOrganizationDomain",
    # Feature
    "CanCreateOrganizationFeature",
    "CanDeleteOrganizationFeature",
    "CanUpdateOrganizationFeature",
    "CanViewOrganizationFeature",
    # Module
    "CanCreateOrganizationModule",
    "CanDeleteOrganizationModule",
    "CanUpdateOrganizationModule",
    "CanViewOrganizationModule",
    # Settings
    "CanCreateOrganizationSettings",
    "CanDeleteOrganizationSettings",
    "CanUpdateOrganizationSettings",
    "CanViewOrganizationSettings",
)
