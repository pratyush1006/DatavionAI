"""Workflow-based Clinical Appointment API views."""

from __future__ import annotations

import hashlib

from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.clinical.appointments.api.serializers import (
    AppointmentCancelSerializer,
    AppointmentCheckInSerializer,
    AppointmentCreateSerializer,
    AppointmentDepositVerifySerializer,
    AppointmentRescheduleSerializer,
    AppointmentSerializer,
    AppointmentUpdateSerializer,
)
from apps.clinical.appointments.models import Appointment
from apps.clinical.appointments.permissions.api import AppointmentAPIPermission
from apps.clinical.appointments.selectors import AppointmentSelector
from apps.clinical.appointments.workflows import (
    AppointmentBookingRequest,
    AppointmentBookingWorkflow,
    AppointmentCancelRequest,
    AppointmentCancelWorkflow,
    AppointmentCheckInWorkflow,
    AppointmentCompleteWorkflow,
    AppointmentConfirmWorkflow,
    AppointmentDeleteRequest,
    AppointmentDeleteWorkflow,
    AppointmentNoShowWorkflow,
    AppointmentRescheduleRequest,
    AppointmentRescheduleWorkflow,
    AppointmentStartWorkflow,
    AppointmentUpdateRequest,
    AppointmentUpdateWorkflow,
)
from apps.common.api.responses import (
    created_response,
    error_response,
    success_response,
)
from apps.core.workflows import WorkflowContext
from apps.platform.saas_billing.gateways.razorpay import RazorpayGateway
from apps.platform.saas_billing.razorpay_config import RAZORPAY_KEY_ID
from apps.revenue_cycle.billing.healthcare_models import (
    HealthcareInvoice,
    HealthcarePayment,
)
from apps.revenue_cycle.billing.healthcare_services import (
    create_pending_payment,
    settle_pending_payment,
)
from apps.transcription.models import LiveTranscriptionSession
from apps.transcription.services.live import LiveTranscriptionService


def organization_from_request(request):
    """Return the tenant-consistent organization resolved by middleware.

    ``User`` does not carry a ``tenant_id`` field.  The former implementation
    attempted to filter an organization with that nonexistent value whenever a
    platform user selected an organization, which turned an otherwise valid
    appointments list request into a 500.  The shared context middleware is
    the single source of truth for the active organization.
    """

    organization = getattr(request, "organization", None)

    if organization is None:
        organization = getattr(request.user, "organization", None)

    if organization is None or not organization.is_active:
        raise PermissionDenied("An active organization context is required.")

    tenant = getattr(request, "tenant", None)
    if tenant is not None and organization.tenant_id != tenant.id:
        raise PermissionDenied(
            "The selected organization is outside the active tenant."
        )

    return organization


def workflow_context(
    request,
    workflow_name: str,
):
    """Build the canonical immutable WorkflowContext."""

    organization = organization_from_request(request)

    return WorkflowContext(
        tenant_id=organization.tenant_id,
        actor_id=request.user.id,
        workflow_name=workflow_name,
        request_id=request.headers.get(
            "X-Request-ID",
        ),
    )


def _response(request, result, *, status_code=status.HTTP_200_OK):
    """Serialize a successful workflow result."""

    return success_response(
        data=AppointmentSerializer(
            getattr(result, "data", result),
        ).data,
        request=request,
        status_code=status_code,
    )


class AppointmentListCreateView(APIView):
    """List and create organization-scoped appointments."""

    serializer_class = AppointmentSerializer

    def get_permissions(self):
        if self.request.method in {"GET", "HEAD"}:
            return [IsAuthenticated(), AppointmentAPIPermission(action="view")]
        return [IsAuthenticated(), AppointmentAPIPermission(action="create")]

    def get_permissions(self):
        action = "view" if self.request.method in {"GET", "HEAD"} else "create"
        return [IsAuthenticated(), AppointmentAPIPermission(action=action)]

    def get(self, request):
        """List appointments."""

        organization = organization_from_request(
            request,
        )

        queryset = AppointmentSelector.queryset(
            organization=organization,
        )

        return success_response(
            data=AppointmentSerializer(
                queryset,
                many=True,
            ).data,
            request=request,
        )

    def post(self, request):
        """Create an appointment through the workflow."""

        organization = organization_from_request(
            request,
        )

        serializer = AppointmentCreateSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        data = dict(
            serializer.validated_data,
        )

        patient_id = data.pop(
            "patient_id",
        )
        provider_id = data.pop(
            "provider_id",
        )

        result = AppointmentBookingWorkflow(
            request=AppointmentBookingRequest(
                organization_id=organization.id,
                patient_id=patient_id,
                provider_id=provider_id,
                scheduled_start=data.pop(
                    "scheduled_start",
                ),
                scheduled_end=data.pop(
                    "scheduled_end",
                ),
                data=data,
                actor=request.user,
                idempotency_key=request.headers.get("Idempotency-Key", "").strip(),
            ),
        ).execute(
            context=workflow_context(
                request,
                "appointment.create",
            ),
        )

        return created_response(
            data={
                **AppointmentSerializer(
                    result.data,
                ).data,
                "tracking_token": result.data.tracking_token,
            },
            request=request,
        )


class AppointmentTrackView(APIView):
    """Return a privacy-limited live status using a one-time-issued bearer token."""

    serializer_class = AppointmentSerializer

    permission_classes = (AllowAny,)

    def get(self, request, tracking_token):
        token_hash = hashlib.sha256(tracking_token.encode("utf-8")).hexdigest()
        appointment = get_object_or_404(
            Appointment.objects.filter(is_deleted=False),
            tracking_token_hash=token_hash,
        )
        return success_response(
            data={
                "appointment_number": appointment.appointment_number,
                "status": appointment.status,
                "scheduled_start": appointment.scheduled_start,
                "scheduled_end": appointment.scheduled_end,
                "deposit_paid": appointment.deposit_paid,
                "can_reschedule": appointment.can_reschedule,
            },
            request=request,
        )


class AppointmentDetailView(APIView):
    """Retrieve, update, and delete one appointment."""

    serializer_class = AppointmentSerializer

    def get_permissions(self):
        action = {
            "GET": "view",
            "HEAD": "view",
            "PATCH": "update",
            "DELETE": "delete",
        }.get(self.request.method)
        return [IsAuthenticated(), AppointmentAPIPermission(action=action)]

    def get(
        self,
        request,
        appointment_id,
    ):
        """Retrieve an appointment."""

        organization = organization_from_request(
            request,
        )

        record = get_object_or_404(
            AppointmentSelector.queryset(
                organization=organization,
            ),
            id=appointment_id,
        )

        return _response(request, record)

    def patch(
        self,
        request,
        appointment_id,
    ):
        """Update an appointment through its workflow."""

        organization = organization_from_request(
            request,
        )

        serializer = AppointmentUpdateSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        result = AppointmentUpdateWorkflow(
            request=AppointmentUpdateRequest(
                organization_id=organization.id,
                appointment_id=appointment_id,
                data=dict(
                    serializer.validated_data,
                ),
                actor=request.user,
            ),
        ).execute(
            context=workflow_context(
                request,
                "appointment.update",
            ),
        )

        return _response(request, result)

    def delete(
        self,
        request,
        appointment_id,
    ):
        """Soft-delete an appointment through its workflow."""

        organization = organization_from_request(request)
        result = AppointmentDeleteWorkflow(
            request=AppointmentDeleteRequest(
                organization_id=organization.id,
                appointment_id=appointment_id,
                actor=request.user,
            ),
        ).execute(
            context=workflow_context(request, "appointment.delete"),
        )
        return _response(request, result)


class AppointmentDepositCheckoutView(APIView):
    """Create a Razorpay checkout order for the already-finalized RCM deposit invoice."""

    permission_classes = (IsAuthenticated, AppointmentAPIPermission)
    serializer_class = AppointmentDepositVerifySerializer

    def post(self, request, appointment_id):
        organization = organization_from_request(request)
        appointment = get_object_or_404(
            AppointmentSelector.queryset(organization=organization),
            id=appointment_id,
        )
        if appointment.deposit_paid:
            return error_response(
                message="The appointment deposit has already been paid.",
                status_code=status.HTTP_409_CONFLICT,
                request=request,
            )
        if not appointment.deposit_invoice_id:
            return error_response(
                message="No Revenue Cycle deposit invoice is linked to this appointment.",
                status_code=status.HTTP_409_CONFLICT,
                request=request,
            )
        invoice = get_object_or_404(
            HealthcareInvoice,
            pk=appointment.deposit_invoice_id,
            organization=organization,
        )
        try:
            existing = (
                HealthcarePayment.objects.filter(
                    organization=organization,
                    invoice=invoice,
                    status=HealthcarePayment.Status.PENDING,
                    gateway_order_id__gt="",
                )
                .order_by("-created_at")
                .first()
            )
            if existing:
                order_id = existing.gateway_order_id
                amount_paise = RazorpayGateway.amount_to_paise(existing.amount)
            else:
                gateway_order = RazorpayGateway().create_order(
                    amount=invoice.balance_due,
                    receipt=f"appt-{appointment.id.hex[:24]}",
                    notes={
                        "appointment_id": str(appointment.id),
                        "invoice_id": str(invoice.id),
                    },
                )
                order_id = str(gateway_order["id"])
                amount_paise = int(gateway_order["amount"])
                create_pending_payment(
                    organization=organization,
                    invoice=invoice,
                    amount=invoice.balance_due,
                    method=HealthcarePayment.Method.OTHER,
                    gateway_order_id=order_id,
                    actor=request.user,
                )
        except (RuntimeError, ValueError, KeyError) as exc:
            return error_response(
                message=str(exc),
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                request=request,
            )

        return success_response(
            data={
                "key_id": RAZORPAY_KEY_ID,
                "order_id": order_id,
                "amount": amount_paise,
                "currency": invoice.currency,
                "invoice_id": str(invoice.id),
            },
            request=request,
        )


class AppointmentDepositVerifyView(APIView):
    """Verify Razorpay signature and post the deposit into Revenue Cycle Billing."""

    permission_classes = (IsAuthenticated, AppointmentAPIPermission)
    serializer_class = AppointmentDepositVerifySerializer

    def post(self, request, appointment_id):
        organization = organization_from_request(request)
        appointment = get_object_or_404(
            AppointmentSelector.queryset(organization=organization),
            id=appointment_id,
        )
        serializer = AppointmentDepositVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        values = serializer.validated_data
        payment = get_object_or_404(
            HealthcarePayment,
            organization=organization,
            invoice_id=appointment.deposit_invoice_id,
            gateway_order_id=values["razorpay_order_id"],
        )
        try:
            RazorpayGateway.verify_payment_signature(
                order_id=values["razorpay_order_id"],
                payment_id=values["razorpay_payment_id"],
                signature=values["razorpay_signature"],
            )
            settle_pending_payment(
                organization=organization,
                payment=payment,
                gateway_payment_id=values["razorpay_payment_id"],
                method=HealthcarePayment.Method.OTHER,
                actor=request.user,
            )
        except (RuntimeError, ValueError, DjangoValidationError) as exc:
            raise ValidationError(str(exc)) from exc

        appointment.deposit_paid = True
        appointment.save(update_fields=["deposit_paid", "updated_at"])
        return _response(request, appointment)


class AppointmentConfirmView(APIView):
    """Confirm an appointment."""

    serializer_class = AppointmentSerializer
    workflow_name = "appointment.confirm"

    permission_classes = (IsAuthenticated, AppointmentAPIPermission)

    def post(
        self,
        request,
        appointment_id,
    ):
        """Confirm an appointment."""

        organization = organization_from_request(
            request,
        )

        result = AppointmentConfirmWorkflow(
            organization_id=organization.id,
            appointment_id=appointment_id,
            actor=request.user,
        ).execute(
            context=workflow_context(
                request,
                "appointment.confirm",
            ),
        )

        return _response(request, result)


class AppointmentRescheduleView(APIView):
    """Reschedule an appointment."""

    serializer_class = AppointmentRescheduleSerializer
    workflow_name = "appointment.reschedule"

    permission_classes = (IsAuthenticated, AppointmentAPIPermission)

    def post(
        self,
        request,
        appointment_id,
    ):
        """Reschedule an appointment."""

        organization = organization_from_request(
            request,
        )

        serializer = AppointmentRescheduleSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        result = AppointmentRescheduleWorkflow(
            request=AppointmentRescheduleRequest(
                organization_id=organization.id,
                appointment_id=appointment_id,
                scheduled_start=serializer.validated_data["scheduled_start"],
                scheduled_end=serializer.validated_data["scheduled_end"],
                duration_minutes=serializer.validated_data["duration_minutes"],
                actor=request.user,
            ),
        ).execute(
            context=workflow_context(
                request,
                "appointment.reschedule",
            ),
        )

        return _response(request, result)


class AppointmentCancelView(APIView):
    """Cancel an appointment."""

    serializer_class = AppointmentCancelSerializer
    workflow_name = "appointment.cancel"

    permission_classes = (IsAuthenticated, AppointmentAPIPermission)

    def post(
        self,
        request,
        appointment_id,
    ):
        """Cancel an appointment."""

        organization = organization_from_request(
            request,
        )

        serializer = AppointmentCancelSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        result = AppointmentCancelWorkflow(
            request=AppointmentCancelRequest(
                organization_id=organization.id,
                appointment_id=appointment_id,
                reason=serializer.validated_data["reason"],
                actor=request.user,
            ),
        ).execute(
            context=workflow_context(
                request,
                "appointment.cancel",
            ),
        )

        return _response(request, result)


class AppointmentCheckInView(APIView):
    """Check in an appointment."""

    serializer_class = AppointmentCheckInSerializer
    workflow_name = "appointment.check_in"

    permission_classes = (IsAuthenticated, AppointmentAPIPermission)

    def post(
        self,
        request,
        appointment_id,
    ):
        """Check in an appointment."""

        serializer = AppointmentCheckInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = organization_from_request(
            request,
        )

        result = AppointmentCheckInWorkflow(
            organization_id=organization.id,
            appointment_id=appointment_id,
            actor=request.user,
        ).execute(
            context=workflow_context(
                request,
                "appointment.check_in",
            ),
        )

        appointment = result.data
        session = None
        if serializer.validated_data["recording_consent"]:
            session = (
                LiveTranscriptionSession.objects.filter(
                    organization=organization,
                    appointment_id=appointment.id,
                )
                .order_by("-created_at")
                .first()
            )
            if session is None:
                session = LiveTranscriptionService.create_session(
                    organization=organization,
                    patient=appointment.patient,
                    created_by=request.user,
                    appointment=appointment,
                    audio_mime_type="audio/webm",
                    metadata={
                        "recording_consent": True,
                        "consented_at": timezone.now().isoformat(),
                        "consented_by": str(request.user.pk),
                    },
                )

        return success_response(
            data={
                "appointment": AppointmentSerializer(appointment).data,
                "transcription_session": (
                    {
                        "session_id": str(session.session_id),
                        "status": session.status,
                    }
                    if session
                    else None
                ),
            },
            request=request,
        )


class AppointmentStartView(APIView):
    """Start an appointment."""

    serializer_class = AppointmentSerializer
    workflow_name = "appointment.start"

    permission_classes = (IsAuthenticated, AppointmentAPIPermission)

    def post(
        self,
        request,
        appointment_id,
    ):
        """Start an appointment."""

        organization = organization_from_request(
            request,
        )

        result = AppointmentStartWorkflow(
            organization_id=organization.id,
            appointment_id=appointment_id,
            actor=request.user,
        ).execute(
            context=workflow_context(
                request,
                "appointment.start",
            ),
        )

        return _response(request, result)


class AppointmentCompleteView(APIView):
    """Complete an appointment."""

    serializer_class = AppointmentSerializer
    workflow_name = "appointment.complete"

    permission_classes = (IsAuthenticated, AppointmentAPIPermission)

    def post(
        self,
        request,
        appointment_id,
    ):
        """Complete an appointment."""

        organization = organization_from_request(
            request,
        )

        result = AppointmentCompleteWorkflow(
            organization_id=organization.id,
            appointment_id=appointment_id,
            actor=request.user,
        ).execute(
            context=workflow_context(
                request,
                "appointment.complete",
            ),
        )

        return _response(request, result)


class AppointmentNoShowView(APIView):
    """Record a missed visit after its scheduled end; the deposit remains non-refundable."""

    serializer_class = AppointmentSerializer
    workflow_name = "appointment.no_show"

    permission_classes = (IsAuthenticated, AppointmentAPIPermission)

    def post(self, request, appointment_id):
        organization = organization_from_request(request)
        result = AppointmentNoShowWorkflow(
            organization_id=organization.id,
            appointment_id=appointment_id,
            actor=request.user,
        ).execute(
            context=workflow_context(request, "appointment.no_show"),
        )
        return _response(request, result)


__all__ = (
    "AppointmentCancelView",
    "AppointmentCheckInView",
    "AppointmentCompleteView",
    "AppointmentConfirmView",
    "AppointmentDetailView",
    "AppointmentListCreateView",
    "AppointmentNoShowView",
    "AppointmentRescheduleView",
    "AppointmentStartView",
)
