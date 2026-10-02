"""Platform-administration operational overview API."""

from __future__ import annotations

from datetime import timedelta

from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework.views import APIView

from apps.common.api.responses import success_response
from apps.core.health.checks import application_health_checks
from apps.platform.accounts.models import User
from apps.platform.organizations.constants import OrganizationStatus
from apps.platform.organizations.models import Organization
from apps.platform.saas_billing.models import Invoice, Subscription
from apps.platform.tenancy.models import Tenant
from apps.platform.tenancy.permissions import IsPlatformAdmin


class PlatformOverviewAPIView(APIView):
    """Return authenticated, backend-derived control-plane metrics.

    This endpoint intentionally returns only aggregate operational data. It
    never exposes tenant patient or clinical records, and is restricted to the
    same platform-administrator boundary as the tenant directory.
    """

    permission_classes = (IsPlatformAdmin,)

    def get(self, request):
        now = timezone.now()
        month_start = now.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        previous_month_start = (month_start - timedelta(days=1)).replace(day=1)

        paid_invoices = Invoice.objects.filter(
            status=Invoice.Status.PAID,
            paid_at__gte=month_start,
            paid_at__lte=now,
        )
        revenue_by_currency = list(
            paid_invoices.values("currency")
            .annotate(
                amount=Sum("paid_amount"),
                invoice_count=Count("id"),
            )
            .order_by("currency")
        )

        previous_active_organizations = Organization.objects.filter(
            status=OrganizationStatus.ACTIVE,
            created_at__lt=month_start,
        ).count()
        active_organizations = Organization.objects.filter(
            status=OrganizationStatus.ACTIVE,
        ).count()
        organization_growth = (
            round(
                (
                    (active_organizations - previous_active_organizations)
                    / previous_active_organizations
                )
                * 100,
                1,
            )
            if previous_active_organizations
            else None
        )

        health = application_health_checks()
        recent_tenants = list(
            Tenant.objects.order_by("-created_at").values(
                "id",
                "name",
                "slug",
                "tenant_type",
                "status",
                "created_at",
            )[:8]
        )

        return success_response(
            request=request,
            data={
                "generated_at": now,
                "organizations": {
                    "total": Tenant.objects.count(),
                    "active": Tenant.objects.filter(status="active").count(),
                    "growth_percent": organization_growth,
                },
                "users": {
                    "total": User.objects.count(),
                    "active": User.objects.filter(is_active=True).count(),
                },
                "subscriptions": {
                    "active": Subscription.objects.filter(
                        status=Subscription.Status.ACTIVE,
                    ).count(),
                    "trial": Subscription.objects.filter(
                        status=Subscription.Status.TRIAL,
                    ).count(),
                    "past_due": Subscription.objects.filter(
                        status=Subscription.Status.PAST_DUE,
                    ).count(),
                },
                "revenue": {
                    "period_start": month_start,
                    "previous_period_start": previous_month_start,
                    "collected": [
                        {
                            "currency": entry["currency"],
                            "amount": str(entry["amount"] or 0),
                            "invoice_count": entry["invoice_count"],
                        }
                        for entry in revenue_by_currency
                    ],
                },
                "system": {
                    "healthy": health["healthy"],
                    "status": health["status"],
                    "checks": health["checks"],
                },
                "recent_organizations": recent_tenants,
            },
        )


__all__ = ("PlatformOverviewAPIView",)
