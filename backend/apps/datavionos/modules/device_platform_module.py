from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "device-platform"


def device_platform_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Device Platform",
        display_name="Device Platform",
        category=ModuleCategory.CORE,
        version="1.0.0",
        description="Device Platform workspace and operational capabilities.",
        icon="/static/datavionos/icons/device-platform.svg",
        route="/workspace/device-platform",
        api_prefix="/api/device-platform",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=150,
        navigation=NavigationConfig(
            title="Device Platform",
            route="/workspace/device-platform",
            icon="grid",
            category="core",
            order=150,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Device Platform",
            description="Device Platform workspace and operational capabilities.",
            icon="grid",
            route="/workspace/device-platform",
            order=150,
        ),
        tags=("core", "device-platform"),
        permissions=("devices.view",),
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
