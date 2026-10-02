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
    permission_actions_for,
)


def permissions_for(
    module: PermissionModule,
    *actions: PermissionAction,
) -> list[str]:
    allowed_actions = frozenset(
        permission_actions_for(module),
    )

    return [
        f"{module.value}.{action.value}"
        for action in actions
        if action in allowed_actions
    ]


HR_WORKFLOW_MODULES = (
    PermissionModule.ATTENDANCE,
    PermissionModule.LEAVE,
    PermissionModule.SHIFTS,
    PermissionModule.HOLIDAYS,
    PermissionModule.ONBOARDING,
    PermissionModule.PAYROLL,
    PermissionModule.PERFORMANCE,
    PermissionModule.RECRUITMENT,
)


def hr_workflow_permissions(*actions: PermissionAction) -> list[str]:
    return [
        code
        for module in HR_WORKFLOW_MODULES
        for code in permissions_for(module, *actions)
    ]


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
            PermissionModule.TELEMEDICINE,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.DELETE,
            PermissionAction.ACTIVATE,
            PermissionAction.DEACTIVATE,
            PermissionAction.SUSPEND,
            PermissionAction.RESTORE,
            PermissionAction.APPROVE,
            PermissionAction.ASSIGN,
            PermissionAction.CONTRACT,
            PermissionAction.ONBOARD,
            PermissionAction.OFFBOARD,
            PermissionAction.VERIFY,
            PermissionAction.RELEASE,
            PermissionAction.SIGN,
            PermissionAction.UPLOAD,
            PermissionAction.DOWNLOAD,
            PermissionAction.EXPORT,
            PermissionAction.IMPORT,
            PermissionAction.SHARE,
            PermissionAction.PRINT,
            PermissionAction.CANCEL,
            PermissionAction.SCHEDULE,
            PermissionAction.CONFIRM,
            PermissionAction.PREPARE,
            PermissionAction.START,
            PermissionAction.COMPLETE,
            PermissionAction.NO_SHOW,
            PermissionAction.FAIL,
            PermissionAction.PARTICIPANT_MANAGE,
            PermissionAction.RECORDING_MANAGE,
        )
        + permissions_for(
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
            PermissionModule.HR,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.HOSPITAL_OPERATIONS,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.DEVICES,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.IMAGING,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.NOTES,
            *PermissionAction,
        )
        + permissions_for(
            PermissionModule.TRANSCRIPTION,
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
            PermissionModule.TELEMEDICINE,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.DELETE,
            PermissionAction.CANCEL,
            PermissionAction.SCHEDULE,
            PermissionAction.CONFIRM,
            PermissionAction.PREPARE,
            PermissionAction.START,
            PermissionAction.COMPLETE,
            PermissionAction.NO_SHOW,
            PermissionAction.FAIL,
            PermissionAction.PARTICIPANT_MANAGE,
            PermissionAction.RECORDING_MANAGE,
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
            PermissionModule.DEPARTMENTS,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        )
        + permissions_for(
            PermissionModule.TEAMS,
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
            PermissionAction.ASSIGN,
        )
        + permissions_for(
            PermissionModule.AI,
            PermissionAction.VIEW,
        )
        + permissions_for(
            PermissionModule.HR,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        )
        + permissions_for(
            PermissionModule.HOSPITAL_OPERATIONS,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        )
        + permissions_for(
            PermissionModule.NURSING,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.DELETE,
        )
        + permissions_for(
            PermissionModule.DEVICES,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        )
        + permissions_for(
            PermissionModule.IMAGING,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        )
        + permissions_for(
            PermissionModule.NOTES,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        )
        + permissions_for(
            PermissionModule.TRANSCRIPTION,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
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
            PermissionModule.AI,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.VERIFY,
            PermissionAction.SIGN,
        )
        + permissions_for(
            PermissionModule.TELEMEDICINE,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.CANCEL,
            PermissionAction.SCHEDULE,
            PermissionAction.CONFIRM,
            PermissionAction.PREPARE,
            PermissionAction.START,
            PermissionAction.COMPLETE,
            PermissionAction.NO_SHOW,
            PermissionAction.FAIL,
            PermissionAction.PARTICIPANT_MANAGE,
            PermissionAction.RECORDING_MANAGE,
        )
        + permissions_for(
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
            PermissionModule.MEDICATIONS,
            PermissionAction.VIEW,
        )
        + permissions_for(
            PermissionModule.IMAGING,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        )
        + permissions_for(
            PermissionModule.NOTES,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.SIGN,
        )
        + permissions_for(
            PermissionModule.TRANSCRIPTION,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
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
            PermissionModule.TELEMEDICINE,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.SCHEDULE,
            PermissionAction.CONFIRM,
            PermissionAction.PREPARE,
            PermissionAction.START,
            PermissionAction.COMPLETE,
            PermissionAction.PARTICIPANT_MANAGE,
            PermissionAction.RECORDING_MANAGE,
        )
        + permissions_for(
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
            PermissionModule.NURSING,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        )
        + permissions_for(
            PermissionModule.TELEMEDICINE,
            PermissionAction.VIEW,
            PermissionAction.PARTICIPANT_MANAGE,
        )
        + permissions_for(
            PermissionModule.PATIENTS,
            PermissionAction.VIEW,
            PermissionAction.UPDATE,
        )
        + permissions_for(
            PermissionModule.APPOINTMENTS,
            PermissionAction.VIEW,
        )
        + permissions_for(
            PermissionModule.ENCOUNTERS,
            PermissionAction.VIEW,
        )
        + permissions_for(
            PermissionModule.PRESCRIPTIONS,
            PermissionAction.VIEW,
        )
        + permissions_for(
            PermissionModule.MEDICATIONS,
            PermissionAction.VIEW,
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
        + permissions_for(
            PermissionModule.NOTES,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
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
        + [
            "pharmacy.manage",
            "pharmacy.inventory",
            "pharmacy.purchasing",
            "pharmacy.dispense",
        ]
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
    SystemRole.BILLING_OFFICER.value: (
        permissions_for(
            PermissionModule.BILLING,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.APPROVE,
            PermissionAction.EXPORT,
        )
        + permissions_for(
            PermissionModule.INSURANCE,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        )
        + permissions_for(
            PermissionModule.DOCUMENTS,
            PermissionAction.VIEW,
            PermissionAction.UPLOAD,
            PermissionAction.DOWNLOAD,
        )
    ),
    # =========================================================================
    # HR Manager
    # =========================================================================
    SystemRole.HR_MANAGER.value: (
        permissions_for(PermissionModule.HR, *PermissionAction)
        + hr_workflow_permissions(
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.DELETE,
            PermissionAction.APPROVE,
            PermissionAction.VERIFY,
            PermissionAction.RELEASE,
            PermissionAction.EXPORT,
        )
        + permissions_for(PermissionModule.EMPLOYEES, *PermissionAction)
        + permissions_for(PermissionModule.DEPARTMENTS, *PermissionAction)
        + permissions_for(PermissionModule.TEAMS, *PermissionAction)
        + permissions_for(
            PermissionModule.DOCUMENTS,
            PermissionAction.VIEW,
            PermissionAction.UPLOAD,
            PermissionAction.DOWNLOAD,
            PermissionAction.SHARE,
        )
    ),
    # =========================================================================
    # Receptionist
    # =========================================================================
    SystemRole.RECEPTIONIST.value: (
        permissions_for(
            PermissionModule.TELEMEDICINE,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.DELETE,
            PermissionAction.CANCEL,
            PermissionAction.SCHEDULE,
            PermissionAction.CONFIRM,
        )
        + permissions_for(
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
            PermissionModule.TELEMEDICINE,
            PermissionAction.VIEW,
        )
        + permissions_for(
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

# Least-privilege defaults for the canonical roles added after the original
# seed set.  They deliberately contain no wildcard except Platform Owner.
SYSTEM_ROLE_PERMISSIONS.update(
    {
        SystemRole.PLATFORM_OWNER.value: ["*"],
        SystemRole.PLATFORM_OPERATIONS.value: permissions_for(
            PermissionModule.ORGANIZATIONS,
            PermissionAction.VIEW,
            PermissionAction.UPDATE,
        )
        + permissions_for(PermissionModule.AUDIT, PermissionAction.VIEW),
        SystemRole.PLATFORM_SECURITY.value: permissions_for(
            PermissionModule.AUDIT, PermissionAction.VIEW, PermissionAction.EXPORT
        )
        + permissions_for(PermissionModule.RBAC, PermissionAction.VIEW),
        SystemRole.PLATFORM_SUPPORT.value: permissions_for(
            PermissionModule.ORGANIZATIONS, PermissionAction.VIEW
        )
        + permissions_for(PermissionModule.ACCOUNTS, PermissionAction.VIEW),
        SystemRole.PLATFORM_FINANCE.value: permissions_for(
            PermissionModule.BILLING, PermissionAction.VIEW, PermissionAction.EXPORT
        ),
        SystemRole.ORGANIZATION_MANAGER.value: permissions_for(
            PermissionModule.EMPLOYEES, PermissionAction.VIEW, PermissionAction.UPDATE
        )
        + permissions_for(
            PermissionModule.DEPARTMENTS, PermissionAction.VIEW, PermissionAction.UPDATE
        )
        + permissions_for(
            PermissionModule.TEAMS, PermissionAction.VIEW, PermissionAction.UPDATE
        ),
        SystemRole.THERAPIST.value: permissions_for(
            PermissionModule.PATIENTS, PermissionAction.VIEW
        )
        + permissions_for(
            PermissionModule.ENCOUNTERS,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        ),
        SystemRole.CLINICAL_MANAGER.value: permissions_for(
            PermissionModule.PATIENTS, PermissionAction.VIEW
        )
        + permissions_for(
            PermissionModule.ENCOUNTERS,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        )
        + permissions_for(PermissionModule.EMPLOYEES, PermissionAction.VIEW)
        + permissions_for(PermissionModule.NURSING, *PermissionAction),
        SystemRole.FRONT_DESK_MANAGER.value: permissions_for(
            PermissionModule.APPOINTMENTS, *PermissionAction
        )
        + permissions_for(
            PermissionModule.PATIENTS,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        ),
        SystemRole.HR_EXECUTIVE.value: hr_workflow_permissions(
            PermissionAction.VIEW, PermissionAction.CREATE, PermissionAction.UPDATE
        )
        + permissions_for(
            PermissionModule.EMPLOYEES,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.ASSIGN,
            PermissionAction.ONBOARD,
            PermissionAction.OFFBOARD,
            PermissionAction.ACTIVATE,
            PermissionAction.DEACTIVATE,
        )
        + permissions_for(
            PermissionModule.HR,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        ),
        SystemRole.ACCOUNTANT.value: permissions_for(
            PermissionModule.BILLING,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.EXPORT,
        ),
        SystemRole.FINANCE_MANAGER.value: permissions_for(
            PermissionModule.BILLING, *PermissionAction
        )
        + permissions_for(
            PermissionModule.INSURANCE,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        ),
        SystemRole.PHARMACY_MANAGER.value: permissions_for(
            PermissionModule.PHARMACY, *PermissionAction
        )
        + [
            "pharmacy.manage",
            "pharmacy.inventory",
            "pharmacy.purchasing",
            "pharmacy.purchasing.approve",
            "pharmacy.dispense",
        ],
        SystemRole.INVENTORY_MANAGER.value: permissions_for(
            PermissionModule.INVENTORY, *PermissionAction
        )
        + permissions_for(PermissionModule.PHARMACY, PermissionAction.VIEW)
        + [
            "pharmacy.manage",
            "pharmacy.inventory",
            "pharmacy.purchasing",
            "pharmacy.purchasing.approve",
        ],
        SystemRole.IMAGING_TECHNICIAN.value: permissions_for(
            PermissionModule.IMAGING,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        ),
        SystemRole.RADIOLOGIST.value: permissions_for(
            PermissionModule.IMAGING,
            PermissionAction.VIEW,
            PermissionAction.UPDATE,
            PermissionAction.APPROVE,
        ),
        SystemRole.IMAGING_MANAGER.value: permissions_for(
            PermissionModule.IMAGING, *PermissionAction
        ),
        SystemRole.DEPARTMENT_MANAGER.value: permissions_for(
            PermissionModule.DEPARTMENTS, *PermissionAction
        )
        + permissions_for(
            PermissionModule.EMPLOYEES, PermissionAction.VIEW, PermissionAction.ASSIGN
        ),
        SystemRole.TEAM_LEAD.value: permissions_for(
            PermissionModule.TEAMS, PermissionAction.VIEW, PermissionAction.UPDATE
        )
        + permissions_for(PermissionModule.EMPLOYEES, PermissionAction.VIEW),
        SystemRole.TELEMEDICINE_DOCTOR.value: permissions_for(
            PermissionModule.TELEMEDICINE,
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.START,
            PermissionAction.COMPLETE,
        )
        + permissions_for(PermissionModule.PATIENTS, PermissionAction.VIEW),
        SystemRole.FAMILY_CAREGIVER.value: permissions_for(
            PermissionModule.PATIENTS, PermissionAction.VIEW
        ),
        SystemRole.SUPPORT_AGENT.value: permissions_for(
            PermissionModule.DOCUMENTS, PermissionAction.VIEW
        )
        + permissions_for(PermissionModule.EMPLOYEES, PermissionAction.VIEW),
    }
)


SYSTEM_ROLE_PERMISSIONS[SystemRole.HR_EXECUTIVE.value] += permissions_for(
    PermissionModule.DEPARTMENTS, PermissionAction.VIEW
)

for _role_code, _codes in SYSTEM_ROLE_PERMISSIONS.items():
    _actions = [action for action in PermissionAction if f"hr.{action.value}" in _codes]
    SYSTEM_ROLE_PERMISSIONS[_role_code] = list(
        dict.fromkeys(_codes + hr_workflow_permissions(*_actions))
    )


__all__ = [
    "SYSTEM_ROLE_PERMISSIONS",
]
