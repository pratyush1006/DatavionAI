"""
Built-in RBAC role permissions.

Defines default permissions assigned to
system roles in DatavionOS.

Supports:

- Multi-tenant SaaS RBAC
- Healthcare roles
- AI platform access
- Audit compliance
"""

from __future__ import annotations

from apps.platform.rbac.constants import (
    PermissionAction,
    PermissionModule,
    SystemRole,
)


def permissions_for(
    module: PermissionModule,
    *actions: PermissionAction,
) -> list[str]:
    """
    Build permission codes for a module.
    """

    return [f"{module.value}.{action.value}" for action in actions]


SYSTEM_ROLE_PERMISSIONS = {
    # =========================================================================
    # Platform Administrator
    # =========================================================================
    SystemRole.PLATFORM_ADMIN.value: [
        "*",
    ],
    # =========================================================================
    # Organization Owner
    # =========================================================================
    SystemRole.ORGANIZATION_OWNER.value: (
        permissions_for(
            PermissionModule.ORGANIZATIONS,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.EMPLOYEES,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.DEPARTMENTS,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.TEAMS,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.PROVIDERS,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.PATIENTS,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.APPOINTMENTS,
            *PermissionAction,
        )
        # ---------------------------------------------------------------------
        # RBAC Administration
        # ---------------------------------------------------------------------
        + permissions_for(
            PermissionModule.RBAC,
            *PermissionAction,
        )
        # ---------------------------------------------------------------------
        # AI Platform
        # ---------------------------------------------------------------------
        + permissions_for(
            PermissionModule.AI,
            *PermissionAction,
        )
        # ---------------------------------------------------------------------
        # Compliance Audit
        # ---------------------------------------------------------------------
        + permissions_for(
            PermissionModule.AUDIT,
            PermissionAction.VIEW,
            PermissionAction.EXPORT,
        )
    ),
    # =========================================================================
    # Organization Administrator
    # =========================================================================
    SystemRole.ORGANIZATION_ADMIN.value: (
        permissions_for(
            PermissionModule.PATIENTS,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.APPOINTMENTS,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.ENCOUNTERS,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.EMPLOYEES,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        )
        # RBAC visibility
        + permissions_for(
            PermissionModule.RBAC,
            PermissionAction.VIEW,
        )
        # AI access
        + permissions_for(
            PermissionModule.AI,
            PermissionAction.VIEW,
        )
        # Audit visibility
        + permissions_for(
            PermissionModule.AUDIT,
            PermissionAction.VIEW,
        )
    ),
    # =========================================================================
    # Doctor
    # =========================================================================
    SystemRole.DOCTOR.value: (
        permissions_for(
            PermissionModule.PATIENTS,
            PermissionAction.VIEW,
            PermissionAction.UPDATE,
        )
        + permissions_for(
            PermissionModule.ENCOUNTERS,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.PRESCRIPTIONS,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.DIAGNOSES,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.ALLERGIES,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.VITALS,
            *PermissionAction,
        )
    ),
    # =========================================================================
    # Consultant
    # =========================================================================
    SystemRole.CONSULTANT.value: (
        permissions_for(
            PermissionModule.PATIENTS,
            PermissionAction.VIEW,
        )
        + permissions_for(
            PermissionModule.ENCOUNTERS,
            PermissionAction.VIEW,
        )
    ),
    # =========================================================================
    # Nurse
    # =========================================================================
    SystemRole.NURSE.value: (
        permissions_for(
            PermissionModule.PATIENTS,
            PermissionAction.VIEW,
            PermissionAction.UPDATE,
        )
        + permissions_for(
            PermissionModule.VITALS,
            *PermissionAction,
        )
    ),
    # =========================================================================
    # Laboratory Manager
    # =========================================================================
    SystemRole.LABORATORY_MANAGER.value: (
        permissions_for(
            PermissionModule.LABORATORIES,
            *PermissionAction,
        )
    ),
    # =========================================================================
    # Laboratory Technician
    # =========================================================================
    SystemRole.LABORATORY_TECHNICIAN.value: (
        permissions_for(
            PermissionModule.LABORATORIES,
            PermissionAction.VIEW,
            PermissionAction.UPDATE,
            PermissionAction.RELEASE,
        )
    ),
    # =========================================================================
    # Pharmacist
    # =========================================================================
    SystemRole.PHARMACIST.value: (
        permissions_for(
            PermissionModule.PHARMACY,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.MEDICATIONS,
            PermissionAction.VIEW,
        )
    ),
    # =========================================================================
    # Receptionist
    # =========================================================================
    SystemRole.RECEPTIONIST.value: (
        permissions_for(
            PermissionModule.PATIENTS,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
        )
        + permissions_for(
            PermissionModule.APPOINTMENTS,
            *PermissionAction,
        )
    ),
    # =========================================================================
    # Patient
    # =========================================================================
    SystemRole.PATIENT.value: (
        permissions_for(
            PermissionModule.PATIENTS,
            PermissionAction.VIEW,
        )
        + permissions_for(
            PermissionModule.APPOINTMENTS,
            PermissionAction.VIEW,
        )
    ),
    # =========================================================================
    # AI Agent
    # =========================================================================
    SystemRole.AI_AGENT.value: (
        permissions_for(
            PermissionModule.AI,
            *PermissionAction,
        )
    ),
}


__all__ = [
    "SYSTEM_ROLE_PERMISSIONS",
]
