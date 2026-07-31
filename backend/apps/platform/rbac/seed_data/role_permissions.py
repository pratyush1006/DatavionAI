"""
Built-in RBAC role permissions.

Defines default permissions assigned to
system roles in DatavionOS.

Supports:

- Multi-tenant SaaS RBAC
- Healthcare roles
- AI platform access
- Document access control
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
        + permissions_for(
            PermissionModule.DOCUMENTS,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.RBAC,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.AI,
            *PermissionAction,
        )
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
        + permissions_for(
            PermissionModule.DOCUMENTS,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.RBAC,
            PermissionAction.VIEW,
        )
        + permissions_for(
            PermissionModule.AI,
            PermissionAction.VIEW,
        )
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
        + permissions_for(
            PermissionModule.DOCUMENTS,
            PermissionAction.VIEW,
            PermissionAction.UPLOAD,
            PermissionAction.DOWNLOAD,
            PermissionAction.SHARE,
            PermissionAction.VERIFY,
            PermissionAction.SIGN,
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
        + permissions_for(
            PermissionModule.DOCUMENTS,
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
        + permissions_for(
            PermissionModule.DOCUMENTS,
            PermissionAction.VIEW,
            PermissionAction.UPLOAD,
            PermissionAction.DOWNLOAD,
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
        + permissions_for(
            PermissionModule.DOCUMENTS,
            PermissionAction.VIEW,
            PermissionAction.UPLOAD,
            PermissionAction.DOWNLOAD,
            PermissionAction.VERIFY,
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
        + permissions_for(
            PermissionModule.DOCUMENTS,
            PermissionAction.VIEW,
            PermissionAction.UPLOAD,
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
        + permissions_for(
            PermissionModule.DOCUMENTS,
            PermissionAction.VIEW,
            PermissionAction.DOWNLOAD,
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
        + permissions_for(
            PermissionModule.DOCUMENTS,
            PermissionAction.VIEW,
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
        + permissions_for(
            PermissionModule.DOCUMENTS,
            PermissionAction.VIEW,
            PermissionAction.DOWNLOAD,
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
        + permissions_for(
            PermissionModule.DOCUMENTS,
            PermissionAction.VIEW,
            PermissionAction.EXPORT,
        )
    ),
}


__all__ = [
    "SYSTEM_ROLE_PERMISSIONS",
]
