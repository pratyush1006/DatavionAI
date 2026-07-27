"""
Organization manager exports.

Central manager registry for the
DatavionOS Organizations bounded context.
"""

from .organization import (
    OrganizationManager,
)
from .organization_branding import (
    OrganizationBrandingManager,
)
from .organization_feature import (
    OrganizationFeatureManager,
)
from .organization_hierarchy import (
    OrganizationHierarchyManager,
)
from .organization_module import (
    OrganizationModuleManager,
)
from .organization_profile import (
    OrganizationProfileManager,
)

__all__: tuple[str, ...] = (
    "OrganizationManager",
    "OrganizationBrandingManager",
    "OrganizationFeatureManager",
    "OrganizationHierarchyManager",
    "OrganizationModuleManager",
    "OrganizationProfileManager",
)
