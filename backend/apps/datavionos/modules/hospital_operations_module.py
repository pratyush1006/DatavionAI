from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "hospital-operations"


def hospital_operations_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Hospital Operations",
        display_name="Hospital Operations",
        category=ModuleCategory.CORE,
        version="1.0.0",
        description="Hospital Operations workspace and operational capabilities.",
        icon="/static/datavionos/icons/hospital-operations.svg",
        route="/workspace/hospital-operations",
        api_prefix="/api/hospital-operations",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=120,
        navigation=NavigationConfig(
            title="Hospital Operations",
            route="/workspace/hospital-operations",
            icon="grid",
            category="core",
            order=120,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Hospital Operations",
            description="Hospital Operations workspace and operational capabilities.",
            icon="grid",
            route="/workspace/hospital-operations",
            order=120,
        ),
        tags=("core", "hospital-operations"),
        permissions=("hospital_operations.view",),
        dependencies=(),
        optional_dependencies=(),
        feature_flags=(),
        metadata={
            "domain": "core",
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
