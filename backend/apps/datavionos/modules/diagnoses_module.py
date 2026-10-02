from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "diagnoses"


def diagnoses_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Diagnoses",
        display_name="Diagnoses",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description="Diagnoses workspace and operational capabilities.",
        icon="/static/datavionos/icons/diagnoses.svg",
        route="/workspace/diagnoses",
        api_prefix="/api/diagnoses",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=80,
        navigation=NavigationConfig(
            title="Diagnoses",
            route="/workspace/diagnoses",
            icon="grid",
            category="clinical",
            order=80,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Diagnoses",
            description="Diagnoses workspace and operational capabilities.",
            icon="grid",
            route="/workspace/diagnoses",
            order=80,
        ),
        tags=("clinical", "diagnoses"),
        permissions=("diagnoses.view",),
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
