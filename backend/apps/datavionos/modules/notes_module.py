from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "notes"


def notes_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Notes",
        display_name="Notes",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description="Notes workspace and operational capabilities.",
        icon="/static/datavionos/icons/notes.svg",
        route="/workspace/notes",
        api_prefix="/api/notes",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=170,
        navigation=NavigationConfig(
            title="Notes",
            route="/workspace/notes",
            icon="grid",
            category="clinical",
            order=170,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Notes",
            description="Notes workspace and operational capabilities.",
            icon="grid",
            route="/workspace/notes",
            order=170,
        ),
        tags=("clinical", "notes"),
        permissions=("notes.view",),
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
