"""
DatavionOS module contract definitions.

The ModuleContract is the canonical metadata definition
for every DatavionOS platform module.

Examples:

- Patient Management
- Appointment Management
- Laboratory
- Pharmacy
- Billing
- AI Assistant
- Workflow Engine

The contract contains metadata only.

Runtime behavior belongs to services/selectors.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
    replace,
)
from typing import (
    Any,
)

from apps.datavionos.constants import (
    ModuleCategory,
    ModuleStatus,
)
from apps.datavionos.contracts.base import (
    BaseContract,
)

# ============================================================================
# UI CONTRACTS
# ============================================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class NavigationConfig:
    """
    Runtime navigation metadata.

    Controls sidebar/menu generation.
    """

    title: str

    route: str

    icon: str = ""

    category: str = "general"

    order: int = 0


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DashboardConfig:
    """
    Runtime dashboard metadata.

    Controls dashboard card generation.
    """

    enabled: bool = False

    title: str = ""

    description: str = ""

    icon: str = ""

    route: str = ""

    order: int = 0


# ============================================================================
# MODULE CONTRACT
# ============================================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ModuleContract(
    BaseContract,
):
    """
    Immutable DatavionOS module definition.

    Responsibilities:

    - Module identity
    - Runtime metadata
    - Permissions
    - Feature requirements
    - Dependencies
    - SaaS metadata
    - Navigation metadata
    - Dashboard metadata

    Runtime logic belongs outside this contract.
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    identifier: str

    name: str

    display_name: str

    category: ModuleCategory

    version: str = "1.0.0"

    description: str = ""

    icon: str = ""

    route: str = ""

    api_prefix: str = ""

    # ------------------------------------------------------------------
    # Runtime availability
    # ------------------------------------------------------------------

    enabled: bool = True

    system: bool = False

    tenant_scoped: bool = True

    order: int = 0

    # ------------------------------------------------------------------
    # UI Metadata
    # ------------------------------------------------------------------

    navigation: NavigationConfig | None = None

    dashboard: DashboardConfig | None = None

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    tags: tuple[str, ...] = ()

    # ------------------------------------------------------------------
    # RBAC
    # ------------------------------------------------------------------

    permissions: tuple[str, ...] = ()

    # ------------------------------------------------------------------
    # Dependency graph
    # ------------------------------------------------------------------

    dependencies: tuple[str, ...] = ()

    optional_dependencies: tuple[str, ...] = ()

    # ------------------------------------------------------------------
    # Feature entitlement
    # ------------------------------------------------------------------

    feature_flags: tuple[str, ...] = ()

    # ------------------------------------------------------------------
    # Extension metadata
    # ------------------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    status: ModuleStatus = ModuleStatus.ACTIVE

    # ------------------------------------------------------------------
    # Ownership
    # ------------------------------------------------------------------

    owner: str = ""

    homepage: str = ""

    documentation: str = ""

    support_email: str = ""

    license: str = ""

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(
        self,
    ) -> None:
        """
        Validate module definition.
        """

        super().validate()

        if not self.identifier.strip():
            raise ValueError(
                "identifier cannot be empty.",
            )

        if not self.display_name.strip():
            raise ValueError(
                "display_name cannot be empty.",
            )

        if not self.version.strip():
            raise ValueError(
                "version cannot be empty.",
            )

        if self.order < 0:
            raise ValueError(
                "order cannot be negative.",
            )

        if self.identifier in self.dependencies:
            raise ValueError(
                "A module cannot depend on itself.",
            )

        if len(
            set(self.dependencies),
        ) != len(
            self.dependencies,
        ):
            raise ValueError(
                "Duplicate module dependencies are not allowed.",
            )

        if self.navigation and not self.navigation.title.strip():
            raise ValueError(
                "Navigation title cannot be empty.",
            )

        if self.dashboard and self.dashboard.order < 0:
            raise ValueError(
                "Dashboard order cannot be negative.",
            )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def permission_count(
        self,
    ) -> int:
        return len(
            self.permissions,
        )

    @property
    def feature_flag_count(
        self,
    ) -> int:
        return len(
            self.feature_flags,
        )

    @property
    def has_navigation(
        self,
    ) -> bool:
        return self.navigation is not None

    @property
    def has_dashboard(
        self,
    ) -> bool:
        return self.dashboard is not None and self.dashboard.enabled

    @property
    def is_active(
        self,
    ) -> bool:

        return self.status is ModuleStatus.ACTIVE

    @property
    def is_available(
        self,
    ) -> bool:

        return self.enabled and self.is_active

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def with_enabled(
        self,
        enabled: bool,
    ) -> ModuleContract:

        return replace(
            self,
            enabled=enabled,
        )

    def with_metadata(
        self,
        **metadata: Any,
    ) -> ModuleContract:

        return replace(
            self,
            metadata={
                **self.metadata,
                **metadata,
            },
        )

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return {
            "identifier": self.identifier,
            "name": self.name,
            "display_name": self.display_name,
            "category": self.category.value,
            "version": self.version,
            "description": self.description,
            "icon": self.icon,
            "route": self.route,
            "api_prefix": self.api_prefix,
            "enabled": self.enabled,
            "system": self.system,
            "tenant_scoped": self.tenant_scoped,
            "order": self.order,
            "navigation": (
                {
                    "title": self.navigation.title,
                    "route": self.navigation.route,
                    "icon": self.navigation.icon,
                    "category": self.navigation.category,
                    "order": self.navigation.order,
                }
                if self.navigation
                else None
            ),
            "dashboard": (
                {
                    "enabled": self.dashboard.enabled,
                    "title": self.dashboard.title,
                    "description": self.dashboard.description,
                    "icon": self.dashboard.icon,
                    "route": self.dashboard.route,
                    "order": self.dashboard.order,
                }
                if self.dashboard
                else None
            ),
            "tags": list(self.tags),
            "permissions": list(self.permissions),
            "dependencies": list(self.dependencies),
            "optional_dependencies": list(
                self.optional_dependencies,
            ),
            "feature_flags": list(
                self.feature_flags,
            ),
            "metadata": dict(
                self.metadata,
            ),
            "status": self.status.value,
            "owner": self.owner,
            "homepage": self.homepage,
            "documentation": self.documentation,
            "support_email": self.support_email,
            "license": self.license,
        }


__all__ = [
    "NavigationConfig",
    "DashboardConfig",
    "ModuleContract",
]
