from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "insurance"


def insurance_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Insurance",
        display_name="Insurance",
        category=ModuleCategory.FINANCIAL,
        version="1.0.0",
        description="Insurance workspace and operational capabilities.",
        icon="/static/datavionos/icons/insurance.svg",
        route="/workspace/insurance",
        api_prefix="/api/insurance",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=130,
        navigation=NavigationConfig(
            title="Insurance",
            route="/workspace/insurance",
            icon="grid",
            category="financial",
            order=130,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Insurance",
            description="Insurance workspace and operational capabilities.",
            icon="grid",
            route="/workspace/insurance",
            order=130,
        ),
        tags=("financial", "insurance"),
        permissions=("insurance.view",),
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
