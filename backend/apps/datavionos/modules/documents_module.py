from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "documents"


def documents_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Documents",
        display_name="Documents",
        category=ModuleCategory.CORE,
        version="1.0.0",
        description="Documents workspace and operational capabilities.",
        icon="/static/datavionos/icons/documents.svg",
        route="/workspace/documents",
        api_prefix="/api/documents",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=200,
        navigation=NavigationConfig(
            title="Documents",
            route="/workspace/documents",
            icon="grid",
            category="core",
            order=200,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Documents",
            description="Documents workspace and operational capabilities.",
            icon="grid",
            route="/workspace/documents",
            order=200,
        ),
        tags=("core", "documents"),
        permissions=("documents.view",),
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
