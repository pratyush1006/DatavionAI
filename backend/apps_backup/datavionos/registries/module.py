"""
DatavionOS module registry.

Central registry for all platform modules.

Responsibilities:

- Define available DatavionOS modules
- Resolve module metadata
- Provide runtime module configuration

Module availability is controlled by SaaS Plan entitlements.

Architecture:

Plan.modules
      |
      v
EntitlementResolver
      |
      v
ModuleRegistry
      |
      v
Bootstrap Payload
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class PlatformModule:
    """
    DatavionOS platform module metadata.
    """

    code: str

    name: str

    description: str

    route: str

    icon: str

    category: str


class ModuleRegistry:
    """
    DatavionOS module registry.

    SaaS plans enable modules dynamically.
    """

    _modules: dict[str, PlatformModule] = {}

    @classmethod
    def register(
        cls,
        module: PlatformModule,
    ) -> None:
        """
        Register platform module.
        """

        cls._modules[module.code] = module

    @classmethod
    def get(
        cls,
        code: str,
    ) -> PlatformModule | None:
        """
        Get module metadata.
        """

        return cls._modules.get(
            code,
        )

    @classmethod
    def all(
        cls,
    ) -> dict[str, PlatformModule]:
        """
        Return all modules.
        """

        return cls._modules.copy()

    @classmethod
    def resolve_enabled(
        cls,
        enabled_modules: dict[str, bool],
    ) -> list[PlatformModule]:
        """
        Resolve modules enabled by subscription plan.
        """

        return [
            cls._modules[module]
            for module, enabled in enabled_modules.items()
            if enabled and module in cls._modules
        ]


# ==========================================================
# Core Healthcare Modules
# ==========================================================


ModuleRegistry.register(
    PlatformModule(
        code="patients",
        name="Patient Management",
        description="Patient registration and medical records",
        route="/patients",
        icon="users",
        category="clinical",
    )
)


ModuleRegistry.register(
    PlatformModule(
        code="appointments",
        name="Appointments",
        description="Scheduling and appointment management",
        route="/appointments",
        icon="calendar",
        category="clinical",
    )
)


ModuleRegistry.register(
    PlatformModule(
        code="clinical",
        name="Clinical Management",
        description="Clinical workflows and encounters",
        route="/clinical",
        icon="stethoscope",
        category="clinical",
    )
)


ModuleRegistry.register(
    PlatformModule(
        code="laboratory",
        name="Laboratory",
        description="Lab orders and diagnostics",
        route="/laboratory",
        icon="flask",
        category="diagnostics",
    )
)


ModuleRegistry.register(
    PlatformModule(
        code="pharmacy",
        name="Pharmacy",
        description="Medicine inventory and pharmacy workflows",
        route="/pharmacy",
        icon="pill",
        category="operations",
    )
)


ModuleRegistry.register(
    PlatformModule(
        code="imaging",
        name="Imaging",
        description="Radiology and imaging workflows",
        route="/imaging",
        icon="scan",
        category="diagnostics",
    )
)


ModuleRegistry.register(
    PlatformModule(
        code="ai",
        name="AI Healthcare Copilot",
        description="AI powered healthcare assistant",
        route="/ai",
        icon="brain",
        category="artificial_intelligence",
    )
)


ModuleRegistry.register(
    PlatformModule(
        code="billing",
        name="Billing",
        description="Subscription and billing management",
        route="/billing",
        icon="credit-card",
        category="platform",
    )
)

module_registry = ModuleRegistry()
__all__ = [
    "PlatformModule",
    "ModuleRegistry",
    "module_registry",
]
