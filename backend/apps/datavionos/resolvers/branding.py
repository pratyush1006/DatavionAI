"""
Platform branding resolver.
"""

from __future__ import annotations

from typing import Any

from apps.platform.organizations.models import Organization


class BrandingResolver:
    """
    Resolve branding configuration for an organization.
    """

    def resolve(
        self,
        *,
        organization: Organization | None,
    ) -> dict[str, Any]:
        """
        Return branding information.
        """

        if organization is None:
            return self._default()

        return {
            "application_name": "Datavion AI",
            "organization_name": organization.name,
            "logo": None,
            "favicon": None,
            "primary_color": "#2563EB",
            "secondary_color": "#0F172A",
            "theme": "light",
        }

    def _default(
        self,
    ) -> dict[str, Any]:
        """
        Return default branding.
        """

        return {
            "application_name": "Datavion AI",
            "organization_name": "",
            "logo": None,
            "favicon": None,
            "primary_color": "#2563EB",
            "secondary_color": "#0F172A",
            "theme": "light",
        }


branding_resolver = BrandingResolver()


__all__ = [
    "BrandingResolver",
    "branding_resolver",
]
