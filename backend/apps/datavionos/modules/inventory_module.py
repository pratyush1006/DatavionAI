from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)


def inventory_module() -> ModuleContract:
    return ModuleContract(
        identifier="inventory",
        name="Inventory",
        display_name="Inventory Management",
        category=ModuleCategory.UTILITY,
        version="1.0.0",
        description="Central inventory, procurement, stock movement, and transfer operations.",
        icon="/static/datavionos/icons/inventory.svg",
        route="/workspace/inventory",
        api_prefix="/api/pharmacy",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=108,
        navigation=NavigationConfig(
            title="Inventory",
            route="/workspace/inventory",
            icon="boxes",
            category="operations",
            order=108,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Inventory",
            description="Central inventory operations.",
            icon="boxes",
            route="/workspace/inventory",
            order=108,
        ),
        tags=("operations", "inventory", "supply-chain"),
        permissions=("inventory.view",),
        dependencies=("pharmacy",),
        optional_dependencies=(),
        feature_flags=(),
        metadata={
            "domain": "operations",
            "source": "datavionos-canonical-module-catalog",
        },
        status=ModuleStatus.ACTIVE,
        owner="datavionos",
        homepage="",
        documentation="",
        support_email="",
        license="",
    )
