"""
OrganizationBranding test factories.
"""

from __future__ import annotations

from apps.platform.organizations.constants import (
    OrganizationBrandingThemeMode,
)
from apps.platform.organizations.models import (
    Organization,
    OrganizationBranding,
)

from .organization import (
    create_organization,
)


def create_organization_branding(
    *,
    organization: Organization | None = None,
    **kwargs,
) -> OrganizationBranding:
    """
    Create an organization branding record for testing.
    """

    if organization is None:
        organization = create_organization()

    defaults = {
        "organization": organization,
        "primary_color": "#1A73E8",
        "theme_mode": OrganizationBrandingThemeMode.LIGHT,
    }

    defaults.update(
        kwargs,
    )

    return OrganizationBranding.objects.create(
        **defaults,
    )


__all__ = [
    "create_organization_branding",
]
