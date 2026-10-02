from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "providers"


def providers_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Providers",
        display_name="Providers",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description="Providers workspace and operational capabilities.",
        icon="/static/datavionos/icons/providers.svg",
        route="/workspace/providers",
        api_prefix="/api/providers",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=75,
        navigation=NavigationConfig(
            title="Providers",
            route="/workspace/providers",
            icon="grid",
            category="clinical",
            order=75,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Providers",
            description="Providers workspace and operational capabilities.",
            icon="grid",
            route="/workspace/providers",
            order=75,
        ),
        tags=("clinical", "providers"),
        permissions=("providers.view",),
        dependencies=(),
        optional_dependencies=(),
        feature_flags=(),
        metadata={
            "domain": "clinical",
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
