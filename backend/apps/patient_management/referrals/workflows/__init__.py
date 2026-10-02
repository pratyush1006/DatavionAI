"""
Patient Referral workflows.
"""

from __future__ import annotations

from apps.patient_management.referrals.workflows.creation import (
    ReferralCreationData,
    ReferralCreationRequest,
    ReferralCreationWorkflow,
)
from apps.patient_management.referrals.workflows.deletion import (
    ReferralDeletionRequest,
    ReferralDeletionWorkflow,
)
from apps.patient_management.referrals.workflows.lifecycle import (
    ReferralLifecycleRequest,
    ReferralLifecycleWorkflow,
)
from apps.patient_management.referrals.workflows.restore import (
    ReferralRestoreRequest,
    ReferralRestoreWorkflow,
)
from apps.patient_management.referrals.workflows.update import (
    ReferralUpdateRequest,
    ReferralUpdateWorkflow,
)

__all__ = (
    "ReferralCreationData",
    "ReferralCreationRequest",
    "ReferralCreationWorkflow",
    "ReferralDeletionRequest",
    "ReferralDeletionWorkflow",
    "ReferralLifecycleRequest",
    "ReferralLifecycleWorkflow",
    "ReferralRestoreRequest",
    "ReferralRestoreWorkflow",
    "ReferralUpdateRequest",
    "ReferralUpdateWorkflow",
)
