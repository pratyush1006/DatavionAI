"""
Organization bootstrap builder.

Builds the response returned after successfully bootstrapping
a new organization.

Builders are responsible only for assembling response objects.
They must never contain business logic or database access.
"""

from __future__ import annotations

from dataclasses import (
    asdict,
    dataclass,
)

from apps.datavionos.services import (
    OrganizationBootstrapResult,
)


@dataclass(slots=True, frozen=True)
class OrganizationBootstrapPayload:
    """
    Response payload returned after organization bootstrap.
    """

    organization: object
    branding: object | None
    feature_flags: object | None
    navigation: object | None
    dashboard: object | None
    modules: list[object]


class OrganizationBootstrapBuilder:
    """
    Build the bootstrap response payload.

    Converts the OrganizationBootstrapResult returned by the
    service layer into a response object suitable for serializers
    and API views.
    """

    def build(
        self,
        result: OrganizationBootstrapResult,
    ) -> OrganizationBootstrapPayload:
        """
        Build the bootstrap payload.
        """

        return OrganizationBootstrapPayload(
            organization=result.organization,
            branding=result.branding,
            feature_flags=result.feature_flags,
            navigation=result.navigation,
            dashboard=result.dashboard,
            modules=result.modules or [],
        )

    def build_dict(
        self,
        result: OrganizationBootstrapResult,
    ) -> dict[str, object]:
        """
        Return the bootstrap payload as a dictionary.
        """

        return asdict(
            self.build(
                result,
            ),
        )


__all__ = [
    "OrganizationBootstrapBuilder",
    "OrganizationBootstrapPayload",
]
