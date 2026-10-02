from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "imaging"


def imaging_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Imaging",
        display_name="Imaging",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description="Imaging workspace and operational capabilities.",
        icon="/static/datavionos/icons/imaging.svg",
        route="/workspace/imaging",
        api_prefix="/api/imaging",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=100,
        navigation=NavigationConfig(
            title="Imaging",
            route="/workspace/imaging",
            icon="grid",
            category="clinical",
            order=100,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Imaging",
            description="Imaging workspace and operational capabilities.",
            icon="grid",
            route="/workspace/imaging",
            order=100,
        ),
        tags=("clinical", "imaging"),
        permissions=("imaging.view",),
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
