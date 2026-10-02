"""Provider-scoped doctor workspace overview."""

from __future__ import annotations

from datetime import timedelta

from django.utils import timezone
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.clinical.appointments.models import Appointment
from apps.clinical.providers.models import Provider
from apps.common.api.responses import success_response
from apps.datavionos.selectors.bootstrap import platform_bootstrap_selector


class DoctorOverviewAPIView(APIView):
    """Return only the authenticated provider's operational workload."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        context = platform_bootstrap_selector.get(user=request.user)
        if context.employee is None or context.organization is None:
            raise NotFound("A provider workspace is not available for this user.")
        provider = Provider.objects.filter(
            employee=context.employee,
            organization=context.organization,
        ).first()
        if provider is None:
            raise PermissionDenied("An active provider profile is required.")

        now = timezone.now()
        day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        appointments = Appointment.objects.filter(provider=provider)
        today = appointments.filter(
            scheduled_start__gte=day_start, scheduled_start__lt=day_end
        )
        schedule = today.select_related("patient").order_by("scheduled_start")[:12]
        return success_response(
            request=request,
            data={
                "provider_id": str(provider.id),
                "today_appointments": today.count(),
                "my_patients": appointments.values("patient_id").distinct().count(),
                "upcoming_appointments": appointments.filter(
                    scheduled_start__gte=now
                ).count(),
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
                    for item in schedule
                ],
            },
        )


__all__ = ("DoctorOverviewAPIView",)
