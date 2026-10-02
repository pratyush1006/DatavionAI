"""
Canonical application service for clinical prescriptions.

Clinical prescription deletion is a SOFT DELETE.

The physical database row is retained. Deletion records:
    - is_active = False
    - is_deleted = True
    - deleted_at = current timestamp
    - deleted_by_id = acting user

No physical SQL DELETE is performed by this service.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from uuid import UUID

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import ForeignKey
from django.utils import timezone

from apps.clinical.appointments.constants import AppointmentStatus
from apps.clinical.appointments.models import Appointment
from apps.clinical.appointments.services import AppointmentService
from apps.clinical.encounters.constants import EncounterStatus
from apps.clinical.encounters.models import Encounter
from apps.clinical.encounters.services import EncounterService
from apps.clinical.prescriptions.models import Prescription
from apps.platform.organizations.models import Organization

User = get_user_model()


class PrescriptionService:
    """Transactional, organization-scoped prescription mutations."""

    @staticmethod
    def resolve_actor(*, actor_id: UUID):
        """Resolve the acting user."""
        try:
            return User.objects.get(pk=actor_id)
        except User.DoesNotExist as exc:
            raise ValidationError(
                "Actor user does not exist.",
            ) from exc

    @staticmethod
    def _org_id(value: Any) -> str:
        """Normalize an organization identifier."""
        return str(getattr(value, "pk", value))

    @classmethod
    def _organization_from_value(
        cls,
        value: Any,
    ) -> Any | None:
        """Extract an Organization from an object or nested mapping."""
        if value is None:
            return None

        organization = getattr(
            value,
            "organization",
            None,
        )
        if organization is not None:
            return organization

        organization_id = getattr(
            value,
            "organization_id",
            None,
        )
        if organization_id is not None:
            try:
                return Organization.objects.get(
                    pk=organization_id,
                )
            except Organization.DoesNotExist:
                return None

        if isinstance(value, Mapping):
            candidate = value.get("organization")
            if candidate is not None:
                if not isinstance(candidate, (str, bytes)):
                    return candidate
                try:
                    return Organization.objects.get(pk=candidate)
                except (
                    Organization.DoesNotExist,
                    ValueError,
                    TypeError,
                ):
                    pass

            candidate_id = value.get("organization_id")
            if candidate_id is not None:
                try:
                    return Organization.objects.get(pk=candidate_id)
                except (
                    Organization.DoesNotExist,
                    ValueError,
                    TypeError,
                ):
                    pass

            for nested in value.values():
                candidate = cls._organization_from_value(nested)
                if candidate is not None:
                    return candidate

        return None

    @classmethod
    def resolve_organization(
        cls,
        *,
        organization=None,
        organization_id=None,
        tenant_id=None,
        request=None,
        context=None,
        data=None,
        prescription=None,
        instance=None,
    ):
        """Resolve the organization context."""
        if request is not None:
            if organization is None:
                organization = getattr(
                    request,
                    "organization",
                    None,
                )
            if organization_id is None:
                organization_id = getattr(
                    request,
                    "organization_id",
                    None,
                )
            if tenant_id is None:
                tenant_id = getattr(
                    request,
                    "tenant_id",
                    None,
                )
            if data is None:
                data = getattr(
                    request,
                    "data",
                    None,
                )

        if context is not None:
            if organization is None:
                organization = getattr(
                    context,
                    "organization",
                    None,
                )
            if organization_id is None:
                organization_id = getattr(
                    context,
                    "organization_id",
                    None,
                )
            if tenant_id is None:
                tenant_id = getattr(
                    context,
                    "tenant_id",
                    None,
                )

        if organization is not None:
            resolved = cls._organization_from(
                organization=organization,
                data=data,
                prescription=prescription,
                instance=instance,
            )
        elif organization_id is not None:
            lookup = {"pk": organization_id}
            if tenant_id is not None:
                lookup["tenant_id"] = tenant_id

            try:
                resolved = Organization.objects.get(**lookup)
            except (
                Organization.DoesNotExist,
                ValueError,
                TypeError,
            ) as exc:
                raise ValidationError(
                    "Organization context is required for prescription mutation.",
                ) from exc
        else:
            resolved = cls._organization_from(
                data=data,
                prescription=prescription,
                instance=instance,
            )

        if organization_id is not None and str(resolved.pk) != str(organization_id):
            raise ValidationError(
                "Organization boundary violation.",
            )

        if tenant_id is not None and str(resolved.tenant_id) != str(tenant_id):
            raise ValidationError(
                "Organization tenant boundary violation.",
            )

        return resolved

    @classmethod
    def _organization_from(
        cls,
        *,
        organization: Any | None = None,
        data: Mapping[str, Any] | None = None,
        prescription: Any | None = None,
        instance: Any | None = None,
    ) -> Any:
        """Resolve an organization from explicit or related values."""
        if organization is not None:
            if isinstance(organization, (str, bytes)):
                try:
                    return Organization.objects.get(
                        pk=organization,
                    )
                except (
                    Organization.DoesNotExist,
                    ValueError,
                    TypeError,
                ) as exc:
                    raise ValidationError(
                        "Organization context is required for prescription mutation.",
                    ) from exc
            return organization

        current = prescription or instance

        candidate = cls._organization_from_value(current)
        if candidate is not None:
            return candidate

        candidate = cls._organization_from_value(data or {})
        if candidate is not None:
            return candidate

        raise ValidationError(
            "Organization context is required for prescription mutation.",
        )

    @classmethod
    def _locked(
        cls,
        *,
        organization: Any,
        prescription: Any | None = None,
        instance: Any | None = None,
        prescription_id: Any | None = None,
        record_id: Any | None = None,
    ) -> Prescription:
        """Retrieve an organization-scoped prescription with a row lock."""
        current = prescription or instance

        identifier = getattr(current, "pk", current) if current is not None else None
        identifier = identifier or prescription_id or record_id

        if identifier is None:
            raise ValidationError(
                "Prescription identifier is required.",
            )

        try:
            return Prescription.objects.select_for_update().get(
                pk=identifier,
                organization_id=organization.pk,
            )
        except Prescription.DoesNotExist as exc:
            raise ValidationError(
                "Prescription was not found.",
            ) from exc

    @staticmethod
    def _normalize_foreign_keys(
        payload: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Resolve primitive foreign-key identifiers."""
        normalized = dict(payload)

        for name, value in list(normalized.items()):
            if value is None:
                continue

            try:
                field = Prescription._meta.get_field(name)
            except Exception:
                continue

            if not isinstance(field, ForeignKey):
                continue

            related_model = field.remote_field.model

            if isinstance(value, related_model):
                continue

            try:
                normalized[name] = related_model.objects.get(
                    pk=value,
                )
            except (
                related_model.DoesNotExist,
                ValueError,
                TypeError,
            ) as exc:
                raise ValidationError(
                    {name: "Related object does not exist."},
                ) from exc

        return normalized

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        organization: Any | None = None,
        data: Mapping[str, Any] | None = None,
        validated_data: Mapping[str, Any] | None = None,
        performed_by: Any | None = None,
        **kwargs: Any,
    ) -> Prescription:
        """Create and validate a prescription."""
        payload = dict(data or {})
        payload.update(dict(validated_data or {}))
        payload.update(kwargs)

        verification_fields = {"is_verified", "verified_at", "verified_by"}
        if verification_fields.intersection(payload):
            raise ValidationError(
                "Prescription verification can only be changed through its lifecycle transition."
            )

        organization = cls._organization_from(
            organization=organization,
            data=payload,
        )

        supplied_org = payload.pop("organization", None)
        supplied_org_id = payload.pop("organization_id", None)
        expected = cls._org_id(organization)

        if supplied_org is not None and cls._org_id(supplied_org) != expected:
            raise ValidationError(
                "Organization boundary violation.",
            )

        if supplied_org_id is not None and str(supplied_org_id) != expected:
            raise ValidationError(
                "Organization boundary violation.",
            )

        payload["organization"] = organization
        payload = cls._normalize_foreign_keys(payload)

        obj = Prescription(**payload)
        obj.full_clean()
        obj.save(force_insert=True)
        obj.full_clean()

        return obj

    @classmethod
    @transaction.atomic
    def update(
        cls,
        *,
        organization: Any | None = None,
        prescription: Any | None = None,
        instance: Any | None = None,
        prescription_id: Any | None = None,
        record_id: Any | None = None,
        data: Mapping[str, Any] | None = None,
        validated_data: Mapping[str, Any] | None = None,
        performed_by: Any | None = None,
        **kwargs: Any,
    ) -> Prescription:
        """Update an active, non-deleted prescription."""
        payload = dict(data or {})
        payload = cls._normalize_foreign_keys(payload)
        payload.update(dict(validated_data or {}))
        payload.update(kwargs)

        current = prescription or instance

        organization = cls._organization_from(
            organization=organization,
            data=payload,
            prescription=current,
            instance=current,
        )

        obj = cls._locked(
            organization=organization,
            prescription=current,
            instance=current,
            prescription_id=prescription_id,
            record_id=record_id,
        )

        if obj.is_deleted:
            raise ValidationError(
                "Deleted prescriptions cannot be updated.",
            )

        payload.pop("id", None)
        payload.pop("organization", None)
        payload.pop("organization_id", None)

        writable = {
            field.name
            for field in obj._meta.fields
            if not field.primary_key
            and not getattr(field, "auto_now", False)
            and not getattr(field, "auto_now_add", False)
        }
        writable.difference_update({"is_verified", "verified_at", "verified_by"})

        unknown = sorted(set(payload) - writable)
        if unknown:
            raise ValidationError(
                {name: f"Field '{name}' is not writable." for name in unknown},
            )

        for name, value in payload.items():
            setattr(obj, name, value)

        obj.full_clean()
        obj.save()

        return obj

    @classmethod
    @transaction.atomic
    def transition(
        cls,
        *,
        organization,
        record_id,
        target,
        performed_by=None,
    ) -> Prescription:
        """Verify a prescription; finish the encounter only when all are verified."""

        obj = cls._locked(
            organization=organization,
            record_id=record_id,
        )
        if obj.is_deleted:
            raise ValidationError("Deleted prescriptions cannot be verified.")
        if target != "verify":
            raise ValidationError(
                "Only the verify prescription transition is supported."
            )

        actor_id = getattr(performed_by, "pk", performed_by)
        if not actor_id:
            raise ValidationError(
                "An authenticated doctor is required to verify a prescription."
            )
        if str(obj.provider.employee.user_id) != str(actor_id) and not getattr(
            performed_by, "is_superuser", False
        ):
            raise ValidationError(
                "Only the prescribing doctor may verify this prescription."
            )

        encounter = Encounter.objects.select_for_update().get(
            pk=obj.encounter_id,
            organization=organization,
        )

        if not obj.is_verified:
            obj.is_verified = True
            obj.verified_at = timezone.now()
            obj.verified_by = performed_by
            obj.save(
                update_fields=(
                    "is_verified",
                    "verified_at",
                    "verified_by",
                    "updated_at",
                )
            )

        outstanding = Prescription.objects.filter(
            organization=organization,
            encounter_id=obj.encounter_id,
            is_deleted=False,
            is_verified=False,
        ).exists()
        if outstanding:
            return obj

        encounter_is_complete_for_checkout = encounter.status in {
            EncounterStatus.IN_PROGRESS,
            EncounterStatus.COMPLETED,
        }
        if encounter.status == EncounterStatus.IN_PROGRESS:
            EncounterService.transition(
                encounter=encounter,
                target_status=EncounterStatus.COMPLETED,
                actor_id=actor_id,
            )

        appointment = Appointment.objects.select_for_update().get(
            pk=encounter.appointment_id,
            organization=organization,
        )
        if (
            encounter_is_complete_for_checkout
            and appointment.status == AppointmentStatus.IN_PROGRESS
        ):
            AppointmentService.transition(
                record=appointment,
                target_status=AppointmentStatus.COMPLETED,
                actor=performed_by,
            )
        return obj

    @classmethod
    @transaction.atomic
    def delete(
        cls,
        *,
        organization: Any | None = None,
        record_id: Any | None = None,
        prescription_id: Any | None = None,
        prescription: Any | None = None,
        instance: Any | None = None,
        performed_by: Any | None = None,
    ) -> Prescription:
        """
        Soft-delete a prescription.

        This operation intentionally retains the physical database row.
        All soft-delete state is persisted in one ORM UPDATE:
            is_active = False
            is_deleted = True
            deleted_at = current timestamp
            deleted_by_id = actor
        """
        current = prescription or instance

        resolved_id = prescription_id if prescription_id is not None else record_id

        organization = cls.resolve_organization(
            organization=organization,
            prescription=current,
            instance=current,
        )

        obj = cls._locked(
            organization=organization,
            prescription=current,
            instance=current,
            prescription_id=resolved_id,
            record_id=record_id,
        )

        if obj.is_deleted:
            raise ValidationError(
                "Prescription is already soft-deleted.",
            )

        actor_id = getattr(
            performed_by,
            "pk",
            performed_by,
        )

        now = timezone.now()

        obj.is_active = False
        obj.is_deleted = True
        obj.deleted_at = now
        obj.deleted_by_id = actor_id

        obj.save(
            update_fields=[
                "is_active",
                "is_deleted",
                "deleted_at",
                "deleted_by_id",
            ],
        )

        db_alias = obj._state.db or "default"

        persisted = Prescription.all_objects.using(db_alias).get(pk=obj.pk)

        if persisted.is_active is not False:
            raise ValidationError(
                "Prescription soft-delete verification failed: is_active is not false.",
            )

        if persisted.is_deleted is not True:
            raise ValidationError(
                "Prescription soft-delete verification failed: is_deleted is not true.",
            )

        if persisted.deleted_at is None:
            raise ValidationError(
                "Prescription soft-delete verification failed: deleted_at is missing.",
            )

        return Prescription.deleted_objects.using(db_alias).get(pk=obj.pk)


def create_prescription(
    *,
    organization: Any | None = None,
    data: Mapping[str, Any] | None = None,
    validated_data: Mapping[str, Any] | None = None,
    performed_by: Any | None = None,
    **kwargs: Any,
) -> Prescription:
    """Public prescription creation wrapper."""
    return PrescriptionService.create(
        organization=organization,
        data=data,
        validated_data=validated_data,
        performed_by=performed_by,
        **kwargs,
    )


def update_prescription(
    prescription: Any = None,
    *,
    instance: Any | None = None,
    prescription_id: Any | None = None,
    record_id: Any | None = None,
    organization: Any | None = None,
    data: Mapping[str, Any] | None = None,
    validated_data: Mapping[str, Any] | None = None,
    performed_by: Any | None = None,
    **kwargs: Any,
) -> Prescription:
    """Public prescription update wrapper."""
    return PrescriptionService.update(
        organization=organization,
        prescription=prescription,
        instance=instance,
        prescription_id=prescription_id,
        record_id=record_id,
        data=data,
        validated_data=validated_data,
        performed_by=performed_by,
        **kwargs,
    )


def delete_prescription(
    prescription: Any = None,
    *,
    instance: Any | None = None,
    prescription_id: Any | None = None,
    record_id: Any | None = None,
    organization: Any | None = None,
    performed_by: Any | None = None,
) -> Prescription:
    """Public prescription soft-delete wrapper."""
    return PrescriptionService.delete(
        organization=organization,
        prescription=prescription,
        instance=instance,
        prescription_id=prescription_id,
        record_id=record_id,
        performed_by=performed_by,
    )


__all__ = (
    "PrescriptionService",
    "create_prescription",
    "update_prescription",
    "delete_prescription",
)
