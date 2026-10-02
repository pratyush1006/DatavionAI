from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "prescriptions"


def prescriptions_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Prescriptions",
        display_name="Prescriptions",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description="Prescriptions workspace and operational capabilities.",
        icon="/static/datavionos/icons/prescriptions.svg",
        route="/workspace/prescriptions",
        api_prefix="/api/prescriptions",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=118,
        navigation=NavigationConfig(
            title="Prescriptions",
            route="/workspace/prescriptions",
            icon="grid",
            category="clinical",
            order=118,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Prescriptions",
            description="Prescriptions workspace and operational capabilities.",
            icon="grid",
            route="/workspace/prescriptions",
            order=118,
        ),
        tags=("clinical", "prescriptions"),
        permissions=("prescriptions.view",),
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
