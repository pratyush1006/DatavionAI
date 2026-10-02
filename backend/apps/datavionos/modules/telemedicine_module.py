from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "telemedicine"


def telemedicine_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Telemedicine",
        display_name="Telemedicine",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description="Telemedicine workspace and operational capabilities.",
        icon="/static/datavionos/icons/telemedicine.svg",
        route="/workspace/telemedicine",
        api_prefix="/api/telemedicine",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=125,
        navigation=NavigationConfig(
            title="Telemedicine",
            route="/workspace/telemedicine",
            icon="grid",
            category="clinical",
            order=125,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Telemedicine",
            description="Telemedicine workspace and operational capabilities.",
            icon="grid",
            route="/workspace/telemedicine",
            order=125,
        ),
        tags=("clinical", "telemedicine"),
        permissions=("telemedicine.view",),
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
