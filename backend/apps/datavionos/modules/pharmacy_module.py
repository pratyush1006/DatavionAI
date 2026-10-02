from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "pharmacy"


def pharmacy_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Pharmacy",
        display_name="Pharmacy",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description="Pharmacy workspace and operational capabilities.",
        icon="/static/datavionos/icons/pharmacy.svg",
        route="/workspace/pharmacy",
        api_prefix="/api/pharmacy",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=105,
        navigation=NavigationConfig(
            title="Pharmacy",
            route="/workspace/pharmacy",
            icon="grid",
            category="clinical",
            order=105,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Pharmacy",
            description="Pharmacy workspace and operational capabilities.",
            icon="grid",
            route="/workspace/pharmacy",
            order=105,
        ),
        tags=("clinical", "pharmacy"),
        permissions=("pharmacy.view",),
        dependencies=(),
        optional_dependencies=(),
        feature_flags=(),
        metadata={
            "domain": "clinical",
            "tenant_types": ("clinic", "hospital", "pharmacy", "enterprise"),
            "source": "datavionos-canonical-module-catalog",
        },
        status=ModuleStatus.ACTIVE,
        owner="datavionos",
        homepage="",
        documentation="",
        support_email="",
        license="",
    )
