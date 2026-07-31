"""
Organization bootstrap builder.

Builds DatavionOS organization runtime payload.

Responsibilities:

- Assemble bootstrap response objects
- Convert service result into API payload

Builders must:

- NOT contain business logic
- NOT access database
- NOT resolve entitlements

Architecture:

OrganizationBootstrapService
        |
        ↓
OrganizationBootstrapResult
        |
        ↓
OrganizationBootstrapBuilder
        |
        ↓
DatavionOS Runtime Payload
"""

from __future__ import annotations

from dataclasses import (
    asdict,
    dataclass,
)

from apps.datavionos.services import (
    OrganizationBootstrapResult,
)


@dataclass(
    slots=True,
    frozen=True,
)
class OrganizationBootstrapPayload:
    """
    Runtime payload returned after organization bootstrap.
    """

    organization: object

    branding: object | None

    feature_flags: dict | None

    navigation: object | None

    dashboard: object | None

    modules: list[object]

    capabilities: dict | None


class OrganizationBootstrapBuilder:
    """
    Convert bootstrap service result into
    DatavionOS runtime payload.
    """

    def build(
        self,
        result: OrganizationBootstrapResult,
    ) -> OrganizationBootstrapPayload:
        """
        Build bootstrap payload.
        """

        return OrganizationBootstrapPayload(
            organization=(result.organization),
            branding=(result.branding),
            feature_flags=(result.feature_flags),
            navigation=(result.navigation),
            dashboard=(result.dashboard),
            modules=(result.modules or []),
            capabilities=(
                getattr(
                    result,
                    "capabilities",
                    {},
                )
            ),
        )

    def build_dict(
        self,
        result: OrganizationBootstrapResult,
    ) -> dict[str, object]:
        """
        Return payload as dictionary.
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
