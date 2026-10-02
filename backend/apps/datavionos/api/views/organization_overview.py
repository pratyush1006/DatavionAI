"""Organization-scoped operational overview."""

from __future__ import annotations

from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.clinical.appointments.models import Appointment
from apps.common.api.responses import success_response
from apps.datavionos.selectors.bootstrap import platform_bootstrap_selector
from apps.patient_management.patients.models import Patient
from apps.platform.saas_billing.models import Invoice


class OrganizationOverviewAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        context = platform_bootstrap_selector.get(user=request.user)
        organization = context.organization
        if organization is None:
            from rest_framework.exceptions import NotFound

            raise NotFound("Active organization context was not found.")
        now = timezone.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        appointments = Appointment.objects.filter(organization=organization)
        today = appointments.filter(scheduled_start__gte=start, scheduled_start__lt=end)
        month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        revenue = (
            Invoice.objects.filter(
                organization=organization,
                status=Invoice.Status.PAID,
                paid_at__gte=month,
            ).aggregate(amount=Sum("paid_amount"))["amount"]
            or 0
        )
        return success_response(
            request=request,
            data={
                "patients": Patient.objects.filter(organization=organization).count(),
                "today_appointments": today.count(),
                "revenue": str(revenue),
                "schedule": [
                    {
                        "id": str(item.id),
                        "time": item.scheduled_start,
                        "patient_name": " ".join(
                            filter(
                                None, [item.patient.first_name, item.patient.last_name]
                            )
                        ),
                        "status": item.status,
                    }
                    for item in today.select_related("patient").order_by(
                        "scheduled_start"
                    )[:12]
                ],
            },
        )


__all__ = ("OrganizationOverviewAPIView",)
