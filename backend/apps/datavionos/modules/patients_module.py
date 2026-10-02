from __future__ import annotations

from apps.datavionos.constants import (
    ModuleCategory,
    ModuleStatus,
)
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

PATIENT_MANAGEMENT_MODULE_ID = "patients"


def patient_management_module() -> ModuleContract:
    """Return the canonical Patients runtime module contract."""

    return ModuleContract(
        identifier=PATIENT_MANAGEMENT_MODULE_ID,
        name="Patient Management",
        display_name="Patients",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description="Patient registration, records, and clinical patient management.",
        icon="/static/datavionos/icons/patients.svg",
        route="/patients",
        api_prefix="/api/patients",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=60,
        navigation=NavigationConfig(
            title="Patients",
            route="/patients",
            icon="users",
            category="clinical",
            order=60,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Patients",
            description="Patient registration, records, and clinical patient management.",
            icon="users",
            route="/patients",
            order=60,
        ),
        tags=("clinical", "patients"),
        permissions=(
            "patients.view",
            "patients.create",
            "patients.update",
            "patients.delete",
        ),
        dependencies=(),
        optional_dependencies=(),
        feature_flags=("patients.dashboard",),
        metadata={
            "domain": "clinical",
            "tenant_types": ["clinic", "hospital", "enterprise"],
            "domain_module": "patient-management",
            "submodules": [
                "registration",
                "patients",
                "profile",
                "mpi",
                "addresses",
                "contacts",
                "emergency",
                "emergency_contacts",
                "communication",
                "consents",
                "medical_history",
                "relationships",
                "family_members",
                "referrals",
                "patient_documents",
                "portal",
                "preferences",
                "timeline",
            ],
            "family_members_parent": "patient-management",
            "family_members_protected": True,
        },
        status=ModuleStatus.ACTIVE,
        owner="datavionos",
        homepage="",
        documentation="",
        support_email="",
        license="",
    )


__all__ = [
    "PATIENT_MANAGEMENT_MODULE_ID",
    "patient_management_module",
]
