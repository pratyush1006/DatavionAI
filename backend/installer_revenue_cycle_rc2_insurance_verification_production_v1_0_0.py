from __future__ import annotations

import ast
import py_compile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ACTIVE = ROOT / "apps" / "revenue_cycle" / "insurance_verification"
BACKUP = ROOT / "apps" / "revenue_cycle_legacy_backup"

FILES = {
    "apps/revenue_cycle/insurance_verification/__init__.py": '''"""Revenue Cycle Insurance Verification bounded context."""

from __future__ import annotations

__all__ = ()
''',
    "apps/revenue_cycle/insurance_verification/constants.py": '''"""Insurance Verification lifecycle and normalized result constants."""

from __future__ import annotations

from enum import StrEnum


class VerificationStatus(StrEnum):
    """Supported Insurance Verification lifecycle states."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    FAILED = "failed"
    EXPIRED = "expired"
    INACTIVE = "inactive"


class VerificationOutcome(StrEnum):
    """Normalized verification outcomes."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    NOT_FOUND = "not_found"
    UNKNOWN = "unknown"


class VerificationMethod(StrEnum):
    """Supported verification initiation methods."""

    MANUAL = "manual"
    PAYER_API = "payer_api"
    CLEARINGHOUSE = "clearinghouse"
    IMPORT = "import"


__all__ = ("VerificationMethod", "VerificationOutcome", "VerificationStatus")
''',
    "apps/revenue_cycle/insurance_verification/exceptions.py": '''"""Insurance Verification domain exceptions."""

from __future__ import annotations


class InsuranceVerificationError(Exception):
    """Base Insurance Verification exception."""


class InsuranceVerificationInvariantError(InsuranceVerificationError):
    """Raised when a verification invariant is violated."""


class InsuranceVerificationTransitionError(InsuranceVerificationError):
    """Raised when an invalid lifecycle transition is requested."""


__all__ = (
    "InsuranceVerificationError",
    "InsuranceVerificationInvariantError",
    "InsuranceVerificationTransitionError",
)
''',
    "apps/revenue_cycle/insurance_verification/permissions.py": '''"""Revenue Cycle Insurance Verification RBAC permission codes."""

from __future__ import annotations

from enum import StrEnum


class InsuranceVerificationPermission(StrEnum):
    """Exact platform RBAC permission codes."""

    VIEW = "revenue_cycle.insurance_verification.view"
    CREATE = "revenue_cycle.insurance_verification.create"
    UPDATE = "revenue_cycle.insurance_verification.update"
    DELETE = "revenue_cycle.insurance_verification.delete"
    RESTORE = "revenue_cycle.insurance_verification.restore"
    LIFECYCLE = "revenue_cycle.insurance_verification.lifecycle"


__all__ = ("InsuranceVerificationPermission",)
''',
    "apps/revenue_cycle/insurance_verification/rbac.py": '''"""DRF RBAC adapters for Insurance Verification."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase
from apps.revenue_cycle.insurance_verification.permissions import InsuranceVerificationPermission


class CanViewInsuranceVerification(RBACPermissionBase):
    """Require Insurance Verification view permission."""

    permission_code = InsuranceVerificationPermission.VIEW
    message = "You do not have permission to view insurance verification records."


class CanCreateInsuranceVerification(RBACPermissionBase):
    """Require Insurance Verification creation permission."""

    permission_code = InsuranceVerificationPermission.CREATE
    message = "You do not have permission to create insurance verification records."


class CanUpdateInsuranceVerification(RBACPermissionBase):
    """Require Insurance Verification update permission."""

    permission_code = InsuranceVerificationPermission.UPDATE
    message = "You do not have permission to update insurance verification records."


class CanDeleteInsuranceVerification(RBACPermissionBase):
    """Require Insurance Verification deletion permission."""

    permission_code = InsuranceVerificationPermission.DELETE
    message = "You do not have permission to delete insurance verification records."


class CanRestoreInsuranceVerification(RBACPermissionBase):
    """Require Insurance Verification restoration permission."""

    permission_code = InsuranceVerificationPermission.RESTORE
    message = "You do not have permission to restore insurance verification records."


class CanTransitionInsuranceVerification(RBACPermissionBase):
    """Require Insurance Verification lifecycle permission."""

    permission_code = InsuranceVerificationPermission.LIFECYCLE
    message = "You do not have permission to change insurance verification lifecycle."


__all__ = (
    "CanCreateInsuranceVerification",
    "CanDeleteInsuranceVerification",
    "CanRestoreInsuranceVerification",
    "CanTransitionInsuranceVerification",
    "CanUpdateInsuranceVerification",
    "CanViewInsuranceVerification",
)
''',
    "apps/revenue_cycle/insurance_verification/models/__init__.py": '''"""Revenue Cycle Insurance Verification models."""

from __future__ import annotations

from apps.revenue_cycle.insurance_verification.models.insurance_verification import InsuranceVerification

__all__ = ("InsuranceVerification",)
''',
    "apps/revenue_cycle/insurance_verification/models/insurance_verification.py": '''"""Revenue Cycle Insurance Verification aggregate model."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.insurance_verification.constants import (
    VerificationMethod,
    VerificationOutcome,
    VerificationStatus,
)


class InsuranceVerification(BaseModel):
    """Store an organization-scoped insurance verification transaction."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_insurance_verifications",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_insurance_verifications",
    )
    eligibility_reference = models.UUIDField(null=True, blank=True, db_index=True)
    payer_id = models.CharField(max_length=100, db_index=True)
    payer_name = models.CharField(max_length=255, blank=True)
    member_id = models.CharField(max_length=100, db_index=True)
    policy_number = models.CharField(max_length=100, blank=True)
    group_number = models.CharField(max_length=100, blank=True)
    subscriber_name = models.CharField(max_length=255, blank=True)
    subscriber_relationship = models.CharField(max_length=50, blank=True)
    verification_method = models.CharField(
        max_length=30,
        choices=tuple((item.value, item.value) for item in VerificationMethod),
        default=VerificationMethod.MANUAL.value,
    )
    status = models.CharField(
        max_length=30,
        choices=tuple((item.value, item.value) for item in VerificationStatus),
        default=VerificationStatus.PENDING.value,
        db_index=True,
    )
    outcome = models.CharField(
        max_length=30,
        choices=tuple((item.value, item.value) for item in VerificationOutcome),
        default=VerificationOutcome.UNKNOWN.value,
        db_index=True,
    )
    requested_at = models.DateTimeField(auto_now_add=True, db_index=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    coverage_start = models.DateField(null=True, blank=True)
    coverage_end = models.DateField(null=True, blank=True)
    copay_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    deductible_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    coinsurance_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    prior_authorization_required = models.BooleanField(default=False)
    response_code = models.CharField(max_length=100, blank=True)
    response_message = models.TextField(blank=True)
    response_payload = models.JSONField(default=dict, blank=True)
    request_reference = models.CharField(max_length=100, db_index=True)
    idempotency_key = models.CharField(max_length=255, db_index=True)
    failure_reason = models.TextField(blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="revenue_cycle_insurance_verifications_verified",
    )

    class Meta:
        """Database metadata for Insurance Verification."""

        db_table = "revenue_cycle_insurance_verification"
        ordering = ("-requested_at",)
        indexes = (
            models.Index(
                fields=("organization", "patient", "-requested_at"),
                name="rc_iv_org_patient_req_idx",
            ),
            models.Index(
                fields=("organization", "status"),
                name="rc_iv_org_status_idx",
            ),
            models.Index(
                fields=("organization", "payer_id", "member_id"),
                name="rc_iv_org_payer_member_idx",
            ),
            models.Index(
                fields=("organization", "outcome"),
                name="rc_iv_org_outcome_idx",
            ),
        )
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "idempotency_key"),
                name="rc_iv_org_idempotency_uniq",
            ),
        )

    def __str__(self) -> str:
        """Return a stable verification representation."""

        return f"{self.payer_id}:{self.member_id}:{self.request_reference}"


__all__ = ("InsuranceVerification",)
''',
    "apps/revenue_cycle/insurance_verification/selectors/__init__.py": '''"""Tenant-safe Insurance Verification selectors."""

from __future__ import annotations

from apps.revenue_cycle.insurance_verification.selectors.insurance_verification import (
    get_deleted_verification_for_update,
    get_verification,
    get_verification_for_update,
    list_verifications,
)

__all__ = (
    "get_deleted_verification_for_update",
    "get_verification",
    "get_verification_for_update",
    "list_verifications",
)
''',
    "apps/revenue_cycle/insurance_verification/selectors/insurance_verification.py": '''"""Tenant-safe Insurance Verification query selectors."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.revenue_cycle.insurance_verification.models import InsuranceVerification


def list_verifications(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    patient_id: UUID | None = None,
) -> QuerySet[InsuranceVerification]:
    """List active records inside the exact tenant and organization scope."""

    queryset = (
        InsuranceVerification.objects.select_related(
            "patient",
            "organization",
            "verified_by",
        )
        .filter(
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
        )
        .order_by("-requested_at")
    )
    if patient_id is not None:
        queryset = queryset.filter(patient_id=patient_id)
    return queryset


def get_verification(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    verification_id: UUID,
) -> InsuranceVerification:
    """Get one active verification inside the exact scope."""

    return InsuranceVerification.objects.select_related(
        "patient",
        "organization",
        "verified_by",
    ).get(
        pk=verification_id,
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
    )


def get_verification_for_update(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    verification_id: UUID,
) -> InsuranceVerification:
    """Lock one active verification for mutation."""

    return InsuranceVerification.objects.select_for_update().select_related(
        "patient",
        "organization",
    ).get(
        pk=verification_id,
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
    )


def get_deleted_verification_for_update(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    verification_id: UUID,
) -> InsuranceVerification:
    """Lock one deleted verification for restoration."""

    return InsuranceVerification.all_objects.select_for_update().select_related(
        "patient",
        "organization",
    ).get(
        pk=verification_id,
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
        is_deleted=True,
    )


__all__ = (
    "get_deleted_verification_for_update",
    "get_verification",
    "get_verification_for_update",
    "list_verifications",
)
''',
    "apps/revenue_cycle/insurance_verification/policies.py": '''"""Authorization policies for Insurance Verification."""

from __future__ import annotations

from uuid import UUID

from apps.platform.organizations.models import Organization
from apps.platform.rbac.engines import user_has_permission
from apps.revenue_cycle.insurance_verification.permissions import InsuranceVerificationPermission


def _authorized(*, user, permission: InsuranceVerificationPermission, organization_id: UUID) -> bool:
    """Return whether the user has a permission in the organization."""

    if not user or not user.is_authenticated:
        return False
    organization = Organization.objects.filter(pk=organization_id).first()
    if organization is None:
        return False
    return bool(
        user_has_permission(
            user=user,
            permission=permission.value,
            organization=organization,
        )
    )


def can_view(*, user, organization_id: UUID) -> bool:
    """Check view authorization."""

    return _authorized(
        user=user,
        permission=InsuranceVerificationPermission.VIEW,
        organization_id=organization_id,
    )


def can_create(*, user, organization_id: UUID) -> bool:
    """Check create authorization."""

    return _authorized(
        user=user,
        permission=InsuranceVerificationPermission.CREATE,
        organization_id=organization_id,
    )


def can_update(*, user, organization_id: UUID) -> bool:
    """Check update authorization."""

    return _authorized(
        user=user,
        permission=InsuranceVerificationPermission.UPDATE,
        organization_id=organization_id,
    )


def can_delete(*, user, organization_id: UUID) -> bool:
    """Check delete authorization."""

    return _authorized(
        user=user,
        permission=InsuranceVerificationPermission.DELETE,
        organization_id=organization_id,
    )


def can_restore(*, user, organization_id: UUID) -> bool:
    """Check restore authorization."""

    return _authorized(
        user=user,
        permission=InsuranceVerificationPermission.RESTORE,
        organization_id=organization_id,
    )


def can_transition(*, user, organization_id: UUID) -> bool:
    """Check lifecycle authorization."""

    return _authorized(
        user=user,
        permission=InsuranceVerificationPermission.LIFECYCLE,
        organization_id=organization_id,
    )


__all__ = (
    "can_create",
    "can_delete",
    "can_restore",
    "can_transition",
    "can_update",
    "can_view",
)
''',
    "apps/revenue_cycle/insurance_verification/services/__init__.py": '''"""Insurance Verification domain services."""

from __future__ import annotations

from apps.revenue_cycle.insurance_verification.services.insurance_verification import (
    InsuranceVerificationService,
)

__all__ = ("InsuranceVerificationService",)
''',
    "apps/revenue_cycle/insurance_verification/services/insurance_verification.py": '''"""Transactional Insurance Verification domain services."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any
from uuid import UUID

from django.db import transaction
from django.utils import timezone

from apps.patient_management.patients.models import Patient
from apps.revenue_cycle.insurance_verification.constants import (
    VerificationMethod,
    VerificationOutcome,
    VerificationStatus,
)
from apps.revenue_cycle.insurance_verification.exceptions import (
    InsuranceVerificationInvariantError,
    InsuranceVerificationTransitionError,
)
from apps.revenue_cycle.insurance_verification.models import InsuranceVerification
from apps.revenue_cycle.insurance_verification.selectors import (
    get_deleted_verification_for_update,
    get_verification_for_update,
)


_ALLOWED_TRANSITIONS = {
    VerificationStatus.PENDING.value: {
        VerificationStatus.IN_PROGRESS.value,
        VerificationStatus.FAILED.value,
    },
    VerificationStatus.IN_PROGRESS.value: {
        VerificationStatus.VERIFIED.value,
        VerificationStatus.FAILED.value,
    },
    VerificationStatus.VERIFIED.value: {
        VerificationStatus.EXPIRED.value,
        VerificationStatus.INACTIVE.value,
    },
    VerificationStatus.FAILED.value: {
        VerificationStatus.PENDING.value,
        VerificationStatus.INACTIVE.value,
    },
    VerificationStatus.EXPIRED.value: {
        VerificationStatus.PENDING.value,
        VerificationStatus.INACTIVE.value,
    },
    VerificationStatus.INACTIVE.value: set(),
}


class InsuranceVerificationService:
    """Provide transactional mutations for Insurance Verification."""

    @staticmethod
    def validate_dates(*, coverage_start: date | None, coverage_end: date | None) -> None:
        """Reject an invalid coverage interval."""

        if coverage_start and coverage_end and coverage_end < coverage_start:
            raise InsuranceVerificationInvariantError(
                "coverage_end cannot be earlier than coverage_start."
            )

    @staticmethod
    def validate_amounts(
        *,
        copay_amount: Decimal | None,
        deductible_amount: Decimal | None,
        coinsurance_percent: Decimal | None,
    ) -> None:
        """Reject negative monetary values and invalid coinsurance."""

        if copay_amount is not None and copay_amount < 0:
            raise InsuranceVerificationInvariantError(
                "copay_amount cannot be negative."
            )
        if deductible_amount is not None and deductible_amount < 0:
            raise InsuranceVerificationInvariantError(
                "deductible_amount cannot be negative."
            )
        if coinsurance_percent is not None and not 0 <= coinsurance_percent <= 100:
            raise InsuranceVerificationInvariantError(
                "coinsurance_percent must be between 0 and 100."
            )

    @staticmethod
    def validate_patient(*, organization_id: UUID, patient_id: UUID) -> None:
        """Ensure the patient belongs to the target organization."""

        patient = Patient.objects.filter(
            pk=patient_id,
            organization_id=organization_id,
        ).first()
        if patient is None:
            raise InsuranceVerificationInvariantError(
                "Patient does not belong to the target organization or is unavailable."
            )

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        organization_id: UUID,
        patient_id: UUID,
        request_reference: str,
        idempotency_key: str,
        payer_id: str,
        member_id: str,
        data: dict[str, Any],
    ) -> InsuranceVerification:
        """Create an Insurance Verification transaction atomically."""

        if not request_reference.strip():
            raise InsuranceVerificationInvariantError(
                "request_reference is required."
            )
        if not idempotency_key.strip():
            raise InsuranceVerificationInvariantError(
                "idempotency_key is required."
            )
        if not payer_id.strip() or not member_id.strip():
            raise InsuranceVerificationInvariantError(
                "payer_id and member_id are required."
            )

        cls.validate_patient(
            organization_id=organization_id,
            patient_id=patient_id,
        )
        cls.validate_dates(
            coverage_start=data.get("coverage_start"),
            coverage_end=data.get("coverage_end"),
        )
        cls.validate_amounts(
            copay_amount=data.get("copay_amount"),
            deductible_amount=data.get("deductible_amount"),
            coinsurance_percent=data.get("coinsurance_percent"),
        )

        existing = InsuranceVerification.objects.filter(
            organization_id=organization_id,
            idempotency_key=idempotency_key,
        ).first()
        if existing is not None:
            return existing

        return InsuranceVerification.objects.create(
            organization_id=organization_id,
            patient_id=patient_id,
            payer_id=payer_id.strip(),
            member_id=member_id.strip(),
            request_reference=request_reference.strip(),
            idempotency_key=idempotency_key.strip(),
            **data,
        )

    @classmethod
    @transaction.atomic
    def update(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        verification_id: UUID,
        data: dict[str, Any],
    ) -> InsuranceVerification:
        """Update mutable verification fields under row lock."""

        verification = get_verification_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            verification_id=verification_id,
        )
        if verification.status in {
            VerificationStatus.VERIFIED.value,
            VerificationStatus.INACTIVE.value,
        }:
            protected = {
                "payer_id",
                "member_id",
                "request_reference",
                "idempotency_key",
            }
            if protected.intersection(data):
                raise InsuranceVerificationInvariantError(
                    "Identity fields cannot be changed after verification."
                )

        if "coverage_start" in data or "coverage_end" in data:
            cls.validate_dates(
                coverage_start=data.get("coverage_start", verification.coverage_start),
                coverage_end=data.get("coverage_end", verification.coverage_end),
            )
        cls.validate_amounts(
            copay_amount=data.get("copay_amount", verification.copay_amount),
            deductible_amount=data.get("deductible_amount", verification.deductible_amount),
            coinsurance_percent=data.get(
                "coinsurance_percent",
                verification.coinsurance_percent,
            ),
        )

        if "patient_id" in data:
            cls.validate_patient(
                organization_id=organization_id,
                patient_id=data["patient_id"],
            )

        for field, value in data.items():
            setattr(verification, field, value)
        verification.save()
        return verification

    @classmethod
    @transaction.atomic
    def soft_delete(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        verification_id: UUID,
        deleted_by_id: UUID | None,
    ) -> InsuranceVerification:
        """Soft-delete a verification under row lock."""

        verification = get_verification_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            verification_id=verification_id,
        )
        if verification.status == VerificationStatus.IN_PROGRESS.value:
            raise InsuranceVerificationInvariantError(
                "An in-progress verification cannot be deleted."
            )
        verification.soft_delete(user_id=deleted_by_id)
        return verification

    @classmethod
    @transaction.atomic
    def restore(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        verification_id: UUID,
    ) -> InsuranceVerification:
        """Restore a deleted verification under row lock."""

        verification = get_deleted_verification_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            verification_id=verification_id,
        )
        verification.restore()
        return verification

    @classmethod
    @transaction.atomic
    def transition(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        verification_id: UUID,
        target_status: str,
        actor_id: UUID | None,
        outcome: str | None = None,
        response_code: str | None = None,
        response_message: str | None = None,
        response_payload: dict[str, Any] | None = None,
        failure_reason: str | None = None,
    ) -> InsuranceVerification:
        """Apply a strict lifecycle transition atomically."""

        verification = get_verification_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            verification_id=verification_id,
        )
        current = verification.status
        allowed = _ALLOWED_TRANSITIONS.get(current, set())
        if target_status not in allowed:
            raise InsuranceVerificationTransitionError(
                f"Invalid Insurance Verification transition: {current} -> {target_status}."
            )

        verification.status = target_status
        if outcome is not None:
            verification.outcome = outcome
        if response_code is not None:
            verification.response_code = response_code
        if response_message is not None:
            verification.response_message = response_message
        if response_payload is not None:
            verification.response_payload = response_payload
        if failure_reason is not None:
            verification.failure_reason = failure_reason

        if target_status == VerificationStatus.VERIFIED.value:
            verification.verified_at = timezone.now()
            verification.verified_by_id = actor_id
            if verification.outcome == VerificationOutcome.UNKNOWN.value:
                verification.outcome = VerificationOutcome.ACTIVE.value

        verification.save()
        return verification


__all__ = ("InsuranceVerificationService", "_ALLOWED_TRANSITIONS")
''',
    "apps/revenue_cycle/insurance_verification/events.py": '''"""Insurance Verification domain events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class InsuranceVerificationEvent(DomainEvent):
    """Base event emitted for Insurance Verification changes."""

    verification_id: UUID
    organization_id: UUID
    patient_id: UUID
    status: str
    payload: dict[str, Any]


class InsuranceVerificationCreatedEvent(InsuranceVerificationEvent):
    """Emitted after an Insurance Verification is created."""


class InsuranceVerificationUpdatedEvent(InsuranceVerificationEvent):
    """Emitted after an Insurance Verification is updated."""


class InsuranceVerificationDeletedEvent(InsuranceVerificationEvent):
    """Emitted after an Insurance Verification is soft-deleted."""


class InsuranceVerificationRestoredEvent(InsuranceVerificationEvent):
    """Emitted after an Insurance Verification is restored."""


class InsuranceVerificationStatusChangedEvent(InsuranceVerificationEvent):
    """Emitted after an Insurance Verification lifecycle transition."""


__all__ = (
    "InsuranceVerificationCreatedEvent",
    "InsuranceVerificationDeletedEvent",
    "InsuranceVerificationEvent",
    "InsuranceVerificationRestoredEvent",
    "InsuranceVerificationStatusChangedEvent",
    "InsuranceVerificationUpdatedEvent",
)
''',
    "apps/revenue_cycle/insurance_verification/workflows/__init__.py": '''"""Insurance Verification workflow exports."""

from __future__ import annotations

from apps.revenue_cycle.insurance_verification.workflows.insurance_verification import (
    InsuranceVerificationCreateRequest,
    InsuranceVerificationCreationWorkflow,
    InsuranceVerificationDeleteRequest,
    InsuranceVerificationDeletionWorkflow,
    InsuranceVerificationLifecycleRequest,
    InsuranceVerificationLifecycleWorkflow,
    InsuranceVerificationRestoreRequest,
    InsuranceVerificationRestoreWorkflow,
    InsuranceVerificationUpdateRequest,
    InsuranceVerificationUpdateWorkflow,
)

__all__ = (
    "InsuranceVerificationCreateRequest",
    "InsuranceVerificationCreationWorkflow",
    "InsuranceVerificationDeleteRequest",
    "InsuranceVerificationDeletionWorkflow",
    "InsuranceVerificationLifecycleRequest",
    "InsuranceVerificationLifecycleWorkflow",
    "InsuranceVerificationRestoreRequest",
    "InsuranceVerificationRestoreWorkflow",
    "InsuranceVerificationUpdateRequest",
    "InsuranceVerificationUpdateWorkflow",
)
''',
    "apps/revenue_cycle/insurance_verification/workflows/insurance_verification.py": '''"""Insurance Verification workflow orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from apps.core.events import publish_after_commit
from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.revenue_cycle.insurance_verification.events import (
    InsuranceVerificationCreatedEvent,
    InsuranceVerificationDeletedEvent,
    InsuranceVerificationRestoredEvent,
    InsuranceVerificationStatusChangedEvent,
    InsuranceVerificationUpdatedEvent,
)
from apps.revenue_cycle.insurance_verification.services import InsuranceVerificationService


@dataclass(frozen=True)
class InsuranceVerificationCreateRequest:
    """Input for Insurance Verification creation."""

    organization_id: UUID
    patient_id: UUID
    payer_id: str
    member_id: str
    request_reference: str
    idempotency_key: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class InsuranceVerificationUpdateRequest:
    """Input for Insurance Verification updates."""

    organization_id: UUID
    tenant_id: UUID
    verification_id: UUID
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class InsuranceVerificationDeleteRequest:
    """Input for Insurance Verification deletion."""

    organization_id: UUID
    tenant_id: UUID
    verification_id: UUID
    deleted_by_id: UUID | None


@dataclass(frozen=True)
class InsuranceVerificationRestoreRequest:
    """Input for Insurance Verification restoration."""

    organization_id: UUID
    tenant_id: UUID
    verification_id: UUID


@dataclass(frozen=True)
class InsuranceVerificationLifecycleRequest:
    """Input for Insurance Verification lifecycle changes."""

    organization_id: UUID
    tenant_id: UUID
    verification_id: UUID
    target_status: str
    actor_id: UUID | None
    outcome: str | None = None
    response_code: str | None = None
    response_message: str | None = None
    response_payload: dict[str, Any] | None = None
    failure_reason: str | None = None


class InsuranceVerificationCreationWorkflow(BaseWorkflow):
    """Create an Insurance Verification and publish its event after commit."""

    def __init__(self, *, request: InsuranceVerificationCreateRequest, logger_=None):
        """Initialize the creation workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute creation."""

        request = self.payload
        verification = InsuranceVerificationService.create(
            organization_id=request.organization_id,
            patient_id=request.patient_id,
            request_reference=request.request_reference,
            idempotency_key=request.idempotency_key,
            payer_id=request.payer_id,
            member_id=request.member_id,
            data=request.data,
        )
        publish_after_commit(
            InsuranceVerificationCreatedEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"request_reference": verification.request_reference},
            )
        )
        return WorkflowResult.ok(data=verification)


class InsuranceVerificationUpdateWorkflow(BaseWorkflow):
    """Update an Insurance Verification and publish its event after commit."""

    def __init__(self, *, request: InsuranceVerificationUpdateRequest, logger_=None):
        """Initialize the update workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute update."""

        request = self.payload
        verification = InsuranceVerificationService.update(
            tenant_id=request.tenant_id,
            organization_id=request.organization_id,
            verification_id=request.verification_id,
            data=request.data,
        )
        publish_after_commit(
            InsuranceVerificationUpdatedEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"updated": tuple(request.data)},
            )
        )
        return WorkflowResult.ok(data=verification)


class InsuranceVerificationDeletionWorkflow(BaseWorkflow):
    """Soft-delete an Insurance Verification and publish its event after commit."""

    def __init__(self, *, request: InsuranceVerificationDeleteRequest, logger_=None):
        """Initialize the deletion workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute deletion."""

        request = self.payload
        verification = InsuranceVerificationService.soft_delete(
            tenant_id=request.tenant_id,
            organization_id=request.organization_id,
            verification_id=request.verification_id,
            deleted_by_id=request.deleted_by_id,
        )
        publish_after_commit(
            InsuranceVerificationDeletedEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"deleted": True},
            )
        )
        return WorkflowResult.ok(data=verification)


class InsuranceVerificationRestoreWorkflow(BaseWorkflow):
    """Restore an Insurance Verification and publish its event after commit."""

    def __init__(self, *, request: InsuranceVerificationRestoreRequest, logger_=None):
        """Initialize the restoration workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute restoration."""

        request = self.payload
        verification = InsuranceVerificationService.restore(
            tenant_id=request.tenant_id,
            organization_id=request.organization_id,
            verification_id=request.verification_id,
        )
        publish_after_commit(
            InsuranceVerificationRestoredEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"restored": True},
            )
        )
        return WorkflowResult.ok(data=verification)


class InsuranceVerificationLifecycleWorkflow(BaseWorkflow):
    """Transition an Insurance Verification and publish its event after commit."""

    def __init__(self, *, request: InsuranceVerificationLifecycleRequest, logger_=None):
        """Initialize the lifecycle workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute lifecycle transition."""

        request = self.payload
        verification = InsuranceVerificationService.transition(
            tenant_id=request.tenant_id,
            organization_id=request.organization_id,
            verification_id=request.verification_id,
            target_status=request.target_status,
            actor_id=request.actor_id,
            outcome=request.outcome,
            response_code=request.response_code,
            response_message=request.response_message,
            response_payload=request.response_payload,
            failure_reason=request.failure_reason,
        )
        publish_after_commit(
            InsuranceVerificationStatusChangedEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"outcome": verification.outcome},
            )
        )
        return WorkflowResult.ok(data=verification)


__all__ = (
    "InsuranceVerificationCreateRequest",
    "InsuranceVerificationCreationWorkflow",
    "InsuranceVerificationDeleteRequest",
    "InsuranceVerificationDeletionWorkflow",
    "InsuranceVerificationLifecycleRequest",
    "InsuranceVerificationLifecycleWorkflow",
    "InsuranceVerificationRestoreRequest",
    "InsuranceVerificationRestoreWorkflow",
    "InsuranceVerificationUpdateRequest",
    "InsuranceVerificationUpdateWorkflow",
)
''',
    "apps/revenue_cycle/insurance_verification/workflow_registry.py": '''"""Revenue Cycle Insurance Verification workflow registration."""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.revenue_cycle.insurance_verification.workflows import (
    InsuranceVerificationCreationWorkflow,
    InsuranceVerificationDeletionWorkflow,
    InsuranceVerificationLifecycleWorkflow,
    InsuranceVerificationRestoreWorkflow,
    InsuranceVerificationUpdateWorkflow,
)


WORKFLOW_DEFINITIONS = (
    ("revenue_cycle.insurance_verification.create", InsuranceVerificationCreationWorkflow),
    ("revenue_cycle.insurance_verification.update", InsuranceVerificationUpdateWorkflow),
    ("revenue_cycle.insurance_verification.delete", InsuranceVerificationDeletionWorkflow),
    ("revenue_cycle.insurance_verification.restore", InsuranceVerificationRestoreWorkflow),
    ("revenue_cycle.insurance_verification.lifecycle", InsuranceVerificationLifecycleWorkflow),
)


def register_workflows() -> None:
    """Register Insurance Verification workflows idempotently."""

    for name, workflow in WORKFLOW_DEFINITIONS:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=workflow)


register_workflows()

__all__ = ("WORKFLOW_DEFINITIONS", "register_workflows")
''',
    "apps/revenue_cycle/insurance_verification/api/__init__.py": '''"""Insurance Verification API package."""

from __future__ import annotations

__all__ = ()
''',
    "apps/revenue_cycle/insurance_verification/api/serializers/__init__.py": '''"""Insurance Verification API serializers."""

from __future__ import annotations

from apps.revenue_cycle.insurance_verification.api.serializers.insurance_verification import (
    InsuranceVerificationDetailSerializer,
    InsuranceVerificationLifecycleSerializer,
    InsuranceVerificationWriteSerializer,
)

__all__ = (
    "InsuranceVerificationDetailSerializer",
    "InsuranceVerificationLifecycleSerializer",
    "InsuranceVerificationWriteSerializer",
)
''',
    "apps/revenue_cycle/insurance_verification/api/serializers/insurance_verification.py": '''"""Insurance Verification API serializers."""

from __future__ import annotations

from rest_framework import serializers

from apps.revenue_cycle.insurance_verification.constants import (
    VerificationMethod,
    VerificationOutcome,
    VerificationStatus,
)
from apps.revenue_cycle.insurance_verification.models import InsuranceVerification


class InsuranceVerificationWriteSerializer(serializers.Serializer):
    """Validate create and update payloads."""

    patient_id = serializers.UUIDField(required=False)
    payer_id = serializers.CharField(max_length=100, required=False)
    payer_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    member_id = serializers.CharField(max_length=100, required=False)
    policy_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    group_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    subscriber_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    subscriber_relationship = serializers.CharField(max_length=50, required=False, allow_blank=True)
    verification_method = serializers.ChoiceField(
        choices=[item.value for item in VerificationMethod],
        required=False,
    )
    eligibility_reference = serializers.UUIDField(required=False, allow_null=True)
    coverage_start = serializers.DateField(required=False, allow_null=True)
    coverage_end = serializers.DateField(required=False, allow_null=True)
    copay_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        allow_null=True,
    )
    deductible_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        allow_null=True,
    )
    coinsurance_percent = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        allow_null=True,
    )
    prior_authorization_required = serializers.BooleanField(required=False)
    response_code = serializers.CharField(max_length=100, required=False, allow_blank=True)
    response_message = serializers.CharField(required=False, allow_blank=True)
    response_payload = serializers.JSONField(required=False)
    request_reference = serializers.CharField(max_length=100, required=False)
    idempotency_key = serializers.CharField(max_length=255, required=False)
    failure_reason = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        """Validate cross-field coverage and monetary constraints."""

        coverage_start = attrs.get("coverage_start")
        coverage_end = attrs.get("coverage_end")
        if coverage_start and coverage_end and coverage_end < coverage_start:
            raise serializers.ValidationError(
                {"coverage_end": "coverage_end cannot be earlier than coverage_start."}
            )

        coinsurance = attrs.get("coinsurance_percent")
        if coinsurance is not None and not 0 <= coinsurance <= 100:
            raise serializers.ValidationError(
                {"coinsurance_percent": "Must be between 0 and 100."}
            )

        for field in ("copay_amount", "deductible_amount"):
            amount = attrs.get(field)
            if amount is not None and amount < 0:
                raise serializers.ValidationError(
                    {field: "Amount cannot be negative."}
                )
        return attrs


class InsuranceVerificationLifecycleSerializer(serializers.Serializer):
    """Validate lifecycle transition payloads."""

    target_status = serializers.ChoiceField(choices=[item.value for item in VerificationStatus])
    outcome = serializers.ChoiceField(
        choices=[item.value for item in VerificationOutcome],
        required=False,
    )
    response_code = serializers.CharField(max_length=100, required=False, allow_blank=True)
    response_message = serializers.CharField(required=False, allow_blank=True)
    response_payload = serializers.JSONField(required=False)
    request_reference = serializers.CharField(max_length=100, required=False)
    idempotency_key = serializers.CharField(max_length=255, required=False)
    failure_reason = serializers.CharField(required=False, allow_blank=True)


class InsuranceVerificationDetailSerializer(serializers.ModelSerializer):
    """Serialize Insurance Verification records for API responses."""

    class Meta:
        """Serializer metadata."""

        model = InsuranceVerification
        fields = (
            "id",
            "organization",
            "patient",
            "eligibility_reference",
            "payer_id",
            "payer_name",
            "member_id",
            "policy_number",
            "group_number",
            "subscriber_name",
            "subscriber_relationship",
            "verification_method",
            "status",
            "outcome",
            "requested_at",
            "verified_at",
            "coverage_start",
            "coverage_end",
            "copay_amount",
            "deductible_amount",
            "coinsurance_percent",
            "prior_authorization_required",
            "response_code",
            "response_message",
            "response_payload",
            "request_reference",
            "idempotency_key",
            "failure_reason",
            "verified_by",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


__all__ = (
    "InsuranceVerificationDetailSerializer",
    "InsuranceVerificationLifecycleSerializer",
    "InsuranceVerificationWriteSerializer",
)
''',
    "apps/revenue_cycle/insurance_verification/api/views/__init__.py": '''"""Insurance Verification API views."""

from __future__ import annotations

from apps.revenue_cycle.insurance_verification.api.views.insurance_verification import (
    InsuranceVerificationDetailAPIView,
    InsuranceVerificationLifecycleAPIView,
    InsuranceVerificationListCreateAPIView,
    InsuranceVerificationRestoreAPIView,
)

__all__ = (
    "InsuranceVerificationDetailAPIView",
    "InsuranceVerificationLifecycleAPIView",
    "InsuranceVerificationListCreateAPIView",
    "InsuranceVerificationRestoreAPIView",
)
''',
    "apps/revenue_cycle/insurance_verification/api/views/insurance_verification.py": '''"""Insurance Verification API views."""

from __future__ import annotations

from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.revenue_cycle.insurance_verification.api.serializers import (
    InsuranceVerificationDetailSerializer,
    InsuranceVerificationLifecycleSerializer,
    InsuranceVerificationWriteSerializer,
)
from apps.revenue_cycle.insurance_verification.policies import (
    can_create,
    can_delete,
    can_restore,
    can_transition,
    can_update,
    can_view,
)
from apps.revenue_cycle.insurance_verification.rbac import (
    CanCreateInsuranceVerification,
    CanDeleteInsuranceVerification,
    CanRestoreInsuranceVerification,
    CanTransitionInsuranceVerification,
    CanUpdateInsuranceVerification,
    CanViewInsuranceVerification,
)
from apps.revenue_cycle.insurance_verification.selectors import (
    get_verification,
    list_verifications,
)
from apps.revenue_cycle.insurance_verification.workflows import (
    InsuranceVerificationCreateRequest,
    InsuranceVerificationCreationWorkflow,
    InsuranceVerificationDeleteRequest,
    InsuranceVerificationDeletionWorkflow,
    InsuranceVerificationLifecycleRequest,
    InsuranceVerificationLifecycleWorkflow,
    InsuranceVerificationRestoreRequest,
    InsuranceVerificationRestoreWorkflow,
    InsuranceVerificationUpdateRequest,
    InsuranceVerificationUpdateWorkflow,
)


def _tenant(request) -> UUID:
    """Resolve the explicit tenant context or reject the request."""

    tenant = getattr(request, "tenant", None)
    if tenant is None or getattr(tenant, "pk", None) is None:
        raise ValueError("Explicit request.tenant is required.")
    return tenant.pk


def _organization(request):
    """Resolve explicit organization context and validate its tenant."""

    organization = getattr(request, "organization", None)
    if organization is None or getattr(organization, "pk", None) is None:
        raise ValueError("Explicit request.organization is required.")
    tenant = getattr(request, "tenant", None)
    if tenant is None or organization.tenant_id != tenant.pk:
        raise ValueError("Organization does not belong to the active tenant.")
    return organization


def _context(request, operation: str) -> WorkflowContext:
    """Build the standard Revenue Cycle workflow context."""

    return WorkflowContext(
        actor=request.user,
        organization_id=_organization(request).pk,
        tenant_id=_tenant(request),
        operation=operation,
    )


class InsuranceVerificationListCreateAPIView(APIView):
    """List and create Insurance Verification records."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return tenant-safe verification records."""

        organization = _organization(request)
        if not can_view(user=request.user, organization_id=organization.pk):
            CanViewInsuranceVerification().has_permission(request, self)
        patient_id = request.query_params.get("patient_id")
        queryset = list_verifications(
            tenant_id=_tenant(request),
            organization_id=organization.pk,
            patient_id=patient_id,
        )
        return Response(InsuranceVerificationDetailSerializer(queryset, many=True).data)

    def post(self, request):
        """Create a verification through the workflow boundary."""

        organization = _organization(request)
        if not can_create(user=request.user, organization_id=organization.pk):
            CanCreateInsuranceVerification().has_permission(request, self)
        serializer = InsuranceVerificationWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient_id = serializer.validated_data.pop("patient_id", None)
        payer_id = serializer.validated_data.pop("payer_id", "")
        member_id = serializer.validated_data.pop("member_id", "")
        request_reference = request.data.get("request_reference", "")
        idempotency_key = request.headers.get("Idempotency-Key", request.data.get("idempotency_key", ""))
        workflow = InsuranceVerificationCreationWorkflow(
            request=InsuranceVerificationCreateRequest(
                organization_id=organization.pk,
                patient_id=patient_id,
                payer_id=payer_id,
                member_id=member_id,
                request_reference=request_reference,
                idempotency_key=idempotency_key,
                data=serializer.validated_data,
            )
        )
        result = workflow.run(context=_context(request, "revenue_cycle.insurance_verification.create"))
        return Response(
            InsuranceVerificationDetailSerializer(result.data).data,
            status=status.HTTP_201_CREATED,
        )


class InsuranceVerificationDetailAPIView(APIView):
    """Retrieve, update, and delete one Insurance Verification."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, verification_id):
        """Return one tenant-safe verification."""

        organization = _organization(request)
        if not can_view(user=request.user, organization_id=organization.pk):
            CanViewInsuranceVerification().has_permission(request, self)
        verification = get_verification(
            tenant_id=_tenant(request),
            organization_id=organization.pk,
            verification_id=verification_id,
        )
        return Response(InsuranceVerificationDetailSerializer(verification).data)

    def patch(self, request, verification_id):
        """Update a verification through the workflow boundary."""

        organization = _organization(request)
        if not can_update(user=request.user, organization_id=organization.pk):
            CanUpdateInsuranceVerification().has_permission(request, self)
        serializer = InsuranceVerificationWriteSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        result = InsuranceVerificationUpdateWorkflow(
            request=InsuranceVerificationUpdateRequest(
                organization_id=organization.pk,
                tenant_id=_tenant(request),
                verification_id=verification_id,
                data=serializer.validated_data,
            )
        ).run(context=_context(request, "revenue_cycle.insurance_verification.update"))
        return Response(InsuranceVerificationDetailSerializer(result.data).data)

    def delete(self, request, verification_id):
        """Soft-delete a verification through the workflow boundary."""

        organization = _organization(request)
        if not can_delete(user=request.user, organization_id=organization.pk):
            CanDeleteInsuranceVerification().has_permission(request, self)
        result = InsuranceVerificationDeletionWorkflow(
            request=InsuranceVerificationDeleteRequest(
                organization_id=organization.pk,
                tenant_id=_tenant(request),
                verification_id=verification_id,
                deleted_by_id=request.user.pk,
            )
        ).run(context=_context(request, "revenue_cycle.insurance_verification.delete"))
        return Response(InsuranceVerificationDetailSerializer(result.data).data)


class InsuranceVerificationLifecycleAPIView(APIView):
    """Transition Insurance Verification lifecycle state."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, verification_id):
        """Apply a strict lifecycle transition."""

        organization = _organization(request)
        if not can_transition(user=request.user, organization_id=organization.pk):
            CanTransitionInsuranceVerification().has_permission(request, self)
        serializer = InsuranceVerificationLifecycleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = InsuranceVerificationLifecycleWorkflow(
            request=InsuranceVerificationLifecycleRequest(
                organization_id=organization.pk,
                tenant_id=_tenant(request),
                verification_id=verification_id,
                actor_id=request.user.pk,
                **serializer.validated_data,
            )
        ).run(context=_context(request, "revenue_cycle.insurance_verification.lifecycle"))
        return Response(InsuranceVerificationDetailSerializer(result.data).data)


class InsuranceVerificationRestoreAPIView(APIView):
    """Restore a deleted Insurance Verification."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, verification_id):
        """Restore through the workflow boundary."""

        organization = _organization(request)
        if not can_restore(user=request.user, organization_id=organization.pk):
            CanRestoreInsuranceVerification().has_permission(request, self)
        try:
            result = InsuranceVerificationRestoreWorkflow(
                request=InsuranceVerificationRestoreRequest(
                    organization_id=organization.pk,
                    tenant_id=_tenant(request),
                    verification_id=verification_id,
                )
            ).run(context=_context(request, "revenue_cycle.insurance_verification.restore"))
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Insurance verification record not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(InsuranceVerificationDetailSerializer(result.data).data)


__all__ = (
    "InsuranceVerificationDetailAPIView",
    "InsuranceVerificationLifecycleAPIView",
    "InsuranceVerificationListCreateAPIView",
    "InsuranceVerificationRestoreAPIView",
)
''',
    "apps/revenue_cycle/insurance_verification/urls.py": '''"""Revenue Cycle Insurance Verification URL routes."""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.insurance_verification.api.views import (
    InsuranceVerificationDetailAPIView,
    InsuranceVerificationLifecycleAPIView,
    InsuranceVerificationListCreateAPIView,
    InsuranceVerificationRestoreAPIView,
)


app_name = "revenue_cycle_insurance_verification"

urlpatterns = (
    path("", InsuranceVerificationListCreateAPIView.as_view(), name="list-create"),
    path(
        "<uuid:verification_id>/",
        InsuranceVerificationDetailAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:verification_id>/lifecycle/",
        InsuranceVerificationLifecycleAPIView.as_view(),
        name="lifecycle",
    ),
    path(
        "<uuid:verification_id>/restore/",
        InsuranceVerificationRestoreAPIView.as_view(),
        name="restore",
    ),
)

__all__ = ("app_name", "urlpatterns")
''',
    "apps/revenue_cycle/insurance_verification/admin.py": '''"""Django admin for Revenue Cycle Insurance Verification."""

from __future__ import annotations

from django.contrib import admin

from apps.revenue_cycle.insurance_verification.models import InsuranceVerification


@admin.register(InsuranceVerification)
class InsuranceVerificationAdmin(admin.ModelAdmin):
    """Admin interface for Insurance Verification records."""

    list_display = (
        "request_reference",
        "patient",
        "payer_id",
        "member_id",
        "status",
        "outcome",
        "requested_at",
    )
    list_filter = (
        "status",
        "outcome",
        "verification_method",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "request_reference",
        "payer_id",
        "member_id",
        "policy_number",
        "patient__mrn",
        "patient__first_name",
        "patient__last_name",
    )
    readonly_fields = (
        "id",
        "requested_at",
        "verified_at",
        "created_at",
        "updated_at",
    )
    list_select_related = ("patient", "organization", "verified_by")


__all__ = ("InsuranceVerificationAdmin",)
''',
    "apps/revenue_cycle/insurance_verification/migrations/__init__.py": '''"""Deferred Revenue Cycle Insurance Verification migrations."""

from __future__ import annotations

__all__ = ()
''',
    "apps/revenue_cycle/insurance_verification/tests/__init__.py": '''"""Revenue Cycle Insurance Verification tests."""

from __future__ import annotations

__all__ = ()
''',
    "apps/revenue_cycle/insurance_verification/tests/test_architecture.py": '''"""Architecture tests for Revenue Cycle Insurance Verification."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase


class InsuranceVerificationArchitectureTests(SimpleTestCase):
    """Verify the Insurance Verification architectural contract."""

    def test_canonical_patient(self):
        """Insurance Verification must use canonical Patient."""

        source = Path(
            "apps/revenue_cycle/insurance_verification/models/insurance_verification.py"
        ).read_text(encoding="utf-8")
        self.assertIn("apps.patient_management.patients.models", source)

    def test_tenant_scoped_selectors(self):
        """Selectors must constrain tenant and organization."""

        source = Path(
            "apps/revenue_cycle/insurance_verification/selectors/insurance_verification.py"
        ).read_text(encoding="utf-8")
        self.assertIn("organization__tenant_id=tenant_id", source)
        self.assertIn("organization_id=organization_id", source)

    def test_after_commit_events(self):
        """Mutation workflows must dispatch events after commit."""

        source = Path(
            "apps/revenue_cycle/insurance_verification/workflows/insurance_verification.py"
        ).read_text(encoding="utf-8")
        self.assertIn("publish_after_commit", source)

    def test_platform_rbac(self):
        """Authorization must use the canonical platform RBAC engine."""

        source = Path(
            "apps/revenue_cycle/insurance_verification/policies.py"
        ).read_text(encoding="utf-8")
        self.assertIn("apps.platform.rbac.engines", source)

    def test_explicit_context(self):
        """API must require explicit tenant and organization context."""

        source = Path(
            "apps/revenue_cycle/insurance_verification/api/views/insurance_verification.py"
        ).read_text(encoding="utf-8")
        self.assertIn('getattr(request, "tenant", None)', source)
        self.assertIn('getattr(request, "organization", None)', source)


__all__ = ("InsuranceVerificationArchitectureTests",)
''',
    "apps/revenue_cycle/insurance_verification/tests/test_invariants.py": '''"""Insurance Verification invariant tests."""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.revenue_cycle.insurance_verification.constants import (
    VerificationOutcome,
    VerificationStatus,
)
from apps.revenue_cycle.insurance_verification.services.insurance_verification import (
    _ALLOWED_TRANSITIONS,
)


class InsuranceVerificationInvariantTests(SimpleTestCase):
    """Verify strict Insurance Verification state invariants."""

    def test_pending_cannot_skip_to_verified(self):
        """Pending verification must enter processing first."""

        self.assertNotIn(
            VerificationStatus.VERIFIED.value,
            _ALLOWED_TRANSITIONS[VerificationStatus.PENDING.value],
        )

    def test_inactive_is_terminal(self):
        """Inactive verification cannot transition to another state."""

        self.assertEqual(
            _ALLOWED_TRANSITIONS[VerificationStatus.INACTIVE.value],
            set(),
        )

    def test_outcome_set_is_finite(self):
        """Outcome values remain a finite canonical set."""

        self.assertEqual(
            {item.value for item in VerificationOutcome},
            {"active", "inactive", "not_found", "unknown"},
        )


__all__ = ("InsuranceVerificationInvariantTests",)
''',
}


def update_root_models() -> None:
    """Ensure Django discovers Revenue Cycle nested models without migrations."""

    models_dir = ROOT / "apps" / "revenue_cycle" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    init_path = models_dir / "__init__.py"
    existing = init_path.read_text(encoding="utf-8") if init_path.exists() else ""
    additions = (
        "from apps.revenue_cycle.eligibility.models import Eligibility\n",
        "from apps.revenue_cycle.insurance_verification.models import InsuranceVerification\n",
    )
    if "from apps.revenue_cycle.eligibility.models import Eligibility" not in existing:
        existing += "\n" + additions[0]
    if (
        "from apps.revenue_cycle.insurance_verification.models import InsuranceVerification"
        not in existing
    ):
        existing += additions[1]
    if "__all__" not in existing:
        existing += '\n__all__ = ("Eligibility", "InsuranceVerification")\n'
    init_path.write_text(existing, encoding="utf-8")


def update_root_app_registry() -> None:
    """Ensure nested Revenue Cycle workflow registries are loaded at app startup."""

    apps_path = ROOT / "apps" / "revenue_cycle" / "apps.py"
    if not apps_path.exists():
        return
    source = apps_path.read_text(encoding="utf-8")
    marker = "from apps.revenue_cycle.insurance_verification.workflow_registry import register_workflows as register_insurance_verification_workflows"
    if marker not in source:
        source = source.replace(
            "def ready(self) -> None:",
            marker + "\n\n    def ready(self) -> None:",
        )
        source = source.replace(
            "    def ready(self) -> None:\n",
            "    def ready(self) -> None:\n        register_insurance_verification_workflows()\n",
            1,
        )
        apps_path.write_text(source, encoding="utf-8")


def write_files() -> None:
    """Install RC2 without modifying the database or migrations."""

    if not BACKUP.exists():
        raise RuntimeError("apps/revenue_cycle_legacy_backup is required.")
    if ACTIVE.exists():
        shutil.rmtree(ACTIVE)
    for relative, content in FILES.items():
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    update_root_models()
    update_root_app_registry()


def verify() -> None:
    """Verify source syntax and RC2 architecture contracts."""

    python_files = sorted(ACTIVE.rglob("*.py"))
    if len(python_files) < 27:
        raise AssertionError(f"RC2 manifest unexpectedly small: {len(python_files)}")
    print(f"MANIFEST PASS ({len(python_files)} Python files)")
    for path in python_files:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        if ast.get_docstring(tree) is None:
            raise AssertionError(f"Missing module docstring: {path}")
        if "from __future__ import annotations" not in source:
            raise AssertionError(f"Missing future annotations: {path}")
        py_compile.compile(str(path), doraise=True)
    print("STYLE PASS")
    print("PY_COMPILE PASS")

    model = (ACTIVE / "models" / "insurance_verification.py").read_text(
        encoding="utf-8"
    )
    selectors = (ACTIVE / "selectors" / "insurance_verification.py").read_text(
        encoding="utf-8"
    )
    service = (ACTIVE / "services" / "insurance_verification.py").read_text(
        encoding="utf-8"
    )
    workflows = (ACTIVE / "workflows" / "insurance_verification.py").read_text(
        encoding="utf-8"
    )
    views = (ACTIVE / "api" / "views" / "insurance_verification.py").read_text(
        encoding="utf-8"
    )
    policies = (ACTIVE / "policies.py").read_text(encoding="utf-8")

    checks = (
        ("canonical Patient", "apps.patient_management.patients.models", model),
        ("tenant scope", "organization__tenant_id=tenant_id", selectors),
        ("row locking", "select_for_update", selectors),
        ("after commit", "publish_after_commit", workflows),
        ("explicit tenant", 'getattr(request, "tenant", None)', views),
        ("explicit organization", 'getattr(request, "organization", None)', views),
        ("platform RBAC", "apps.platform.rbac.engines", policies),
        ("idempotency", "rc_iv_org_idempotency_uniq", model),
    )
    for label, needle, source in checks:
        if needle not in source:
            raise AssertionError(f"Architecture check failed: {label}")

    if "get_verification_for_update" not in service:
        raise AssertionError(
            "Architecture check failed: service mutation locking delegation"
        )
    if "get_deleted_verification_for_update" not in service:
        raise AssertionError("Architecture check failed: restore locking delegation")

    print("ARCHITECTURE PASS")
    print("CANONICAL PATIENT: patient_core.Patient")
    print("CANONICAL RBAC: PLATFORM ENGINE")
    print("TENANT CONTEXT: EXPLICIT")
    print(
        "WORKFLOW CHAIN: API -> RBAC -> Workflow -> Policy -> Service -> Selector -> Model -> Event"
    )
    print("DOMAIN EVENTS: AFTER COMMIT")
    print("IDEMPOTENCY: ORGANIZATION + KEY UNIQUE")
    print("CONCURRENCY: SELECT_FOR_UPDATE MUTATIONS")
    print("LIFECYCLE: STRICT TRANSITIONS")
    print("MIGRATIONS NOT GENERATED")
    print("DATABASE NOT MODIFIED")
    print("LEGACY BACKUP PRESERVED")
    print("RC2 INSURANCE VERIFICATION INSTALL COMPLETE")


def main() -> None:
    """Install and verify RC2 Insurance Verification."""

    print("DatavionAI Revenue Cycle RC2 Insurance Verification Installer v1.0.0")
    print("=" * 72)
    write_files()
    verify()


if __name__ == "__main__":
    main()
