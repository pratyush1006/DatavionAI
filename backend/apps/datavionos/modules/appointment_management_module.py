"""
Appointment management module contracts for DatavionOS.
"""

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

APPOINTMENT_MANAGEMENT_MODULE_ID = "appointment-management"


def appointment_management_module() -> ModuleContract:
    """
    Return the Appointment Management module contract.
    """

    return ModuleContract(
        # ------------------------------------------------------------------
        # Identity
        # ------------------------------------------------------------------
        identifier=APPOINTMENT_MANAGEMENT_MODULE_ID,
        name="Appointment Management",
        display_name="Appointment Management",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description=(
            "Patient appointment management "
            "(scheduling, status updates, "
            "and related operations)."
        ),
        icon="/static/datavionos/icons/appointments.svg",
        route="/clinical/appointments",
        api_prefix="/api/clinical/appointments",
        # ------------------------------------------------------------------
        # Runtime
        # ------------------------------------------------------------------
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=70,
        # ------------------------------------------------------------------
        # Navigation
        # ------------------------------------------------------------------
        navigation=NavigationConfig(
            title="Appointments",
            route="/clinical/appointments",
            icon="calendar",
            category="clinical",
            order=70,
        ),
        # ------------------------------------------------------------------
        # Dashboard
        # ------------------------------------------------------------------
        dashboard=DashboardConfig(
            enabled=True,
            title="Appointments",
            description=(
                "Manage patient appointments, scheduling, and clinical workflows."
            ),
            icon="calendar",
            route="/clinical/appointments",
            order=70,
        ),
        # ------------------------------------------------------------------
        # Discovery
        # ------------------------------------------------------------------
        tags=(
            "clinical",
            "appointments",
        ),
        # ------------------------------------------------------------------
        # RBAC
        # ------------------------------------------------------------------
        permissions=(
            "appointments.view",
            "appointments.create",
            "appointments.update",
            "appointments.delete",
        ),
        # ------------------------------------------------------------------
        # Dependencies
        # ------------------------------------------------------------------
        dependencies=(),
        optional_dependencies=(),
        # ------------------------------------------------------------------
        # Feature Entitlement
        # ------------------------------------------------------------------
        feature_flags=("appointments",),
        # ------------------------------------------------------------------
        # SaaS Metadata
        # ------------------------------------------------------------------
        metadata={
            "domain": "clinical",
            "tenant_types": [
                "clinic",
                "hospital",
            ],
        },
        # ------------------------------------------------------------------
        # Lifecycle
        # ------------------------------------------------------------------
        status=ModuleStatus.ACTIVE,
        # ------------------------------------------------------------------
        # Ownership
        # ------------------------------------------------------------------
        owner="datavionos",
        homepage="",
        documentation="",
        support_email="",
        license="",
    )


__all__ = [
    "APPOINTMENT_MANAGEMENT_MODULE_ID",
    "appointment_management_module",
]
