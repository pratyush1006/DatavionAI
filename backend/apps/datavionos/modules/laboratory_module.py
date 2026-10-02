from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "laboratory"


def laboratory_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Laboratory",
        display_name="Laboratory",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description="Laboratory workspace and operational capabilities.",
        icon="/static/datavionos/icons/laboratory.svg",
        route="/workspace/laboratory",
        api_prefix="/api/laboratory",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=110,
        navigation=NavigationConfig(
            title="Laboratory",
            route="/workspace/laboratory",
            icon="grid",
            category="clinical",
            order=110,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Laboratory",
            description="Laboratory workspace and operational capabilities.",
            icon="grid",
            route="/workspace/laboratory",
            order=110,
        ),
        tags=("clinical", "laboratory"),
        permissions=("laboratories.view",),
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
