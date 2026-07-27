"""
Organization service exports.

Public service registry for the Organizations domain.
"""

from .organization import (
    activate_organization,
    archive_organization,
    create_organization,
    deactivate_organization,
    delete_organization,
    update_organization,
    verify_organization,
)
from .organization_branding import (
    create_branding,
    create_organization_branding,
    delete_branding,
    delete_organization_branding,
    update_branding,
    update_organization_branding,
)
from .organization_domain import (
    create_domain,
    set_primary_domain,
    update_domain,
    verify_domain,
)
from .organization_feature import (
    create_feature,
    disable_feature,
    enable_feature,
    update_feature,
)
from .organization_hierarchy import (
    create_organization_hierarchy,
    delete_organization_hierarchy,
    update_organization_hierarchy,
)
from .organization_module import (
    create_module,
    disable_module,
    enable_module,
    update_module,
)
from .organization_settings import (
    create_settings,
    disable_mfa,
    enable_mfa,
    update_settings,
)

__all__: tuple[str, ...] = (
    # Organization
    "activate_organization",
    "archive_organization",
    "create_organization",
    "deactivate_organization",
    "delete_organization",
    "update_organization",
    "verify_organization",
    # Branding
    "create_branding",
    "create_organization_branding",
    "delete_branding",
    "delete_organization_branding",
    "update_branding",
    "update_organization_branding",
    # Domain
    "create_domain",
    "set_primary_domain",
    "update_domain",
    "verify_domain",
    # Feature
    "create_feature",
    "disable_feature",
    "enable_feature",
    "update_feature",
    # Hierarchy
    "create_organization_hierarchy",
    "delete_organization_hierarchy",
    "update_organization_hierarchy",
    # Module
    "create_module",
    "disable_module",
    "enable_module",
    "update_module",
    # Settings
    "create_settings",
    "disable_mfa",
    "enable_mfa",
    "update_settings",
)
