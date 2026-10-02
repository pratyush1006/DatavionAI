"""
Workflow registration for Patient Family Members.
"""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.patient_management.family_members.workflows import (
    FamilyMemberActivationWorkflow,
    FamilyMemberCreationWorkflow,
    FamilyMemberDeactivationWorkflow,
    FamilyMemberDeletionWorkflow,
    FamilyMemberEmergencyContactWorkflow,
    FamilyMemberNextOfKinWorkflow,
    FamilyMemberRestoreWorkflow,
    FamilyMemberUpdateWorkflow,
)


def register_family_member_workflows() -> None:
    """Register Family Member workflows idempotently."""

    workflows = {
        "family_member.create": FamilyMemberCreationWorkflow,
        "family_member.update": FamilyMemberUpdateWorkflow,
        "family_member.delete": FamilyMemberDeletionWorkflow,
        "family_member.restore": FamilyMemberRestoreWorkflow,
        "family_member.activate": FamilyMemberActivationWorkflow,
        "family_member.deactivate": FamilyMemberDeactivationWorkflow,
        "family_member.set_next_of_kin": FamilyMemberNextOfKinWorkflow,
        "family_member.set_emergency_contact": (FamilyMemberEmergencyContactWorkflow),
    }

    for name, workflow in workflows.items():
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__ = ("register_family_member_workflows",)
