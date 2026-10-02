"""Transactional domain services for Clinical Appointments."""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.clinical.appointments.constants import AppointmentStatus
from apps.clinical.appointments.models import Appointment
from apps.clinical.providers.models import Provider


class AppointmentService:
    """Perform transactional Appointment domain mutations."""

    @staticmethod
    def _window(
        *,
        scheduled_start: datetime,
        scheduled_end: datetime | None,
        duration_minutes: int,
    ):
        """Normalize and validate an appointment time window."""

        if scheduled_end is None:
            if duration_minutes <= 0:
                raise ValidationError("Appointment duration must be greater than zero.")
            scheduled_end = scheduled_start + timedelta(
                minutes=duration_minutes,
            )

        if scheduled_end <= scheduled_start:
            raise ValidationError("Appointment end time must be after start time.")

        calculated = int((scheduled_end - scheduled_start).total_seconds() // 60)
        if calculated <= 0:
            raise ValidationError("Appointment duration must be greater than zero.")

        return scheduled_start, scheduled_end, calculated

    @staticmethod
    def _ensure_scope(*, organization, patient, provider) -> None:
        """Validate organization ownership of Patient and Provider."""

        if str(patient.organization_id) != str(organization.pk):
            raise ValidationError("Patient does not belong to the organization.")

        if str(provider.organization_id) != str(organization.pk):
            raise ValidationError("Provider does not belong to the organization.")

    @staticmethod
    def _ensure_provider_available(
        *,
        provider_id,
        scheduled_start,
        scheduled_end,
        exclude_id=None,
    ) -> None:
        """Reject overlapping active provider appointments."""

        queryset = Appointment.objects.filter(
            provider_id=provider_id,
            scheduled_start__lt=scheduled_end,
            scheduled_end__gt=scheduled_start,
            status__in=(
                AppointmentStatus.SCHEDULED,
                AppointmentStatus.CONFIRMED,
                AppointmentStatus.CHECKED_IN,
                AppointmentStatus.IN_PROGRESS,
            ),
            is_deleted=False,
        )

        if exclude_id is not None:
            queryset = queryset.exclude(pk=exclude_id)

        if queryset.exists():
            raise ValidationError(
                "The provider is already booked for this time window."
            )

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        organization,
        patient,
        provider,
        scheduled_start,
        scheduled_end,
        data,
        actor=None,
        idempotency_key="",
    ) -> Appointment:
        """Create an appointment transactionally."""

        cls._ensure_scope(
            organization=organization,
            patient=patient,
            provider=provider,
        )

        if scheduled_start <= timezone.now():
            raise ValidationError("Appointment start must be in the future.")

        scheduled_start, scheduled_end, duration = cls._window(
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            duration_minutes=int(data.get("duration_minutes", 30)),
        )

        idempotency_key = str(idempotency_key or "").strip()
        if len(idempotency_key) > 128:
            raise ValidationError("Idempotency-Key cannot exceed 128 characters.")
        fingerprint_payload = {
            "organization_id": str(organization.pk),
            "patient_id": str(patient.pk),
            "provider_id": str(provider.pk),
            "scheduled_start": scheduled_start.isoformat(),
            "scheduled_end": scheduled_end.isoformat(),
            "duration_minutes": duration,
            "data": data,
        }
        request_fingerprint = hashlib.sha256(
            json.dumps(
                fingerprint_payload,
                sort_keys=True,
                separators=(",", ":"),
                default=str,
            ).encode("utf-8"),
        ).hexdigest()
        if idempotency_key:
            existing = Appointment.objects.filter(
                organization=organization,
                client_booking_key=idempotency_key,
                is_deleted=False,
            ).first()
            if existing:
                if existing.booking_request_fingerprint != request_fingerprint:
                    raise ValidationError(
                        "Idempotency-Key was already used with different appointment details."
                    )
                existing.tracking_token = hmac.new(
                    settings.SECRET_KEY.encode("utf-8"),
                    f"appointment-tracker:{organization.pk}:{idempotency_key}".encode(),
                    hashlib.sha256,
                ).hexdigest()
                return existing

        consultation_fee = Decimal(str(provider.consultation_fee)).quantize(
            Decimal("0.01"),
        )
        if consultation_fee <= 0:
            raise ValidationError(
                "The provider must have a consultation fee configured before booking."
            )
        deposit_amount = (consultation_fee / Decimal("2")).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
        if deposit_amount <= 0:
            raise ValidationError("The 50% booking deposit must be at least ₹0.01.")

        Provider.objects.select_for_update().get(
            pk=provider.pk,
            organization_id=organization.pk,
        )

        cls._ensure_provider_available(
            provider_id=provider.pk,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
        )

        payload = dict(data)
        payload.pop("duration_minutes", None)
        payload.update(
            organization=organization,
            patient=patient,
            provider=provider,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            duration_minutes=duration,
            consultation_fee=consultation_fee,
            client_booking_key=idempotency_key,
            booking_request_fingerprint=request_fingerprint if idempotency_key else "",
            status=AppointmentStatus.SCHEDULED,
        )

        record = Appointment(**payload)
        tracking_token = (
            hmac.new(
                settings.SECRET_KEY.encode("utf-8"),
                f"appointment-tracker:{organization.pk}:{idempotency_key}".encode(),
                hashlib.sha256,
            ).hexdigest()
            if idempotency_key
            else secrets.token_urlsafe(32)
        )
        record.tracking_token_hash = hashlib.sha256(
            tracking_token.encode("utf-8"),
        ).hexdigest()
        record.full_clean()
        record.save()
        record.tracking_token = tracking_token

        from apps.revenue_cycle.billing.healthcare_services import (
            create_invoice,
            finalize_invoice,
        )

        invoice = create_invoice(
            organization=organization,
            invoice_number=f"APD-{record.id.hex.upper()}",
            patient_reference=str(patient.pk),
            claim_reference=f"appointment:{record.pk}",
            due_date=scheduled_start.date(),
            lines=[
                {
                    "service_code": "APPOINTMENT_DEPOSIT",
                    "description": f"50% booking deposit for {record.appointment_number}",
                    "quantity": Decimal("1.0000"),
                    "unit_price": deposit_amount,
                }
            ],
            actor=actor,
        )
        finalize_invoice(
            organization=organization,
            invoice=invoice,
            actor=actor,
        )
        record.deposit_invoice_id = invoice.pk
        record.save(update_fields=["deposit_invoice_id", "updated_at"])

        return record

    @staticmethod
    @transaction.atomic
    def update(*, record, data) -> Appointment:
        """Update mutable appointment fields."""

        if record.is_terminal:
            raise ValidationError("A terminal appointment cannot be updated.")

        allowed = {
            "appointment_type",
            "priority",
            "reason",
            "notes",
            "is_virtual",
            "meeting_url",
        }

        unknown = set(data) - allowed
        if unknown:
            raise ValidationError("Unsupported fields: " + ", ".join(sorted(unknown)))

        for field, value in data.items():
            setattr(record, field, value)

        record.full_clean()
        record.save()

        return record

    @staticmethod
    @transaction.atomic
    def delete(*, record, actor=None) -> Appointment:
        """Soft-delete an appointment and remove it from active records."""

        record.soft_delete(
            user_id=getattr(actor, "pk", None),
        )
        if hasattr(record, "is_active") and record.is_active:
            record.is_active = False
            record.save(
                update_fields=["is_active"],
            )
        return record

    @classmethod
    @transaction.atomic
    def transition(
        cls,
        *,
        record,
        target_status,
        reason="",
        actor=None,
    ) -> Appointment:
        """Apply a validated appointment lifecycle transition."""

        allowed = {
            AppointmentStatus.SCHEDULED: {
                AppointmentStatus.CONFIRMED,
                AppointmentStatus.CANCELLED,
                AppointmentStatus.NO_SHOW,
            },
            AppointmentStatus.CONFIRMED: {
                AppointmentStatus.CHECKED_IN,
                AppointmentStatus.CANCELLED,
                AppointmentStatus.NO_SHOW,
            },
            AppointmentStatus.CHECKED_IN: {
                AppointmentStatus.IN_PROGRESS,
                AppointmentStatus.CANCELLED,
            },
            AppointmentStatus.IN_PROGRESS: {
                AppointmentStatus.COMPLETED,
            },
        }

        current = record.status

        if target_status == current:
            return record

        if target_status not in allowed.get(current, set()):
            raise ValidationError(
                f"Invalid appointment transition: {current} -> {target_status}."
            )

        if target_status == AppointmentStatus.CANCELLED:
            if not reason.strip():
                raise ValidationError("Cancellation reason is required.")
            record.cancellation_reason = reason.strip()

        if (
            target_status == AppointmentStatus.NO_SHOW
            and timezone.now() < record.scheduled_end
        ):
            raise ValidationError(
                "A no-show can only be recorded after the scheduled appointment ends."
            )

        if target_status == AppointmentStatus.CHECKED_IN:
            if not record.deposit_paid:
                raise ValidationError(
                    "The appointment booking deposit must be paid before check-in."
                )
            from apps.revenue_cycle.billing.healthcare_services import (
                apply_adjustment,
                create_invoice,
                finalize_invoice,
            )

            invoice = create_invoice(
                organization=record.organization,
                invoice_number=f"APF-{record.id.hex.upper()}",
                patient_reference=str(record.patient_id),
                claim_reference=f"appointment:{record.pk}:visit",
                due_date=record.scheduled_start.date(),
                lines=[
                    {
                        "service_code": "CONSULTATION",
                        "description": f"Consultation for {record.appointment_number}",
                        "quantity": Decimal("1.0000"),
                        "unit_price": record.consultation_fee,
                    }
                ],
                actor=actor,
            )
            finalize_invoice(
                organization=record.organization,
                invoice=invoice,
                actor=actor,
            )
            apply_adjustment(
                organization=record.organization,
                invoice=invoice,
                amount=-record.deposit_amount,
                reason="discount",
                reference=f"appointment:{record.pk}:deposit-credit",
                actor=actor,
            )
            record.final_invoice_id = invoice.pk
            record.check_in_at = timezone.now()

        if target_status == AppointmentStatus.COMPLETED:
            record.check_out_at = timezone.now()

        record.status = target_status
        record.full_clean()
        record.save()

        return record

    @classmethod
    @transaction.atomic
    def reschedule(
        cls,
        *,
        record,
        scheduled_start,
        scheduled_end,
        duration_minutes,
    ) -> Appointment:
        """Reschedule an appointment outside the six-hour cutoff."""

        if not record.can_reschedule:
            raise ValidationError(
                "Appointments cannot be rescheduled within 6 hours of start time."
            )

        if scheduled_start <= timezone.now():
            raise ValidationError("New appointment start must be in the future.")

        next_day = timezone.localdate() + timedelta(days=1)
        if timezone.localtime(scheduled_start).date() != next_day:
            raise ValidationError(
                "An appointment may only be rescheduled to the next calendar day."
            )

        scheduled_start, scheduled_end, duration = cls._window(
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            duration_minutes=duration_minutes,
        )

        Provider.objects.select_for_update().get(
            pk=record.provider_id,
            organization_id=record.organization_id,
        )

        cls._ensure_provider_available(
            provider_id=record.provider_id,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            exclude_id=record.pk,
        )

        record.scheduled_start = scheduled_start
        record.scheduled_end = scheduled_end
        record.duration_minutes = duration
        record.reschedule_count += 1
        record.status = AppointmentStatus.SCHEDULED
        record.full_clean()
        record.save()

        return record


__all__ = ("AppointmentService",)
