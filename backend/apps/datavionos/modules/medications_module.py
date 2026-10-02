from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "medications"


def medications_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Medications",
        display_name="Medications",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description="Medications workspace and operational capabilities.",
        icon="/static/datavionos/icons/medications.svg",
        route="/workspace/medications",
        api_prefix="/api/medications",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=115,
        navigation=NavigationConfig(
            title="Medications",
            route="/workspace/medications",
            icon="grid",
            category="clinical",
            order=115,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Medications",
            description="Medications workspace and operational capabilities.",
            icon="grid",
            route="/workspace/medications",
            order=115,
        ),
        tags=("clinical", "medications"),
        permissions=("medications.view",),
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
