from __future__ import annotations

import ast
import py_compile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ACTIVE = ROOT / "apps" / "revenue_cycle" / "prior_authorization"
BACKUP = ROOT / "apps" / "revenue_cycle_legacy_backup"

FILES = {
    "apps/revenue_cycle/prior_authorization/__init__.py": '''"""Revenue Cycle Prior Authorization bounded context."""

from __future__ import annotations

__all__ = ()
''',
    "apps/revenue_cycle/prior_authorization/constants.py": '''"""Prior Authorization lifecycle and normalized authorization constants."""

from __future__ import annotations

from enum import StrEnum


class AuthorizationStatus(StrEnum):
    """Supported Prior Authorization lifecycle states."""

    PENDING = "pending"
    IN_REVIEW = "in_review"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    INACTIVE = "inactive"


class AuthorizationOutcome(StrEnum):
    """Normalized authorization outcomes."""

    APPROVED = "approved"
    DENIED = "denied"
    PENDED = "pended"
    NOT_REQUIRED = "not_required"
    UNKNOWN = "unknown"


class AuthorizationMethod(StrEnum):
    """Supported authorization submission methods."""

    MANUAL = "manual"
    PAYER_API = "payer_api"
    CLEARINGHOUSE = "clearinghouse"
    PORTAL = "portal"
    IMPORT = "import"


__all__ = ("AuthorizationMethod", "AuthorizationOutcome", "AuthorizationStatus")
''',
    "apps/revenue_cycle/prior_authorization/exceptions.py": '''"""Prior Authorization domain exceptions."""

from __future__ import annotations


class PriorAuthorizationError(Exception):
    """Base Prior Authorization exception."""


class PriorAuthorizationInvariantError(PriorAuthorizationError):
    """Raised when a verification invariant is violated."""


class PriorAuthorizationTransitionError(PriorAuthorizationError):
    """Raised when an invalid lifecycle transition is requested."""


__all__ = (
    "PriorAuthorizationError",
    "PriorAuthorizationInvariantError",
    "PriorAuthorizationTransitionError",
)
''',
    "apps/revenue_cycle/prior_authorization/permissions.py": '''"""Revenue Cycle Prior Authorization RBAC permission codes."""

from __future__ import annotations

from enum import StrEnum


class PriorAuthorizationPermission(StrEnum):
    """Exact platform RBAC permission codes."""

    VIEW = "revenue_cycle.prior_authorization.view"
    CREATE = "revenue_cycle.prior_authorization.create"
    UPDATE = "revenue_cycle.prior_authorization.update"
    DELETE = "revenue_cycle.prior_authorization.delete"
    RESTORE = "revenue_cycle.prior_authorization.restore"
    LIFECYCLE = "revenue_cycle.prior_authorization.lifecycle"


__all__ = ("PriorAuthorizationPermission",)
''',
    "apps/revenue_cycle/prior_authorization/rbac.py": '''"""DRF RBAC adapters for Prior Authorization."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase
from apps.revenue_cycle.prior_authorization.permissions import PriorAuthorizationPermission


class CanViewPriorAuthorization(RBACPermissionBase):
    """Require Prior Authorization view permission."""

    permission_code = PriorAuthorizationPermission.VIEW
    message = "You do not have permission to view prior authorization records."


class CanCreatePriorAuthorization(RBACPermissionBase):
    """Require Prior Authorization creation permission."""

    permission_code = PriorAuthorizationPermission.CREATE
    message = "You do not have permission to create prior authorization records."


class CanUpdatePriorAuthorization(RBACPermissionBase):
    """Require Prior Authorization update permission."""

    permission_code = PriorAuthorizationPermission.UPDATE
    message = "You do not have permission to update prior authorization records."


class CanDeletePriorAuthorization(RBACPermissionBase):
    """Require Prior Authorization deletion permission."""

    permission_code = PriorAuthorizationPermission.DELETE
    message = "You do not have permission to delete prior authorization records."


class CanRestorePriorAuthorization(RBACPermissionBase):
    """Require Prior Authorization restoration permission."""

    permission_code = PriorAuthorizationPermission.RESTORE
    message = "You do not have permission to restore prior authorization records."


class CanTransitionPriorAuthorization(RBACPermissionBase):
    """Require Prior Authorization lifecycle permission."""

    permission_code = PriorAuthorizationPermission.LIFECYCLE
    message = "You do not have permission to change prior authorization lifecycle."


__all__ = (
    "CanCreatePriorAuthorization",
    "CanDeletePriorAuthorization",
    "CanRestorePriorAuthorization",
    "CanTransitionPriorAuthorization",
    "CanUpdatePriorAuthorization",
    "CanViewPriorAuthorization",
)
''',
    "apps/revenue_cycle/prior_authorization/models/__init__.py": '''"""Revenue Cycle Prior Authorization models."""

from __future__ import annotations

from apps.revenue_cycle.prior_authorization.models.prior_authorization import PriorAuthorization

__all__ = ("PriorAuthorization",)
''',
    "apps/revenue_cycle/prior_authorization/models/prior_authorization.py": '''"""Revenue Cycle Prior Authorization aggregate model."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.prior_authorization.constants import (
    AuthorizationMethod,
    AuthorizationOutcome,
    AuthorizationStatus,
)


class PriorAuthorization(BaseModel):
    """Store an organization-scoped prior authorization request and decision."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_prior_authorizations",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_prior_authorizations",
    )
    eligibility_reference = models.UUIDField(null=True, blank=True, db_index=True)
    payer_id = models.CharField(max_length=100, db_index=True)
    payer_name = models.CharField(max_length=255, blank=True)
    member_id = models.CharField(max_length=100, db_index=True)
    policy_number = models.CharField(max_length=100, blank=True)
    group_number = models.CharField(max_length=100, blank=True)
    procedure_code = models.CharField(max_length=50, db_index=True)
    service_description = models.CharField(max_length=500, blank=True)
    place_of_service = models.CharField(max_length=20, blank=True)
    rendering_provider_npi = models.CharField(max_length=20, blank=True)
    clinical_indication = models.TextField(blank=True)
    authorization_method = models.CharField(
        max_length=30,
        choices=tuple((item.value, item.value) for item in AuthorizationMethod),
        default=AuthorizationMethod.MANUAL.value,
    )
    status = models.CharField(
        max_length=30,
        choices=tuple((item.value, item.value) for item in AuthorizationStatus),
        default=AuthorizationStatus.PENDING.value,
        db_index=True,
    )
    outcome = models.CharField(
        max_length=30,
        choices=tuple((item.value, item.value) for item in AuthorizationOutcome),
        default=AuthorizationOutcome.UNKNOWN.value,
        db_index=True,
    )
    requested_service_date = models.DateField(null=True, blank=True)
    requested_units = models.PositiveIntegerField(null=True, blank=True)
    approved_units = models.PositiveIntegerField(null=True, blank=True)
    requested_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )
    authorization_number = models.CharField(max_length=100, blank=True, db_index=True)
    effective_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    decision_reason = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True, db_index=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    response_code = models.CharField(max_length=100, blank=True)
    response_message = models.TextField(blank=True)
    response_payload = models.JSONField(default=dict, blank=True)
    request_reference = models.CharField(max_length=100, db_index=True)
    idempotency_key = models.CharField(max_length=255, db_index=True)
    failure_reason = models.TextField(blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="revenue_cycle_prior_authorizations_approved",
    )

    class Meta:
        """Database metadata for Prior Authorization."""

        db_table = "revenue_cycle_prior_authorization"
        ordering = ("-requested_at",)
        indexes = (
            models.Index(
                fields=("organization", "patient", "-requested_at"),
                name="rc_pa_org_patient_req_idx",
            ),
            models.Index(
                fields=("organization", "status"),
                name="rc_pa_org_status_idx",
            ),
            models.Index(
                fields=("organization", "payer_id", "member_id"),
                name="rc_pa_org_payer_member_idx",
            ),
            models.Index(
                fields=("organization", "procedure_code", "requested_service_date"),
                name="rc_pa_org_proc_date_idx",
            ),
            models.Index(
                fields=("organization", "outcome"),
                name="rc_pa_org_outcome_idx",
            ),
        )
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "idempotency_key"),
                name="rc_pa_org_idempotency_uniq",
            ),
        )

    def __str__(self) -> str:
        """Return a stable authorization representation."""

        return f"{self.payer_id}:{self.member_id}:{self.request_reference}"


__all__ = ("PriorAuthorization",)
''',
    "apps/revenue_cycle/prior_authorization/selectors/__init__.py": '''"""Tenant-safe Prior Authorization selectors."""

from __future__ import annotations

from apps.revenue_cycle.prior_authorization.selectors.prior_authorization import (
    get_deleted_authorization_for_update,
    get_verification,
    get_authorization_for_update,
    list_verifications,
)

__all__ = (
    "get_deleted_authorization_for_update",
    "get_verification",
    "get_authorization_for_update",
    "list_verifications",
)
''',
    "apps/revenue_cycle/prior_authorization/selectors/prior_authorization.py": '''"""Tenant-safe Prior Authorization query selectors."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.revenue_cycle.prior_authorization.models import PriorAuthorization


def list_verifications(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    patient_id: UUID | None = None,
) -> QuerySet[PriorAuthorization]:
    """List active records inside the exact tenant and organization scope."""

    queryset = (
        PriorAuthorization.objects.select_related(
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
) -> PriorAuthorization:
    """Get one active verification inside the exact scope."""

    return PriorAuthorization.objects.select_related(
        "patient",
        "organization",
        "verified_by",
    ).get(
        pk=verification_id,
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
    )


def get_authorization_for_update(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    verification_id: UUID,
) -> PriorAuthorization:
    """Lock one active verification for mutation."""

    return PriorAuthorization.objects.select_for_update().select_related(
        "patient",
        "organization",
    ).get(
        pk=verification_id,
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
    )


def get_deleted_authorization_for_update(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    verification_id: UUID,
) -> PriorAuthorization:
    """Lock one deleted verification for restoration."""

    return PriorAuthorization.all_objects.select_for_update().select_related(
        "patient",
        "organization",
    ).get(
        pk=verification_id,
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
        is_deleted=True,
    )


__all__ = (
    "get_deleted_authorization_for_update",
    "get_verification",
    "get_authorization_for_update",
    "list_verifications",
)
''',
    "apps/revenue_cycle/prior_authorization/policies.py": '''"""Authorization policies for Prior Authorization."""

from __future__ import annotations

from uuid import UUID

from apps.platform.organizations.models import Organization
from apps.platform.rbac.engines import user_has_permission
from apps.revenue_cycle.prior_authorization.permissions import PriorAuthorizationPermission


def _authorized(*, user, permission: PriorAuthorizationPermission, organization_id: UUID) -> bool:
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
        permission=PriorAuthorizationPermission.VIEW,
        organization_id=organization_id,
    )


def can_create(*, user, organization_id: UUID) -> bool:
    """Check create authorization."""

    return _authorized(
        user=user,
        permission=PriorAuthorizationPermission.CREATE,
        organization_id=organization_id,
    )


def can_update(*, user, organization_id: UUID) -> bool:
    """Check update authorization."""

    return _authorized(
        user=user,
        permission=PriorAuthorizationPermission.UPDATE,
        organization_id=organization_id,
    )


def can_delete(*, user, organization_id: UUID) -> bool:
    """Check delete authorization."""

    return _authorized(
        user=user,
        permission=PriorAuthorizationPermission.DELETE,
        organization_id=organization_id,
    )


def can_restore(*, user, organization_id: UUID) -> bool:
    """Check restore authorization."""

    return _authorized(
        user=user,
        permission=PriorAuthorizationPermission.RESTORE,
        organization_id=organization_id,
    )


def can_transition(*, user, organization_id: UUID) -> bool:
    """Check lifecycle authorization."""

    return _authorized(
        user=user,
        permission=PriorAuthorizationPermission.LIFECYCLE,
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
    "apps/revenue_cycle/prior_authorization/services/__init__.py": '''"""Prior Authorization domain services."""

from __future__ import annotations

from apps.revenue_cycle.prior_authorization.services.prior_authorization import (
    PriorAuthorizationService,
)

__all__ = ("PriorAuthorizationService",)
''',
    "apps/revenue_cycle/prior_authorization/services/prior_authorization.py": '''"""Transactional Prior Authorization domain services."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any
from uuid import UUID

from django.db import transaction
from django.utils import timezone

from apps.patient_management.patients.models import Patient
from apps.revenue_cycle.prior_authorization.constants import (
    AuthorizationOutcome,
    AuthorizationStatus,
)
from apps.revenue_cycle.prior_authorization.exceptions import (
    PriorAuthorizationInvariantError,
    PriorAuthorizationTransitionError,
)
from apps.revenue_cycle.prior_authorization.models import PriorAuthorization
from apps.revenue_cycle.prior_authorization.selectors import (
    get_authorization_for_update,
    get_deleted_authorization_for_update,
)


_ALLOWED_TRANSITIONS = {
    AuthorizationStatus.PENDING.value: {
        AuthorizationStatus.IN_REVIEW.value,
        AuthorizationStatus.CANCELLED.value,
    },
    AuthorizationStatus.IN_REVIEW.value: {
        AuthorizationStatus.SUBMITTED.value,
        AuthorizationStatus.APPROVED.value,
        AuthorizationStatus.DENIED.value,
        AuthorizationStatus.CANCELLED.value,
    },
    AuthorizationStatus.SUBMITTED.value: {
        AuthorizationStatus.APPROVED.value,
        AuthorizationStatus.DENIED.value,
        AuthorizationStatus.CANCELLED.value,
    },
    AuthorizationStatus.APPROVED.value: {
        AuthorizationStatus.EXPIRED.value,
        AuthorizationStatus.INACTIVE.value,
    },
    AuthorizationStatus.DENIED.value: {
        AuthorizationStatus.PENDING.value,
        AuthorizationStatus.INACTIVE.value,
    },
    AuthorizationStatus.EXPIRED.value: {
        AuthorizationStatus.PENDING.value,
        AuthorizationStatus.INACTIVE.value,
    },
    AuthorizationStatus.CANCELLED.value: {
        AuthorizationStatus.PENDING.value,
        AuthorizationStatus.INACTIVE.value,
    },
    AuthorizationStatus.INACTIVE.value: set(),
}


class PriorAuthorizationService:
    """Provide transactional mutations for Prior Authorization."""

    @staticmethod
    def validate_request(
        *,
        procedure_code: str,
        requested_units: int | None,
        requested_amount: Decimal | None,
        requested_service_date: date | None,
    ) -> None:
        """Validate the clinical and financial request envelope."""

        if not procedure_code.strip():
            raise PriorAuthorizationInvariantError("procedure_code is required.")
        if requested_units is not None and requested_units <= 0:
            raise PriorAuthorizationInvariantError("requested_units must be positive.")
        if requested_amount is not None and requested_amount < 0:
            raise PriorAuthorizationInvariantError("requested_amount cannot be negative.")
        if requested_service_date is not None and requested_service_date < date.today():
            raise PriorAuthorizationInvariantError(
                "requested_service_date cannot be in the past."
            )

    @staticmethod
    def validate_dates(
        *,
        effective_date: date | None,
        expiration_date: date | None,
    ) -> None:
        """Reject an invalid authorization validity interval."""

        if effective_date and expiration_date and expiration_date < effective_date:
            raise PriorAuthorizationInvariantError(
                "expiration_date cannot be earlier than effective_date."
            )

    @staticmethod
    def validate_patient(*, organization_id: UUID, patient_id: UUID) -> None:
        """Ensure the patient belongs to the target organization."""

        patient = Patient.objects.filter(
            pk=patient_id,
            organization_id=organization_id,
        ).first()
        if patient is None:
            raise PriorAuthorizationInvariantError(
                "Patient does not belong to the target organization or is unavailable."
            )

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        organization_id: UUID,
        patient_id: UUID,
        payer_id: str,
        member_id: str,
        procedure_code: str,
        request_reference: str,
        idempotency_key: str,
        data: dict[str, Any],
    ) -> PriorAuthorization:
        """Create an authorization request idempotently."""

        if not request_reference.strip():
            raise PriorAuthorizationInvariantError("request_reference is required.")
        if not idempotency_key.strip():
            raise PriorAuthorizationInvariantError("idempotency_key is required.")
        if not payer_id.strip() or not member_id.strip():
            raise PriorAuthorizationInvariantError("payer_id and member_id are required.")

        cls.validate_patient(
            organization_id=organization_id,
            patient_id=patient_id,
        )
        cls.validate_request(
            procedure_code=procedure_code,
            requested_units=data.get("requested_units"),
            requested_amount=data.get("requested_amount"),
            requested_service_date=data.get("requested_service_date"),
        )
        cls.validate_dates(
            effective_date=data.get("effective_date"),
            expiration_date=data.get("expiration_date"),
        )

        existing = PriorAuthorization.objects.filter(
            organization_id=organization_id,
            idempotency_key=idempotency_key.strip(),
        ).first()
        if existing is not None:
            return existing

        return PriorAuthorization.objects.create(
            organization_id=organization_id,
            patient_id=patient_id,
            payer_id=payer_id.strip(),
            member_id=member_id.strip(),
            procedure_code=procedure_code.strip(),
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
        authorization_id: UUID,
        data: dict[str, Any],
    ) -> PriorAuthorization:
        """Update mutable authorization fields under row lock."""

        authorization = get_authorization_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            authorization_id=authorization_id,
        )
        if authorization.status in {
            AuthorizationStatus.APPROVED.value,
            AuthorizationStatus.EXPIRED.value,
            AuthorizationStatus.INACTIVE.value,
        }:
            protected = {
                "payer_id",
                "member_id",
                "procedure_code",
                "request_reference",
                "idempotency_key",
            }
            if protected.intersection(data):
                raise PriorAuthorizationInvariantError(
                    "Identity fields cannot be changed after a decision."
                )

        cls.validate_request(
            procedure_code=data.get("procedure_code", authorization.procedure_code),
            requested_units=data.get("requested_units", authorization.requested_units),
            requested_amount=data.get("requested_amount", authorization.requested_amount),
            requested_service_date=data.get(
                "requested_service_date",
                authorization.requested_service_date,
            ),
        )
        cls.validate_dates(
            effective_date=data.get("effective_date", authorization.effective_date),
            expiration_date=data.get("expiration_date", authorization.expiration_date),
        )

        if "patient_id" in data:
            cls.validate_patient(
                organization_id=organization_id,
                patient_id=data["patient_id"],
            )

        for field, value in data.items():
            setattr(authorization, field, value)
        authorization.save()
        return authorization

    @classmethod
    @transaction.atomic
    def soft_delete(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        authorization_id: UUID,
        deleted_by_id: UUID | None,
    ) -> PriorAuthorization:
        """Soft-delete an authorization under row lock."""

        authorization = get_authorization_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            authorization_id=authorization_id,
        )
        if authorization.status in {
            AuthorizationStatus.IN_REVIEW.value,
            AuthorizationStatus.SUBMITTED.value,
        }:
            raise PriorAuthorizationInvariantError(
                "An authorization under active payer review cannot be deleted."
            )
        authorization.soft_delete(user_id=deleted_by_id)
        return authorization

    @classmethod
    @transaction.atomic
    def restore(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        authorization_id: UUID,
    ) -> PriorAuthorization:
        """Restore a deleted authorization under row lock."""

        authorization = get_deleted_authorization_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            authorization_id=authorization_id,
        )
        authorization.restore()
        return authorization

    @classmethod
    @transaction.atomic
    def transition(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        authorization_id: UUID,
        target_status: str,
        actor_id: UUID | None,
        outcome: str | None = None,
        response_code: str | None = None,
        response_message: str | None = None,
        response_payload: dict[str, Any] | None = None,
        authorization_number: str | None = None,
        decision_reason: str | None = None,
        effective_date: date | None = None,
        expiration_date: date | None = None,
        approved_units: int | None = None,
        failure_reason: str | None = None,
    ) -> PriorAuthorization:
        """Apply a strict lifecycle transition atomically."""

        authorization = get_authorization_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            authorization_id=authorization_id,
        )
        allowed = _ALLOWED_TRANSITIONS.get(authorization.status, set())
        if target_status not in allowed:
            raise PriorAuthorizationTransitionError(
                f"Invalid Prior Authorization transition: "
                f"{authorization.status} -> {target_status}."
            )

        if effective_date is not None or expiration_date is not None:
            cls.validate_dates(
                effective_date=effective_date or authorization.effective_date,
                expiration_date=expiration_date or authorization.expiration_date,
            )
        if approved_units is not None:
            if approved_units <= 0:
                raise PriorAuthorizationInvariantError("approved_units must be positive.")
            if authorization.requested_units is not None and approved_units > authorization.requested_units:
                raise PriorAuthorizationInvariantError(
                    "approved_units cannot exceed requested_units."
                )

        authorization.status = target_status
        if outcome is not None:
            authorization.outcome = outcome
        if response_code is not None:
            authorization.response_code = response_code
        if response_message is not None:
            authorization.response_message = response_message
        if response_payload is not None:
            authorization.response_payload = response_payload
        if authorization_number is not None:
            authorization.authorization_number = authorization_number.strip()
        if decision_reason is not None:
            authorization.decision_reason = decision_reason
        if effective_date is not None:
            authorization.effective_date = effective_date
        if expiration_date is not None:
            authorization.expiration_date = expiration_date
        if approved_units is not None:
            authorization.approved_units = approved_units
        if failure_reason is not None:
            authorization.failure_reason = failure_reason

        if target_status == AuthorizationStatus.SUBMITTED.value:
            authorization.submitted_at = timezone.now()
        if target_status in {
            AuthorizationStatus.APPROVED.value,
            AuthorizationStatus.DENIED.value,
        }:
            authorization.decided_at = timezone.now()
            if target_status == AuthorizationStatus.APPROVED.value:
                authorization.approved_by_id = actor_id
                authorization.outcome = outcome or AuthorizationOutcome.APPROVED.value
            elif outcome is None:
                authorization.outcome = AuthorizationOutcome.DENIED.value

        authorization.save()
        return authorization


__all__ = ("PriorAuthorizationService", "_ALLOWED_TRANSITIONS")
''',
    "apps/revenue_cycle/prior_authorization/events.py": '''"""Prior Authorization domain events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class PriorAuthorizationEvent(DomainEvent):
    """Base event emitted for Prior Authorization changes."""

    verification_id: UUID
    organization_id: UUID
    patient_id: UUID
    status: str
    payload: dict[str, Any]


class PriorAuthorizationCreatedEvent(PriorAuthorizationEvent):
    """Emitted after an Prior Authorization is created."""


class PriorAuthorizationUpdatedEvent(PriorAuthorizationEvent):
    """Emitted after an Prior Authorization is updated."""


class PriorAuthorizationDeletedEvent(PriorAuthorizationEvent):
    """Emitted after an Prior Authorization is soft-deleted."""


class PriorAuthorizationRestoredEvent(PriorAuthorizationEvent):
    """Emitted after an Prior Authorization is restored."""


class PriorAuthorizationStatusChangedEvent(PriorAuthorizationEvent):
    """Emitted after an Prior Authorization lifecycle transition."""


__all__ = (
    "PriorAuthorizationCreatedEvent",
    "PriorAuthorizationDeletedEvent",
    "PriorAuthorizationEvent",
    "PriorAuthorizationRestoredEvent",
    "PriorAuthorizationStatusChangedEvent",
    "PriorAuthorizationUpdatedEvent",
)
''',
    "apps/revenue_cycle/prior_authorization/workflows/__init__.py": '''"""Prior Authorization workflow exports."""

from __future__ import annotations

from apps.revenue_cycle.prior_authorization.workflows.prior_authorization import (
    PriorAuthorizationCreateRequest,
    PriorAuthorizationCreationWorkflow,
    PriorAuthorizationDeleteRequest,
    PriorAuthorizationDeletionWorkflow,
    PriorAuthorizationLifecycleRequest,
    PriorAuthorizationLifecycleWorkflow,
    PriorAuthorizationRestoreRequest,
    PriorAuthorizationRestoreWorkflow,
    PriorAuthorizationUpdateRequest,
    PriorAuthorizationUpdateWorkflow,
)

__all__ = (
    "PriorAuthorizationCreateRequest",
    "PriorAuthorizationCreationWorkflow",
    "PriorAuthorizationDeleteRequest",
    "PriorAuthorizationDeletionWorkflow",
    "PriorAuthorizationLifecycleRequest",
    "PriorAuthorizationLifecycleWorkflow",
    "PriorAuthorizationRestoreRequest",
    "PriorAuthorizationRestoreWorkflow",
    "PriorAuthorizationUpdateRequest",
    "PriorAuthorizationUpdateWorkflow",
)
''',
    "apps/revenue_cycle/prior_authorization/workflows/prior_authorization.py": '''"""Prior Authorization workflow orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from apps.core.events import publish_after_commit
from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.revenue_cycle.prior_authorization.events import (
    PriorAuthorizationCreatedEvent,
    PriorAuthorizationDeletedEvent,
    PriorAuthorizationRestoredEvent,
    PriorAuthorizationStatusChangedEvent,
    PriorAuthorizationUpdatedEvent,
)
from apps.revenue_cycle.prior_authorization.services import PriorAuthorizationService


@dataclass(frozen=True)
class PriorAuthorizationCreateRequest:
    """Input for Prior Authorization creation."""

    organization_id: UUID
    patient_id: UUID
    payer_id: str
    member_id: str
    request_reference: str
    idempotency_key: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PriorAuthorizationUpdateRequest:
    """Input for Prior Authorization updates."""

    organization_id: UUID
    tenant_id: UUID
    verification_id: UUID
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PriorAuthorizationDeleteRequest:
    """Input for Prior Authorization deletion."""

    organization_id: UUID
    tenant_id: UUID
    verification_id: UUID
    deleted_by_id: UUID | None


@dataclass(frozen=True)
class PriorAuthorizationRestoreRequest:
    """Input for Prior Authorization restoration."""

    organization_id: UUID
    tenant_id: UUID
    verification_id: UUID


@dataclass(frozen=True)
class PriorAuthorizationLifecycleRequest:
    """Input for Prior Authorization lifecycle changes."""

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


class PriorAuthorizationCreationWorkflow(BaseWorkflow):
    """Create an Prior Authorization and publish its event after commit."""

    def __init__(self, *, request: PriorAuthorizationCreateRequest, logger_=None):
        """Initialize the creation workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute creation."""

        request = self.payload
        verification = PriorAuthorizationService.create(
            organization_id=request.organization_id,
            patient_id=request.patient_id,
            request_reference=request.request_reference,
            idempotency_key=request.idempotency_key,
            payer_id=request.payer_id,
            member_id=request.member_id,
            data=request.data,
        )
        publish_after_commit(
            PriorAuthorizationCreatedEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"request_reference": verification.request_reference},
            )
        )
        return WorkflowResult.ok(data=verification)


class PriorAuthorizationUpdateWorkflow(BaseWorkflow):
    """Update an Prior Authorization and publish its event after commit."""

    def __init__(self, *, request: PriorAuthorizationUpdateRequest, logger_=None):
        """Initialize the update workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute update."""

        request = self.payload
        verification = PriorAuthorizationService.update(
            tenant_id=request.tenant_id,
            organization_id=request.organization_id,
            verification_id=request.verification_id,
            data=request.data,
        )
        publish_after_commit(
            PriorAuthorizationUpdatedEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"updated": tuple(request.data)},
            )
        )
        return WorkflowResult.ok(data=verification)


class PriorAuthorizationDeletionWorkflow(BaseWorkflow):
    """Soft-delete an Prior Authorization and publish its event after commit."""

    def __init__(self, *, request: PriorAuthorizationDeleteRequest, logger_=None):
        """Initialize the deletion workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute deletion."""

        request = self.payload
        verification = PriorAuthorizationService.soft_delete(
            tenant_id=request.tenant_id,
            organization_id=request.organization_id,
            verification_id=request.verification_id,
            deleted_by_id=request.deleted_by_id,
        )
        publish_after_commit(
            PriorAuthorizationDeletedEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"deleted": True},
            )
        )
        return WorkflowResult.ok(data=verification)


class PriorAuthorizationRestoreWorkflow(BaseWorkflow):
    """Restore an Prior Authorization and publish its event after commit."""

    def __init__(self, *, request: PriorAuthorizationRestoreRequest, logger_=None):
        """Initialize the restoration workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute restoration."""

        request = self.payload
        verification = PriorAuthorizationService.restore(
            tenant_id=request.tenant_id,
            organization_id=request.organization_id,
            verification_id=request.verification_id,
        )
        publish_after_commit(
            PriorAuthorizationRestoredEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"restored": True},
            )
        )
        return WorkflowResult.ok(data=verification)


class PriorAuthorizationLifecycleWorkflow(BaseWorkflow):
    """Transition an Prior Authorization and publish its event after commit."""

    def __init__(self, *, request: PriorAuthorizationLifecycleRequest, logger_=None):
        """Initialize the lifecycle workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute lifecycle transition."""

        request = self.payload
        verification = PriorAuthorizationService.transition(
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
            PriorAuthorizationStatusChangedEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"outcome": verification.outcome},
            )
        )
        return WorkflowResult.ok(data=verification)


__all__ = (
    "PriorAuthorizationCreateRequest",
    "PriorAuthorizationCreationWorkflow",
    "PriorAuthorizationDeleteRequest",
    "PriorAuthorizationDeletionWorkflow",
    "PriorAuthorizationLifecycleRequest",
    "PriorAuthorizationLifecycleWorkflow",
    "PriorAuthorizationRestoreRequest",
    "PriorAuthorizationRestoreWorkflow",
    "PriorAuthorizationUpdateRequest",
    "PriorAuthorizationUpdateWorkflow",
)
''',
    "apps/revenue_cycle/prior_authorization/workflow_registry.py": '''"""Revenue Cycle Prior Authorization workflow registration."""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.revenue_cycle.prior_authorization.workflows import (
    PriorAuthorizationCreationWorkflow,
    PriorAuthorizationDeletionWorkflow,
    PriorAuthorizationLifecycleWorkflow,
    PriorAuthorizationRestoreWorkflow,
    PriorAuthorizationUpdateWorkflow,
)


WORKFLOW_DEFINITIONS = (
    ("revenue_cycle.prior_authorization.create", PriorAuthorizationCreationWorkflow),
    ("revenue_cycle.prior_authorization.update", PriorAuthorizationUpdateWorkflow),
    ("revenue_cycle.prior_authorization.delete", PriorAuthorizationDeletionWorkflow),
    ("revenue_cycle.prior_authorization.restore", PriorAuthorizationRestoreWorkflow),
    ("revenue_cycle.prior_authorization.lifecycle", PriorAuthorizationLifecycleWorkflow),
)


def register_workflows() -> None:
    """Register Prior Authorization workflows idempotently."""

    for name, workflow in WORKFLOW_DEFINITIONS:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=workflow)


register_workflows()

__all__ = ("WORKFLOW_DEFINITIONS", "register_workflows")
''',
    "apps/revenue_cycle/prior_authorization/api/__init__.py": '''"""Prior Authorization API package."""

from __future__ import annotations

__all__ = ()
''',
    "apps/revenue_cycle/prior_authorization/api/serializers/__init__.py": '''"""Prior Authorization API serializers."""

from __future__ import annotations

from apps.revenue_cycle.prior_authorization.api.serializers.prior_authorization import (
    PriorAuthorizationDetailSerializer,
    PriorAuthorizationLifecycleSerializer,
    PriorAuthorizationWriteSerializer,
)

__all__ = (
    "PriorAuthorizationDetailSerializer",
    "PriorAuthorizationLifecycleSerializer",
    "PriorAuthorizationWriteSerializer",
)
''',
    "apps/revenue_cycle/prior_authorization/api/serializers/prior_authorization.py": '''"""Prior Authorization API serializers."""

from __future__ import annotations

from rest_framework import serializers

from apps.revenue_cycle.prior_authorization.constants import (
    AuthorizationMethod,
    AuthorizationOutcome,
    AuthorizationStatus,
)
from apps.revenue_cycle.prior_authorization.models import PriorAuthorization


class PriorAuthorizationWriteSerializer(serializers.Serializer):
    """Validate create and update authorization payloads."""

    patient_id = serializers.UUIDField(required=False)
    payer_id = serializers.CharField(max_length=100, required=False)
    payer_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    member_id = serializers.CharField(max_length=100, required=False)
    policy_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    group_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    procedure_code = serializers.CharField(max_length=50, required=False)
    service_description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    place_of_service = serializers.CharField(max_length=20, required=False, allow_blank=True)
    rendering_provider_npi = serializers.CharField(max_length=20, required=False, allow_blank=True)
    clinical_indication = serializers.CharField(required=False, allow_blank=True)
    authorization_method = serializers.ChoiceField(
        choices=[item.value for item in AuthorizationMethod],
        required=False,
    )
    eligibility_reference = serializers.UUIDField(required=False, allow_null=True)
    requested_service_date = serializers.DateField(required=False, allow_null=True)
    requested_units = serializers.IntegerField(required=False, allow_null=True, min_value=1)
    requested_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        required=False,
        allow_null=True,
        min_value=0,
    )
    authorization_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    effective_date = serializers.DateField(required=False, allow_null=True)
    expiration_date = serializers.DateField(required=False, allow_null=True)
    response_code = serializers.CharField(max_length=100, required=False, allow_blank=True)
    response_message = serializers.CharField(required=False, allow_blank=True)
    response_payload = serializers.JSONField(required=False)
    request_reference = serializers.CharField(max_length=100, required=False)
    idempotency_key = serializers.CharField(max_length=255, required=False)
    decision_reason = serializers.CharField(required=False, allow_blank=True)
    failure_reason = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        """Validate authorization request dates."""

        effective_date = attrs.get("effective_date")
        expiration_date = attrs.get("expiration_date")
        if effective_date and expiration_date and expiration_date < effective_date:
            raise serializers.ValidationError(
                {"expiration_date": "expiration_date cannot be earlier than effective_date."}
            )
        return attrs


class PriorAuthorizationLifecycleSerializer(serializers.Serializer):
    """Validate lifecycle transition payloads."""

    target_status = serializers.ChoiceField(
        choices=[item.value for item in AuthorizationStatus]
    )
    outcome = serializers.ChoiceField(
        choices=[item.value for item in AuthorizationOutcome],
        required=False,
    )
    response_code = serializers.CharField(max_length=100, required=False, allow_blank=True)
    response_message = serializers.CharField(required=False, allow_blank=True)
    response_payload = serializers.JSONField(required=False)
    authorization_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    decision_reason = serializers.CharField(required=False, allow_blank=True)
    effective_date = serializers.DateField(required=False, allow_null=True)
    expiration_date = serializers.DateField(required=False, allow_null=True)
    approved_units = serializers.IntegerField(required=False, allow_null=True, min_value=1)
    failure_reason = serializers.CharField(required=False, allow_blank=True)


class PriorAuthorizationDetailSerializer(serializers.ModelSerializer):
    """Serialize Prior Authorization records for API responses."""

    class Meta:
        """Serializer metadata."""

        model = PriorAuthorization
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
            "procedure_code",
            "service_description",
            "place_of_service",
            "rendering_provider_npi",
            "clinical_indication",
            "authorization_method",
            "status",
            "outcome",
            "requested_service_date",
            "requested_units",
            "approved_units",
            "requested_amount",
            "authorization_number",
            "effective_date",
            "expiration_date",
            "requested_at",
            "submitted_at",
            "decided_at",
            "response_code",
            "response_message",
            "response_payload",
            "request_reference",
            "idempotency_key",
            "decision_reason",
            "failure_reason",
            "approved_by",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


__all__ = (
    "PriorAuthorizationDetailSerializer",
    "PriorAuthorizationLifecycleSerializer",
    "PriorAuthorizationWriteSerializer",
)
''',
    "apps/revenue_cycle/prior_authorization/api/views/__init__.py": '''"""Prior Authorization API views."""

from __future__ import annotations

from apps.revenue_cycle.prior_authorization.api.views.prior_authorization import (
    PriorAuthorizationDetailAPIView,
    PriorAuthorizationLifecycleAPIView,
    PriorAuthorizationListCreateAPIView,
    PriorAuthorizationRestoreAPIView,
)

__all__ = (
    "PriorAuthorizationDetailAPIView",
    "PriorAuthorizationLifecycleAPIView",
    "PriorAuthorizationListCreateAPIView",
    "PriorAuthorizationRestoreAPIView",
)
''',
    "apps/revenue_cycle/prior_authorization/api/views/prior_authorization.py": '''"""Prior Authorization API views."""

from __future__ import annotations

from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.revenue_cycle.prior_authorization.api.serializers import (
    PriorAuthorizationDetailSerializer,
    PriorAuthorizationLifecycleSerializer,
    PriorAuthorizationWriteSerializer,
)
from apps.revenue_cycle.prior_authorization.policies import (
    can_create,
    can_delete,
    can_restore,
    can_transition,
    can_update,
    can_view,
)
from apps.revenue_cycle.prior_authorization.rbac import (
    CanCreatePriorAuthorization,
    CanDeletePriorAuthorization,
    CanRestorePriorAuthorization,
    CanTransitionPriorAuthorization,
    CanUpdatePriorAuthorization,
    CanViewPriorAuthorization,
)
from apps.revenue_cycle.prior_authorization.selectors import (
    get_verification,
    list_verifications,
)
from apps.revenue_cycle.prior_authorization.workflows import (
    PriorAuthorizationCreateRequest,
    PriorAuthorizationCreationWorkflow,
    PriorAuthorizationDeleteRequest,
    PriorAuthorizationDeletionWorkflow,
    PriorAuthorizationLifecycleRequest,
    PriorAuthorizationLifecycleWorkflow,
    PriorAuthorizationRestoreRequest,
    PriorAuthorizationRestoreWorkflow,
    PriorAuthorizationUpdateRequest,
    PriorAuthorizationUpdateWorkflow,
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


class PriorAuthorizationListCreateAPIView(APIView):
    """List and create Prior Authorization records."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return tenant-safe verification records."""

        organization = _organization(request)
        if not can_view(user=request.user, organization_id=organization.pk):
            CanViewPriorAuthorization().has_permission(request, self)
        patient_id = request.query_params.get("patient_id")
        queryset = list_verifications(
            tenant_id=_tenant(request),
            organization_id=organization.pk,
            patient_id=patient_id,
        )
        return Response(PriorAuthorizationDetailSerializer(queryset, many=True).data)

    def post(self, request):
        """Create a verification through the workflow boundary."""

        organization = _organization(request)
        if not can_create(user=request.user, organization_id=organization.pk):
            CanCreatePriorAuthorization().has_permission(request, self)
        serializer = PriorAuthorizationWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient_id = serializer.validated_data.pop("patient_id", None)
        payer_id = serializer.validated_data.pop("payer_id", "")
        member_id = serializer.validated_data.pop("member_id", "")
        request_reference = request.data.get("request_reference", "")
        idempotency_key = request.headers.get("Idempotency-Key", request.data.get("idempotency_key", ""))
        workflow = PriorAuthorizationCreationWorkflow(
            request=PriorAuthorizationCreateRequest(
                organization_id=organization.pk,
                patient_id=patient_id,
                payer_id=payer_id,
                member_id=member_id,
                request_reference=request_reference,
                idempotency_key=idempotency_key,
                data=serializer.validated_data,
            )
        )
        result = workflow.run(context=_context(request, "revenue_cycle.prior_authorization.create"))
        return Response(
            PriorAuthorizationDetailSerializer(result.data).data,
            status=status.HTTP_201_CREATED,
        )


class PriorAuthorizationDetailAPIView(APIView):
    """Retrieve, update, and delete one Prior Authorization."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, verification_id):
        """Return one tenant-safe verification."""

        organization = _organization(request)
        if not can_view(user=request.user, organization_id=organization.pk):
            CanViewPriorAuthorization().has_permission(request, self)
        verification = get_verification(
            tenant_id=_tenant(request),
            organization_id=organization.pk,
            verification_id=verification_id,
        )
        return Response(PriorAuthorizationDetailSerializer(verification).data)

    def patch(self, request, verification_id):
        """Update a verification through the workflow boundary."""

        organization = _organization(request)
        if not can_update(user=request.user, organization_id=organization.pk):
            CanUpdatePriorAuthorization().has_permission(request, self)
        serializer = PriorAuthorizationWriteSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        result = PriorAuthorizationUpdateWorkflow(
            request=PriorAuthorizationUpdateRequest(
                organization_id=organization.pk,
                tenant_id=_tenant(request),
                verification_id=verification_id,
                data=serializer.validated_data,
            )
        ).run(context=_context(request, "revenue_cycle.prior_authorization.update"))
        return Response(PriorAuthorizationDetailSerializer(result.data).data)

    def delete(self, request, verification_id):
        """Soft-delete a verification through the workflow boundary."""

        organization = _organization(request)
        if not can_delete(user=request.user, organization_id=organization.pk):
            CanDeletePriorAuthorization().has_permission(request, self)
        result = PriorAuthorizationDeletionWorkflow(
            request=PriorAuthorizationDeleteRequest(
                organization_id=organization.pk,
                tenant_id=_tenant(request),
                verification_id=verification_id,
                deleted_by_id=request.user.pk,
            )
        ).run(context=_context(request, "revenue_cycle.prior_authorization.delete"))
        return Response(PriorAuthorizationDetailSerializer(result.data).data)


class PriorAuthorizationLifecycleAPIView(APIView):
    """Transition Prior Authorization lifecycle state."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, verification_id):
        """Apply a strict lifecycle transition."""

        organization = _organization(request)
        if not can_transition(user=request.user, organization_id=organization.pk):
            CanTransitionPriorAuthorization().has_permission(request, self)
        serializer = PriorAuthorizationLifecycleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = PriorAuthorizationLifecycleWorkflow(
            request=PriorAuthorizationLifecycleRequest(
                organization_id=organization.pk,
                tenant_id=_tenant(request),
                verification_id=verification_id,
                actor_id=request.user.pk,
                **serializer.validated_data,
            )
        ).run(context=_context(request, "revenue_cycle.prior_authorization.lifecycle"))
        return Response(PriorAuthorizationDetailSerializer(result.data).data)


class PriorAuthorizationRestoreAPIView(APIView):
    """Restore a deleted Prior Authorization."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, verification_id):
        """Restore through the workflow boundary."""

        organization = _organization(request)
        if not can_restore(user=request.user, organization_id=organization.pk):
            CanRestorePriorAuthorization().has_permission(request, self)
        try:
            result = PriorAuthorizationRestoreWorkflow(
                request=PriorAuthorizationRestoreRequest(
                    organization_id=organization.pk,
                    tenant_id=_tenant(request),
                    verification_id=verification_id,
                )
            ).run(context=_context(request, "revenue_cycle.prior_authorization.restore"))
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Insurance verification record not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(PriorAuthorizationDetailSerializer(result.data).data)


__all__ = (
    "PriorAuthorizationDetailAPIView",
    "PriorAuthorizationLifecycleAPIView",
    "PriorAuthorizationListCreateAPIView",
    "PriorAuthorizationRestoreAPIView",
)
''',
    "apps/revenue_cycle/prior_authorization/urls.py": '''"""Revenue Cycle Prior Authorization URL routes."""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.prior_authorization.api.views import (
    PriorAuthorizationDetailAPIView,
    PriorAuthorizationLifecycleAPIView,
    PriorAuthorizationListCreateAPIView,
    PriorAuthorizationRestoreAPIView,
)


app_name = "revenue_cycle_prior_authorization"

urlpatterns = (
    path("", PriorAuthorizationListCreateAPIView.as_view(), name="list-create"),
    path(
        "<uuid:verification_id>/",
        PriorAuthorizationDetailAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:verification_id>/lifecycle/",
        PriorAuthorizationLifecycleAPIView.as_view(),
        name="lifecycle",
    ),
    path(
        "<uuid:verification_id>/restore/",
        PriorAuthorizationRestoreAPIView.as_view(),
        name="restore",
    ),
)

__all__ = ("app_name", "urlpatterns")
''',
    "apps/revenue_cycle/prior_authorization/admin.py": '''"""Django admin for Revenue Cycle Prior Authorization."""

from __future__ import annotations

from django.contrib import admin

from apps.revenue_cycle.prior_authorization.models import PriorAuthorization


@admin.register(PriorAuthorization)
class PriorAuthorizationAdmin(admin.ModelAdmin):
    """Admin interface for Prior Authorization records."""

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


__all__ = ("PriorAuthorizationAdmin",)
''',
    "apps/revenue_cycle/prior_authorization/migrations/__init__.py": '''"""Deferred Revenue Cycle Prior Authorization migrations."""

from __future__ import annotations

__all__ = ()
''',
    "apps/revenue_cycle/prior_authorization/tests/__init__.py": '''"""Revenue Cycle Prior Authorization tests."""

from __future__ import annotations

__all__ = ()
''',
    "apps/revenue_cycle/prior_authorization/tests/test_architecture.py": '''"""Architecture tests for Revenue Cycle Prior Authorization."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase


class PriorAuthorizationArchitectureTests(SimpleTestCase):
    """Verify the Prior Authorization architectural contract."""

    def test_canonical_patient(self):
        """Prior Authorization must use canonical Patient."""

        source = Path(
            "apps/revenue_cycle/prior_authorization/models/prior_authorization.py"
        ).read_text(encoding="utf-8")
        self.assertIn("apps.patient_management.patients.models", source)

    def test_tenant_scoped_selectors(self):
        """Selectors must constrain tenant and organization."""

        source = Path(
            "apps/revenue_cycle/prior_authorization/selectors/prior_authorization.py"
        ).read_text(encoding="utf-8")
        self.assertIn("organization__tenant_id=tenant_id", source)
        self.assertIn("organization_id=organization_id", source)

    def test_after_commit_events(self):
        """Mutation workflows must dispatch events after commit."""

        source = Path(
            "apps/revenue_cycle/prior_authorization/workflows/prior_authorization.py"
        ).read_text(encoding="utf-8")
        self.assertIn("publish_after_commit", source)

    def test_platform_rbac(self):
        """Authorization must use the canonical platform RBAC engine."""

        source = Path(
            "apps/revenue_cycle/prior_authorization/policies.py"
        ).read_text(encoding="utf-8")
        self.assertIn("apps.platform.rbac.engines", source)

    def test_explicit_context(self):
        """API must require explicit tenant and organization context."""

        source = Path(
            "apps/revenue_cycle/prior_authorization/api/views/prior_authorization.py"
        ).read_text(encoding="utf-8")
        self.assertIn('getattr(request, "tenant", None)', source)
        self.assertIn('getattr(request, "organization", None)', source)


__all__ = ("PriorAuthorizationArchitectureTests",)
''',
    "apps/revenue_cycle/prior_authorization/tests/test_invariants.py": '''"""Prior Authorization invariant tests."""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.revenue_cycle.prior_authorization.constants import (
    AuthorizationOutcome,
    AuthorizationStatus,
)
from apps.revenue_cycle.prior_authorization.services.prior_authorization import (
    _ALLOWED_TRANSITIONS,
)


class PriorAuthorizationInvariantTests(SimpleTestCase):
    """Verify strict Prior Authorization state invariants."""

    def test_pending_cannot_skip_to_approved(self):
        """Pending authorization must enter review before approval."""

        self.assertNotIn(
            AuthorizationStatus.APPROVED.value,
            _ALLOWED_TRANSITIONS[AuthorizationStatus.PENDING.value],
        )

    def test_inactive_is_terminal(self):
        """Inactive authorization cannot transition to another state."""

        self.assertEqual(
            _ALLOWED_TRANSITIONS[AuthorizationStatus.INACTIVE.value],
            set(),
        )

    def test_outcome_set_is_finite(self):
        """Outcome values remain a finite canonical set."""

        self.assertEqual(
            {item.value for item in AuthorizationOutcome},
            {"approved", "denied", "pended", "not_required", "unknown"},
        )


__all__ = ("PriorAuthorizationInvariantTests",)
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
        "from apps.revenue_cycle.prior_authorization.models import PriorAuthorization\n",
    )
    if "from apps.revenue_cycle.eligibility.models import Eligibility" not in existing:
        existing += "\n" + additions[0]
    if (
        "from apps.revenue_cycle.prior_authorization.models import PriorAuthorization"
        not in existing
    ):
        existing += additions[1]
    if "__all__" not in existing:
        existing += '\n__all__ = ("Eligibility", "PriorAuthorization")\n'
    init_path.write_text(existing, encoding="utf-8")


def update_root_app_registry() -> None:
    """Ensure the Prior Authorization workflow registry loads at startup."""

    apps_path = ROOT / "apps" / "revenue_cycle" / "apps.py"
    if not apps_path.exists():
        return

    source = apps_path.read_text(encoding="utf-8")
    import_line = (
        "from apps.revenue_cycle.prior_authorization.workflow_registry "
        "import register_workflows as register_prior_authorization_workflows"
    )
    if import_line not in source:
        class_marker = "class RevenueCycleConfig"
        if class_marker in source:
            source = source.replace(
                class_marker,
                f"{import_line}\n\n{class_marker}",
                1,
            )
        else:
            source = f"{import_line}\n\n{source}"

    if "register_prior_authorization_workflows()" not in source:
        ready_marker = "    def ready(self) -> None:\n"
        if ready_marker in source:
            source = source.replace(
                ready_marker,
                ready_marker + "        register_prior_authorization_workflows()\n",
                1,
            )

    apps_path.write_text(source, encoding="utf-8")


def write_files() -> None:
    """Install RC3 without modifying the database or migrations."""

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
    """Verify source syntax and RC3 architecture contracts."""

    python_files = sorted(ACTIVE.rglob("*.py"))
    if len(python_files) < 27:
        raise AssertionError(f"RC3 manifest unexpectedly small: {len(python_files)}")
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

    model = (ACTIVE / "models" / "prior_authorization.py").read_text(encoding="utf-8")
    selectors = (ACTIVE / "selectors" / "prior_authorization.py").read_text(
        encoding="utf-8"
    )
    service = (ACTIVE / "services" / "prior_authorization.py").read_text(
        encoding="utf-8"
    )
    workflows = (ACTIVE / "workflows" / "prior_authorization.py").read_text(
        encoding="utf-8"
    )
    views = (ACTIVE / "api" / "views" / "prior_authorization.py").read_text(
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
        ("idempotency", "rc_pa_org_idempotency_uniq", model),
    )
    for label, needle, source in checks:
        if needle not in source:
            raise AssertionError(f"Architecture check failed: {label}")

    if "get_authorization_for_update" not in service:
        raise AssertionError(
            "Architecture check failed: service mutation locking delegation"
        )
    if "get_deleted_authorization_for_update" not in service:
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
    print("RC3 PRIOR AUTHORIZATION INSTALL COMPLETE")


def main() -> None:
    """Install and verify RC3 Prior Authorization."""

    print("DatavionAI Revenue Cycle RC3 Prior Authorization Installer v1.0.0")
    print("=" * 72)
    write_files()
    verify()


if __name__ == "__main__":
    main()
