from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "allergies"


def allergies_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Allergies",
        display_name="Allergies",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description="Allergies workspace and operational capabilities.",
        icon="/static/datavionos/icons/allergies.svg",
        route="/workspace/allergies",
        api_prefix="/api/allergies",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=70,
        navigation=NavigationConfig(
            title="Allergies",
            route="/workspace/allergies",
            icon="grid",
            category="clinical",
            order=70,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Allergies",
            description="Allergies workspace and operational capabilities.",
            icon="grid",
            route="/workspace/allergies",
            order=70,
        ),
        tags=("clinical", "allergies"),
        permissions=("allergies.view",),
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
