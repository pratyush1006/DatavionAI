from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "revenue-cycle"


def revenue_cycle_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Revenue Cycle",
        display_name="Revenue Cycle",
        category=ModuleCategory.FINANCIAL,
        version="1.0.0",
        description="Revenue Cycle workspace and operational capabilities.",
        icon="/static/datavionos/icons/revenue-cycle.svg",
        route="/workspace/revenue-cycle",
        api_prefix="/api/revenue-cycle",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=140,
        navigation=NavigationConfig(
            title="Revenue Cycle",
            route="/workspace/revenue-cycle",
            icon="grid",
            category="financial",
            order=140,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Revenue Cycle",
            description="Revenue Cycle workspace and operational capabilities.",
            icon="grid",
            route="/workspace/revenue-cycle",
            order=140,
        ),
        tags=("financial", "revenue-cycle"),
        permissions=("billing.view",),
        dependencies=(),
        optional_dependencies=(),
        feature_flags=(),
        metadata={
            "domain": "financial",
            "tenant_types": ("clinic", "hospital", "enterprise"),
            "source": "datavionos-canonical-module-catalog",
        },
        status=ModuleStatus.ACTIVE,
        owner="datavionos",
        homepage="",
        documentation="",
        support_email="",
        license="",
    )
