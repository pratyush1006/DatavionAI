from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "vitals"


def vitals_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Clinical Vitals",
        display_name="Clinical Vitals",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description="Clinical Vitals workspace and operational capabilities.",
        icon="/static/datavionos/icons/vitals.svg",
        route="/workspace/vitals",
        api_prefix="/api/vitals",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=72,
        navigation=NavigationConfig(
            title="Clinical Vitals",
            route="/workspace/vitals",
            icon="grid",
            category="clinical",
            order=72,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Clinical Vitals",
            description="Clinical Vitals workspace and operational capabilities.",
            icon="grid",
            route="/workspace/vitals",
            order=72,
        ),
        tags=("clinical", "vitals"),
        permissions=("vitals.view",),
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
