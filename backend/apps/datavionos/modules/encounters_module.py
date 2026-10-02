from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "encounters"


def encounters_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Encounters",
        display_name="Encounters",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description="Encounters workspace and operational capabilities.",
        icon="/static/datavionos/icons/encounters.svg",
        route="/workspace/encounters",
        api_prefix="/api/encounters",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=90,
        navigation=NavigationConfig(
            title="Encounters",
            route="/workspace/encounters",
            icon="grid",
            category="clinical",
            order=90,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Encounters",
            description="Encounters workspace and operational capabilities.",
            icon="grid",
            route="/workspace/encounters",
            order=90,
        ),
        tags=("clinical", "encounters"),
        permissions=("encounters.view",),
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
