"""
Organization selector exports.

Central selector registry for
DatavionOS organization domain.
"""

from .organization import (
    get_active_organizations,
    get_organization_by_code,
    get_organization_by_id,
    get_organization_by_slug,
    get_organization_summary,
    get_organizations,
    get_verified_organizations,
    organization_exists,
    search_organizations,
)
from .organization_branding import (
    branding_exists,
    get_branding_by_domain,
    get_brandings,
    get_organization_branding,
    get_organization_branding_by_id,
    get_organization_branding_by_organization,
    get_organization_brandings,
)
from .organization_domain import (
    domain_exists,
    get_domain_by_id,
    get_domain_by_name,
    get_domains,
    get_primary_domain,
    get_verified_domains,
)
from .organization_feature import (
    feature_exists,
    get_enabled_features,
    get_feature_by_code,
    get_feature_by_id,
    get_features,
    get_organization_features,
)
from .organization_hierarchy import (
    get_child_hierarchies,
    get_organization_hierarchies,
    get_organization_hierarchy_by_id,
    get_parent_hierarchies,
    search_organization_hierarchies,
)
from .organization_module import (
    get_enabled_modules,
    get_module_by_code,
    get_module_by_id,
    get_modules,
    get_organization_modules,
    module_exists,
)
from .organization_settings import (
    get_email_enabled_settings,
    get_mfa_required_settings,
    get_organization_settings,
    get_settings,
)

__all__: tuple[str, ...] = (
    # Organization
    "get_active_organizations",
    "get_organization_by_code",
    "get_organization_by_id",
    "get_organization_by_slug",
    "get_organization_summary",
    "get_organizations",
    "get_verified_organizations",
    "organization_exists",
    "search_organizations",
    # Branding
    "branding_exists",
    "get_branding_by_domain",
    "get_brandings",
    "get_organization_branding",
    "get_organization_branding_by_id",
    "get_organization_branding_by_organization",
    "get_organization_brandings",
    # Domain
    "domain_exists",
    "get_domain_by_id",
    "get_domain_by_name",
    "get_domains",
    "get_primary_domain",
    "get_verified_domains",
    # Features
    "feature_exists",
    "get_enabled_features",
    "get_feature_by_code",
    "get_feature_by_id",
    "get_features",
    "get_organization_features",
    # Modules
    "get_enabled_modules",
    "get_module_by_code",
    "get_module_by_id",
    "get_modules",
    "get_organization_modules",
    "module_exists",
    # Settings
    "get_email_enabled_settings",
    "get_mfa_required_settings",
    "get_organization_settings",
    "get_settings",
    # Hierarchy
    "get_child_hierarchies",
    "get_organization_hierarchies",
    "get_organization_hierarchy_by_id",
    "get_parent_hierarchies",
    "search_organization_hierarchies",
)
