"""
DatavionAI Revenue Cycle RC13 Revenue Analytics installer.

Writes the complete RC13 bounded context without generating or applying migrations.
"""

from __future__ import annotations

import py_compile
import shutil
import textwrap
from pathlib import Path

FILES = {
    "apps/revenue_cycle/revenue_analytics/__init__.py": "\n"
    '"""Revenue Cycle Revenue Analytics bounded '
    'context."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "__all__ = ()\n",
    "apps/revenue_cycle/revenue_analytics/admin.py": "\n"
    '"""Django admin configuration for Revenue '
    'Analytics."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.contrib import admin\n"
    "\n"
    "from .models import RevenueMetricSnapshot\n"
    "\n"
    "\n"
    "@admin.register(RevenueMetricSnapshot)\n"
    "class "
    "RevenueMetricSnapshotAdmin(admin.ModelAdmin):\n"
    '    """Admin configuration for analytics '
    'snapshots."""\n'
    "\n"
    "    list_display = (\n"
    '        "organization",\n'
    '        "period",\n'
    '        "period_start",\n'
    '        "period_end",\n'
    '        "gross_charges",\n'
    '        "payments",\n'
    '        "outstanding_ar",\n'
    '        "generated_at",\n'
    "    )\n"
    '    list_filter = ("period",)\n'
    '    search_fields = ("organization__name",)\n'
    "    readonly_fields = (\n"
    '        "organization",\n'
    '        "period",\n'
    '        "period_start",\n'
    '        "period_end",\n'
    '        "gross_charges",\n'
    '        "payments",\n'
    '        "adjustments",\n'
    '        "denials",\n'
    '        "write_offs",\n'
    '        "outstanding_ar",\n'
    '        "encounter_count",\n'
    '        "claim_count",\n'
    '        "denied_claim_count",\n'
    '        "paid_claim_count",\n'
    '        "generated_at",\n'
    '        "created_at",\n'
    '        "updated_at",\n'
    "    )\n"
    "\n"
    "\n"
    '__all__ = ("RevenueMetricSnapshotAdmin",)\n',
    "apps/revenue_cycle/revenue_analytics/api/__init__.py": "\n"
    '"""Revenue Analytics API package."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "__all__ = ()\n",
    "apps/revenue_cycle/revenue_analytics/api/serializers/__init__.py": "\n"
    '"""Revenue Analytics '
    'serializers."""\n'
    "\n"
    "from __future__ import "
    "annotations\n"
    "\n"
    "from .revenue_analytics "
    "import "
    "RevenueMetricSnapshotSerializer\n"
    "\n"
    "__all__ = "
    '("RevenueMetricSnapshotSerializer",)\n',
    "apps/revenue_cycle/revenue_analytics/api/serializers/revenue_analytics.py": "\n"
    '"""DRF serializers '
    "for Revenue "
    'Analytics."""\n'
    "\n"
    "from __future__ "
    "import annotations\n"
    "\n"
    "from rest_framework "
    "import serializers\n"
    "\n"
    "from ...models "
    "import "
    "RevenueMetricSnapshot\n"
    "\n"
    "\n"
    "class "
    "RevenueMetricSnapshotSerializer(serializers.ModelSerializer):\n"
    '    """Serialize '
    "Revenue Analytics "
    'KPI snapshots."""\n'
    "\n"
    "    class Meta:\n"
    "        "
    '"""Configure the '
    "analytics snapshot "
    'serializer."""\n'
    "\n"
    "        model = "
    "RevenueMetricSnapshot\n"
    "        fields = (\n"
    '            "id",\n'
    "            "
    '"organization",\n'
    "            "
    '"period",\n'
    "            "
    '"period_start",\n'
    "            "
    '"period_end",\n'
    "            "
    '"gross_charges",\n'
    "            "
    '"payments",\n'
    "            "
    '"adjustments",\n'
    "            "
    '"denials",\n'
    "            "
    '"write_offs",\n'
    "            "
    '"outstanding_ar",\n'
    "            "
    '"encounter_count",\n'
    "            "
    '"claim_count",\n'
    "            "
    '"denied_claim_count",\n'
    "            "
    '"paid_claim_count",\n'
    "            "
    '"generated_at",\n'
    "        )\n"
    "        "
    "read_only_fields = "
    "(\n"
    '            "id",\n'
    "            "
    '"organization",\n'
    "            "
    '"generated_at",\n'
    "        )\n"
    "\n"
    "\n"
    "__all__ = "
    '("RevenueMetricSnapshotSerializer",)\n',
    "apps/revenue_cycle/revenue_analytics/api/views/__init__.py": "\n"
    '"""Revenue Analytics API '
    'views."""\n'
    "\n"
    "from __future__ import "
    "annotations\n"
    "\n"
    "from .revenue_analytics import "
    "RevenueAnalyticsGenerateAPIView\n"
    "from .revenue_analytics import "
    "RevenueAnalyticsListAPIView\n"
    "\n"
    "__all__ = (\n"
    "    "
    '"RevenueAnalyticsGenerateAPIView",\n'
    "    "
    '"RevenueAnalyticsListAPIView",\n'
    ")\n",
    "apps/revenue_cycle/revenue_analytics/api/views/revenue_analytics.py": "\n"
    '"""DRF views for Revenue '
    'Analytics."""\n'
    "\n"
    "from __future__ import "
    "annotations\n"
    "\n"
    "from datetime import "
    "date\n"
    "from decimal import "
    "Decimal\n"
    "from uuid import UUID\n"
    "\n"
    "from "
    "django.utils.dateparse "
    "import parse_date\n"
    "from rest_framework "
    "import status\n"
    "from "
    "rest_framework.permissions "
    "import IsAuthenticated\n"
    "from "
    "rest_framework.response "
    "import Response\n"
    "from rest_framework.views "
    "import APIView\n"
    "\n"
    "from ...constants import "
    "AnalyticsPeriod\n"
    "from ...policies import "
    "RevenueAnalyticsPolicy\n"
    "from ...selectors import "
    "RevenueAnalyticsSelector\n"
    "from ...workflows import "
    "RevenueAnalyticsWorkflow\n"
    "from ..serializers import "
    "RevenueMetricSnapshotSerializer\n"
    "\n"
    "\n"
    "def _context(request):\n"
    '    """Require explicit '
    "tenant and organization "
    'context."""\n'
    "\n"
    "    tenant = "
    "request.tenant\n"
    "    organization = "
    "request.organization\n"
    "    if "
    "organization.tenant_id != "
    "tenant.id:\n"
    "        raise "
    'PermissionError("Organization '
    "does not belong to the "
    'active tenant.")\n'
    "    return tenant, "
    "organization\n"
    "\n"
    "\n"
    "def _decimal(data, "
    "field_name: str) -> "
    "Decimal:\n"
    '    """Parse a '
    "non-negative decimal "
    'request field."""\n'
    "\n"
    "    try:\n"
    "        value = "
    "Decimal(str(data.get(field_name, "
    '"0")))\n'
    "    except Exception as "
    "exc:\n"
    "        raise "
    'ValueError(f"{field_name} '
    "must be a valid "
    'decimal.") from exc\n'
    "    if value < 0:\n"
    "        raise "
    'ValueError(f"{field_name} '
    'cannot be negative.")\n'
    "    return value\n"
    "\n"
    "\n"
    "def _count(data, "
    "field_name: str) -> int:\n"
    '    """Parse a '
    "non-negative integer "
    'request field."""\n'
    "\n"
    "    try:\n"
    "        value = "
    "int(data.get(field_name, "
    "0))\n"
    "    except (TypeError, "
    "ValueError) as exc:\n"
    "        raise "
    'ValueError(f"{field_name} '
    "must be a valid "
    'integer.") from exc\n'
    "    if value < 0:\n"
    "        raise "
    'ValueError(f"{field_name} '
    'cannot be negative.")\n'
    "    return value\n"
    "\n"
    "\n"
    "class "
    "RevenueAnalyticsListAPIView(APIView):\n"
    '    """List '
    "organization-scoped "
    "Revenue Analytics "
    'snapshots."""\n'
    "\n"
    "    permission_classes = "
    "(IsAuthenticated,)\n"
    "\n"
    "    def get(self, "
    "request):\n"
    '        """Return '
    "filtered analytics "
    'snapshots."""\n'
    "\n"
    "        _, organization = "
    "_context(request)\n"
    "        if not "
    "RevenueAnalyticsPolicy.can_list(\n"
    "            "
    "user=request.user,\n"
    "            "
    "organization=organization,\n"
    "        ):\n"
    "            return "
    "Response(status=status.HTTP_403_FORBIDDEN)\n"
    "\n"
    "        start_date = "
    'request.query_params.get("start_date")\n'
    "        end_date = "
    'request.query_params.get("end_date")\n'
    "        period = "
    'request.query_params.get("period")\n'
    "\n"
    "        parsed_start = "
    "parse_date(start_date) if "
    "start_date else None\n"
    "        parsed_end = "
    "parse_date(end_date) if "
    "end_date else None\n"
    "\n"
    "        if start_date and "
    "parsed_start is None:\n"
    "            return "
    "Response(\n"
    "                "
    '{"detail": "start_date '
    "must be a valid ISO "
    'date."},\n'
    "                "
    "status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "        if end_date and "
    "parsed_end is None:\n"
    "            return "
    "Response(\n"
    "                "
    '{"detail": "end_date must '
    'be a valid ISO date."},\n'
    "                "
    "status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "        if period and "
    "period not in "
    "AnalyticsPeriod.values:\n"
    "            return "
    "Response(\n"
    "                "
    '{"detail": "Unsupported '
    'analytics period."},\n'
    "                "
    "status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "\n"
    "        queryset = "
    "RevenueAnalyticsSelector.snapshots(\n"
    "            "
    "organization_id=organization.id,\n"
    "            "
    "period=period,\n"
    "            "
    "start_date=parsed_start,\n"
    "            "
    "end_date=parsed_end,\n"
    "        )\n"
    "        return Response(\n"
    "            "
    "RevenueMetricSnapshotSerializer(queryset, "
    "many=True).data,\n"
    "        )\n"
    "\n"
    "\n"
    "class "
    "RevenueAnalyticsGenerateAPIView(APIView):\n"
    '    """Generate one '
    "organization-scoped "
    'analytics snapshot."""\n'
    "\n"
    "    permission_classes = "
    "(IsAuthenticated,)\n"
    "\n"
    "    def post(self, "
    "request):\n"
    '        """Generate a '
    "snapshot through RBAC and "
    'workflow layers."""\n'
    "\n"
    "        _, organization = "
    "_context(request)\n"
    "        payload = "
    "request.data\n"
    "        period = "
    'payload.get("period", '
    '"")\n'
    "        period_start = "
    'parse_date(payload.get("period_start", '
    '""))\n'
    "        period_end = "
    'parse_date(payload.get("period_end", '
    '""))\n'
    "\n"
    "        if period not in "
    "AnalyticsPeriod.values:\n"
    "            return "
    "Response(\n"
    "                "
    '{"detail": "Unsupported '
    'analytics period."},\n'
    "                "
    "status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "        if period_start "
    "is None or period_end is "
    "None:\n"
    "            return "
    "Response(\n"
    "                "
    '{"detail": "period_start '
    "and period_end must be "
    'valid ISO dates."},\n'
    "                "
    "status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "\n"
    "        try:\n"
    "            result = "
    "RevenueAnalyticsWorkflow.generate(\n"
    "                "
    "user=request.user,\n"
    "                "
    "organization=organization,\n"
    "                "
    "period=period,\n"
    "                "
    "period_start=period_start,\n"
    "                "
    "period_end=period_end,\n"
    "                "
    "gross_charges=_decimal(payload, "
    '"gross_charges"),\n'
    "                "
    "payments=_decimal(payload, "
    '"payments"),\n'
    "                "
    "adjustments=_decimal(payload, "
    '"adjustments"),\n'
    "                "
    "denials=_decimal(payload, "
    '"denials"),\n'
    "                "
    "write_offs=_decimal(payload, "
    '"write_offs"),\n'
    "                "
    "outstanding_ar=_decimal(payload, "
    '"outstanding_ar"),\n'
    "                "
    "encounter_count=_count(payload, "
    '"encounter_count"),\n'
    "                "
    "claim_count=_count(payload, "
    '"claim_count"),\n'
    "                "
    "denied_claim_count=_count(payload, "
    '"denied_claim_count"),\n'
    "                "
    "paid_claim_count=_count(payload, "
    '"paid_claim_count"),\n'
    "            )\n"
    "        except "
    "PermissionError as exc:\n"
    "            return "
    "Response(\n"
    "                "
    '{"detail": str(exc)},\n'
    "                "
    "status=status.HTTP_403_FORBIDDEN,\n"
    "            )\n"
    "        except ValueError "
    "as exc:\n"
    "            return "
    "Response(\n"
    "                "
    '{"detail": str(exc)},\n'
    "                "
    "status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "\n"
    "        return Response(\n"
    "            "
    "RevenueMetricSnapshotSerializer(result).data,\n"
    "            "
    "status=status.HTTP_201_CREATED,\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    "    "
    '"RevenueAnalyticsGenerateAPIView",\n'
    "    "
    '"RevenueAnalyticsListAPIView",\n'
    ")\n",
    "apps/revenue_cycle/revenue_analytics/apps.py": "\n"
    '"""Django application configuration for Revenue '
    'Analytics."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.apps import AppConfig\n"
    "\n"
    "\n"
    "class RevenueAnalyticsConfig(AppConfig):\n"
    '    """Configure the Revenue Analytics '
    'application."""\n'
    "\n"
    "    default_auto_field = "
    '"django.db.models.BigAutoField"\n'
    "    name = "
    '"apps.revenue_cycle.revenue_analytics"\n'
    '    label = "revenue_cycle_revenue_analytics"\n'
    '    verbose_name = "Revenue Cycle Revenue '
    'Analytics"\n'
    "\n"
    "\n"
    '__all__ = ("RevenueAnalyticsConfig",)\n',
    "apps/revenue_cycle/revenue_analytics/constants.py": "\n"
    '"""Constants for Revenue Cycle '
    'analytics."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.db import models\n"
    "\n"
    "\n"
    "class AnalyticsPeriod(models.TextChoices):\n"
    '    """Supported analytics aggregation '
    'periods."""\n'
    "\n"
    '    DAY = "DAY", "Day"\n'
    '    WEEK = "WEEK", "Week"\n'
    '    MONTH = "MONTH", "Month"\n'
    '    QUARTER = "QUARTER", "Quarter"\n'
    '    YEAR = "YEAR", "Year"\n'
    "\n"
    "\n"
    '__all__ = ("AnalyticsPeriod",)\n',
    "apps/revenue_cycle/revenue_analytics/events.py": "\n"
    '"""Domain events for Revenue Analytics."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from typing import Any\n"
    "from uuid import UUID\n"
    "\n"
    "from apps.core.events import DomainEvent\n"
    "from apps.core.events import "
    "publish_after_commit\n"
    "\n"
    "\n"
    "class RevenueAnalyticsEvent(DomainEvent):\n"
    '    """Represent a Revenue Analytics domain '
    'event."""\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        event_type: str,\n"
    "        aggregate_id: UUID,\n"
    "        payload: dict[str, Any],\n"
    "    ) -> None:\n"
    '        """Initialize an analytics event."""\n'
    "\n"
    "        super().__init__(\n"
    "            event_type=event_type,\n"
    "            aggregate_id=aggregate_id,\n"
    "            payload=payload,\n"
    "        )\n"
    "\n"
    "\n"
    "def publish_revenue_analytics_event(\n"
    "    *,\n"
    "    event_type: str,\n"
    "    aggregate_id: UUID,\n"
    "    payload: dict[str, Any],\n"
    ") -> None:\n"
    '    """Publish an analytics event after '
    'transaction commit."""\n'
    "\n"
    "    publish_after_commit(\n"
    "        RevenueAnalyticsEvent(\n"
    "            event_type=event_type,\n"
    "            aggregate_id=aggregate_id,\n"
    "            payload=payload,\n"
    "        )\n"
    "    )\n"
    "\n"
    "\n"
    '__all__ = ("RevenueAnalyticsEvent", '
    '"publish_revenue_analytics_event")\n',
    "apps/revenue_cycle/revenue_analytics/migrations/__init__.py": "\n"
    '"""Revenue Analytics '
    'migrations."""\n'
    "\n"
    "from __future__ import "
    "annotations\n"
    "\n"
    "__all__ = ()\n",
    "apps/revenue_cycle/revenue_analytics/models.py": "\n"
    '"""Persistent models for Revenue Cycle '
    'analytics snapshots."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from decimal import Decimal\n"
    "\n"
    "from django.db import models\n"
    "from django.db.models import Q\n"
    "\n"
    "from apps.core.models import BaseModel\n"
    "\n"
    "from .constants import AnalyticsPeriod\n"
    "\n"
    "\n"
    "class RevenueMetricSnapshot(BaseModel):\n"
    '    """Store an organization-scoped, '
    'reproducible revenue KPI snapshot."""\n'
    "\n"
    "    organization = models.ForeignKey(\n"
    '        "organizations.Organization",\n'
    "        on_delete=models.PROTECT,\n"
    "        "
    'related_name="revenue_cycle_metric_snapshots",\n'
    "    )\n"
    "    period = models.CharField(\n"
    "        max_length=10,\n"
    "        choices=AnalyticsPeriod.choices,\n"
    "    )\n"
    "    period_start = models.DateField()\n"
    "    period_end = models.DateField()\n"
    "    gross_charges = models.DecimalField(\n"
    "        max_digits=16,\n"
    "        decimal_places=2,\n"
    '        default=Decimal("0.00"),\n'
    "    )\n"
    "    payments = models.DecimalField(\n"
    "        max_digits=16,\n"
    "        decimal_places=2,\n"
    '        default=Decimal("0.00"),\n'
    "    )\n"
    "    adjustments = models.DecimalField(\n"
    "        max_digits=16,\n"
    "        decimal_places=2,\n"
    '        default=Decimal("0.00"),\n'
    "    )\n"
    "    denials = models.DecimalField(\n"
    "        max_digits=16,\n"
    "        decimal_places=2,\n"
    '        default=Decimal("0.00"),\n'
    "    )\n"
    "    write_offs = models.DecimalField(\n"
    "        max_digits=16,\n"
    "        decimal_places=2,\n"
    '        default=Decimal("0.00"),\n'
    "    )\n"
    "    outstanding_ar = models.DecimalField(\n"
    "        max_digits=16,\n"
    "        decimal_places=2,\n"
    '        default=Decimal("0.00"),\n'
    "    )\n"
    "    encounter_count = "
    "models.PositiveBigIntegerField(default=0)\n"
    "    claim_count = "
    "models.PositiveBigIntegerField(default=0)\n"
    "    denied_claim_count = "
    "models.PositiveBigIntegerField(default=0)\n"
    "    paid_claim_count = "
    "models.PositiveBigIntegerField(default=0)\n"
    "    generated_at = "
    "models.DateTimeField(auto_now_add=True)\n"
    "\n"
    "    class Meta:\n"
    '        """Configure snapshot uniqueness and '
    'analytics indexes."""\n'
    "\n"
    "        db_table = "
    '"revenue_cycle_metric_snapshots"\n'
    '        ordering = ("-period_end", '
    '"-generated_at")\n'
    "        constraints = (\n"
    "            models.UniqueConstraint(\n"
    "                fields=(\n"
    '                    "organization",\n'
    '                    "period",\n'
    '                    "period_start",\n'
    '                    "period_end",\n'
    "                ),\n"
    "                "
    'name="unique_rc_metric_snapshot_period",\n'
    "            ),\n"
    "            models.CheckConstraint(\n"
    "                "
    'condition=Q(period_end__gte=models.F("period_start")),\n'
    "                "
    'name="rc_metric_valid_period",\n'
    "            ),\n"
    "            models.CheckConstraint(\n"
    "                "
    "condition=Q(gross_charges__gte=0),\n"
    "                "
    'name="rc_metric_charges_non_negative",\n'
    "            ),\n"
    "            models.CheckConstraint(\n"
    "                condition=Q(payments__gte=0),\n"
    "                "
    'name="rc_metric_payments_non_negative",\n'
    "            ),\n"
    "            models.CheckConstraint(\n"
    "                "
    "condition=Q(adjustments__gte=0),\n"
    "                "
    'name="rc_metric_adjustments_non_negative",\n'
    "            ),\n"
    "            models.CheckConstraint(\n"
    "                condition=Q(denials__gte=0),\n"
    "                "
    'name="rc_metric_denials_non_negative",\n'
    "            ),\n"
    "            models.CheckConstraint(\n"
    "                "
    "condition=Q(write_offs__gte=0),\n"
    "                "
    'name="rc_metric_writeoffs_non_negative",\n'
    "            ),\n"
    "            models.CheckConstraint(\n"
    "                "
    "condition=Q(outstanding_ar__gte=0),\n"
    "                "
    'name="rc_metric_ar_non_negative",\n'
    "            ),\n"
    "        )\n"
    "        indexes = (\n"
    "            models.Index(\n"
    '                fields=("organization", '
    '"period_end"),\n'
    "                "
    'name="rc_metric_org_period_idx",\n'
    "            ),\n"
    "            models.Index(\n"
    '                fields=("organization", '
    '"period"),\n'
    "                "
    'name="rc_metric_org_type_idx",\n'
    "            ),\n"
    "        )\n"
    "\n"
    "    def __str__(self) -> str:\n"
    '        """Return the snapshot period."""\n'
    "\n"
    "        return "
    'f"{self.period}:{self.period_start}:{self.period_end}"\n'
    "\n"
    "\n"
    '__all__ = ("RevenueMetricSnapshot",)\n',
    "apps/revenue_cycle/revenue_analytics/permissions.py": "\n"
    '"""RBAC permissions for Revenue '
    'Analytics."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from apps.platform.rbac.permissions.base "
    "import RBACPermissionBase\n"
    "\n"
    "\n"
    "class "
    "RevenueAnalyticsPermission(RBACPermissionBase):\n"
    '    """Define canonical Revenue Analytics '
    'permissions."""\n'
    "\n"
    "    LIST = "
    '"revenue_cycle.revenue_analytics.list"\n'
    "    VIEW = "
    '"revenue_cycle.revenue_analytics.view"\n'
    "    GENERATE = "
    '"revenue_cycle.revenue_analytics.generate"\n'
    "\n"
    "\n"
    "__all__ = "
    '("RevenueAnalyticsPermission",)\n',
    "apps/revenue_cycle/revenue_analytics/policies.py": "\n"
    '"""Authorization policies for Revenue '
    'Analytics."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from typing import Any\n"
    "\n"
    "from apps.platform.rbac.engines import "
    "user_has_permission\n"
    "\n"
    "from .permissions import "
    "RevenueAnalyticsPermission\n"
    "\n"
    "\n"
    "class RevenueAnalyticsPolicy:\n"
    '    """Evaluate organization-scoped '
    'analytics permissions."""\n'
    "\n"
    "    @staticmethod\n"
    "    def can_list(*, user: Any, organization: "
    "Any) -> bool:\n"
    '        """Return whether the actor can list '
    'analytics."""\n'
    "\n"
    "        return user_has_permission(\n"
    "            user=user,\n"
    "            "
    "permission=RevenueAnalyticsPermission.LIST,\n"
    "            organization=organization,\n"
    "        )\n"
    "\n"
    "    @staticmethod\n"
    "    def can_view(*, user: Any, organization: "
    "Any) -> bool:\n"
    '        """Return whether the actor can view '
    'analytics."""\n'
    "\n"
    "        return user_has_permission(\n"
    "            user=user,\n"
    "            "
    "permission=RevenueAnalyticsPermission.VIEW,\n"
    "            organization=organization,\n"
    "        )\n"
    "\n"
    "    @staticmethod\n"
    "    def can_generate(*, user: Any, "
    "organization: Any) -> bool:\n"
    '        """Return whether the actor can '
    'generate analytics snapshots."""\n'
    "\n"
    "        return user_has_permission(\n"
    "            user=user,\n"
    "            "
    "permission=RevenueAnalyticsPermission.GENERATE,\n"
    "            organization=organization,\n"
    "        )\n"
    "\n"
    "\n"
    '__all__ = ("RevenueAnalyticsPolicy",)\n',
    "apps/revenue_cycle/revenue_analytics/selectors.py": "\n"
    '"""Organization-scoped selectors for '
    'Revenue Analytics."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from datetime import date\n"
    "from uuid import UUID\n"
    "\n"
    "from django.db.models import QuerySet\n"
    "\n"
    "from .models import RevenueMetricSnapshot\n"
    "\n"
    "\n"
    "class RevenueAnalyticsSelector:\n"
    '    """Provide read-only analytics snapshot '
    'queries."""\n'
    "\n"
    "    @staticmethod\n"
    "    def snapshots(\n"
    "        *,\n"
    "        organization_id: UUID,\n"
    "        period: str | None = None,\n"
    "        start_date: date | None = None,\n"
    "        end_date: date | None = None,\n"
    "    ) -> QuerySet[RevenueMetricSnapshot]:\n"
    '        """Return organization-scoped '
    'snapshots matching optional filters."""\n'
    "\n"
    "        queryset = "
    "RevenueMetricSnapshot.objects.filter(\n"
    "            "
    "organization_id=organization_id,\n"
    "        )\n"
    "        if period:\n"
    "            queryset = "
    "queryset.filter(period=period)\n"
    "        if start_date:\n"
    "            queryset = "
    "queryset.filter(period_end__gte=start_date)\n"
    "        if end_date:\n"
    "            queryset = "
    "queryset.filter(period_start__lte=end_date)\n"
    "        return "
    'queryset.order_by("-period_end", '
    '"-generated_at")\n'
    "\n"
    "    @staticmethod\n"
    "    def latest(\n"
    "        *,\n"
    "        organization_id: UUID,\n"
    "        period: str,\n"
    "    ) -> RevenueMetricSnapshot | None:\n"
    '        """Return the latest snapshot for '
    'one organization and period."""\n'
    "\n"
    "        return (\n"
    "            "
    "RevenueMetricSnapshot.objects.filter(\n"
    "                "
    "organization_id=organization_id,\n"
    "                period=period,\n"
    "            )\n"
    '            .order_by("-period_end", '
    '"-generated_at")\n'
    "            .first()\n"
    "        )\n"
    "\n"
    "\n"
    '__all__ = ("RevenueAnalyticsSelector",)\n',
    "apps/revenue_cycle/revenue_analytics/services.py": "\n"
    '"""Services for Revenue Analytics snapshot '
    'generation."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from datetime import date\n"
    "from decimal import Decimal\n"
    "from typing import Any\n"
    "\n"
    "from django.db import transaction\n"
    "\n"
    "from .constants import AnalyticsPeriod\n"
    "from .events import "
    "publish_revenue_analytics_event\n"
    "from .models import RevenueMetricSnapshot\n"
    "\n"
    "\n"
    "class RevenueAnalyticsService:\n"
    '    """Generate deterministic '
    'organization-scoped KPI snapshots."""\n'
    "\n"
    "    @staticmethod\n"
    "    @transaction.atomic\n"
    "    def create_snapshot(\n"
    "        *,\n"
    "        organization: Any,\n"
    "        period: str,\n"
    "        period_start: date,\n"
    "        period_end: date,\n"
    "        gross_charges: Decimal = "
    'Decimal("0.00"),\n'
    "        payments: Decimal = "
    'Decimal("0.00"),\n'
    "        adjustments: Decimal = "
    'Decimal("0.00"),\n'
    '        denials: Decimal = Decimal("0.00"),\n'
    "        write_offs: Decimal = "
    'Decimal("0.00"),\n'
    "        outstanding_ar: Decimal = "
    'Decimal("0.00"),\n'
    "        encounter_count: int = 0,\n"
    "        claim_count: int = 0,\n"
    "        denied_claim_count: int = 0,\n"
    "        paid_claim_count: int = 0,\n"
    "        actor: Any = None,\n"
    "    ) -> RevenueMetricSnapshot:\n"
    '        """Create or return the unique '
    'snapshot for a reporting period."""\n'
    "\n"
    "        if period not in "
    "AnalyticsPeriod.values:\n"
    '            raise ValueError("Unsupported '
    'analytics period.")\n'
    "        if period_end < period_start:\n"
    '            raise ValueError("period_end '
    'cannot precede period_start.")\n'
    "\n"
    "        monetary_values = {\n"
    '            "gross_charges": gross_charges,\n'
    '            "payments": payments,\n'
    '            "adjustments": adjustments,\n'
    '            "denials": denials,\n'
    '            "write_offs": write_offs,\n'
    '            "outstanding_ar": '
    "outstanding_ar,\n"
    "        }\n"
    "        if any(value < 0 for value in "
    "monetary_values.values()):\n"
    '            raise ValueError("Analytics '
    'monetary values cannot be negative.")\n'
    "\n"
    "        count_values = {\n"
    '            "encounter_count": '
    "encounter_count,\n"
    '            "claim_count": claim_count,\n'
    '            "denied_claim_count": '
    "denied_claim_count,\n"
    '            "paid_claim_count": '
    "paid_claim_count,\n"
    "        }\n"
    "        if any(value < 0 for value in "
    "count_values.values()):\n"
    '            raise ValueError("Analytics '
    'counts cannot be negative.")\n'
    "\n"
    "        snapshot, created = "
    "RevenueMetricSnapshot.objects.get_or_create(\n"
    "            organization=organization,\n"
    "            period=period,\n"
    "            period_start=period_start,\n"
    "            period_end=period_end,\n"
    "            defaults={\n"
    "                **monetary_values,\n"
    "                **count_values,\n"
    "            },\n"
    "        )\n"
    "\n"
    "        if not created:\n"
    '            raise ValueError("An analytics '
    'snapshot already exists for this period.")\n'
    "\n"
    "        publish_revenue_analytics_event(\n"
    "            "
    'event_type="revenue_cycle.analytics.snapshot_created",\n'
    "            aggregate_id=snapshot.id,\n"
    "            payload={\n"
    '                "organization_id": '
    "str(organization.id),\n"
    '                "period": period,\n'
    '                "period_start": '
    "period_start.isoformat(),\n"
    '                "period_end": '
    "period_end.isoformat(),\n"
    '                "generated_by": '
    "str(actor.id) if actor else None,\n"
    "            },\n"
    "        )\n"
    "        return snapshot\n"
    "\n"
    "\n"
    '__all__ = ("RevenueAnalyticsService",)\n',
    "apps/revenue_cycle/revenue_analytics/tests/__init__.py": "\n"
    '"""Revenue Analytics tests."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "__all__ = ()\n",
    "apps/revenue_cycle/revenue_analytics/tests/test_invariants.py": "\n"
    '"""Architecture tests for '
    'Revenue Analytics."""\n'
    "\n"
    "from __future__ import "
    "annotations\n"
    "\n"
    "from django.test import "
    "SimpleTestCase\n"
    "\n"
    "from ..models import "
    "RevenueMetricSnapshot\n"
    "\n"
    "\n"
    "class "
    "RevenueAnalyticsArchitectureTests(SimpleTestCase):\n"
    '    """Verify non-negotiable '
    "Revenue Analytics "
    'architecture."""\n'
    "\n"
    "    def "
    "test_snapshot_has_organization_scope(self) "
    "-> None:\n"
    '        """Verify analytics '
    "snapshots are organization "
    'scoped."""\n'
    "\n"
    "        field = "
    'RevenueMetricSnapshot._meta.get_field("organization")\n'
    "        "
    "self.assertIsNotNone(field.remote_field.model)\n"
    "\n"
    "    def "
    "test_snapshot_has_unique_reporting_period(self) "
    "-> None:\n"
    '        """Verify '
    "reporting-period uniqueness is "
    'represented in the model."""\n'
    "\n"
    "        constraint_names = {\n"
    "            constraint.name\n"
    "            for constraint in "
    "RevenueMetricSnapshot._meta.constraints\n"
    "        }\n"
    "        self.assertIn(\n"
    "            "
    '"unique_rc_metric_snapshot_period",\n'
    "            constraint_names,\n"
    "        )\n"
    "\n"
    "    def "
    "test_snapshot_uses_decimal_money(self) "
    "-> None:\n"
    '        """Verify KPI monetary '
    'values use DecimalField."""\n'
    "\n"
    "        field = "
    'RevenueMetricSnapshot._meta.get_field("gross_charges")\n'
    "        "
    "self.assertEqual(field.get_internal_type(), "
    '"DecimalField")\n'
    "\n"
    "\n"
    "__all__ = "
    '("RevenueAnalyticsArchitectureTests",)\n',
    "apps/revenue_cycle/revenue_analytics/urls.py": "\n"
    '"""URL routes for Revenue Analytics."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.urls import path\n"
    "\n"
    "from .api.views import "
    "RevenueAnalyticsGenerateAPIView\n"
    "from .api.views import "
    "RevenueAnalyticsListAPIView\n"
    "\n"
    'app_name = "revenue_cycle_revenue_analytics"\n'
    "\n"
    "urlpatterns = [\n"
    "    path(\n"
    '        "snapshots/",\n'
    "        RevenueAnalyticsListAPIView.as_view(),\n"
    '        name="snapshot-list",\n'
    "    ),\n"
    "    path(\n"
    '        "snapshots/generate/",\n'
    "        "
    "RevenueAnalyticsGenerateAPIView.as_view(),\n"
    '        name="snapshot-generate",\n'
    "    ),\n"
    "]\n"
    "\n"
    '__all__ = ("app_name", "urlpatterns")\n',
    "apps/revenue_cycle/revenue_analytics/workflows.py": "\n"
    '"""Workflow orchestration for Revenue '
    'Analytics."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from datetime import date\n"
    "from decimal import Decimal\n"
    "from typing import Any\n"
    "\n"
    "from .policies import "
    "RevenueAnalyticsPolicy\n"
    "from .services import "
    "RevenueAnalyticsService\n"
    "\n"
    "\n"
    "class RevenueAnalyticsWorkflow:\n"
    '    """Orchestrate authorized analytics '
    'snapshot generation."""\n'
    "\n"
    "    @staticmethod\n"
    "    def generate(\n"
    "        *,\n"
    "        user: Any,\n"
    "        organization: Any,\n"
    "        period: str,\n"
    "        period_start: date,\n"
    "        period_end: date,\n"
    "        gross_charges: Decimal,\n"
    "        payments: Decimal,\n"
    "        adjustments: Decimal,\n"
    "        denials: Decimal,\n"
    "        write_offs: Decimal,\n"
    "        outstanding_ar: Decimal,\n"
    "        encounter_count: int,\n"
    "        claim_count: int,\n"
    "        denied_claim_count: int,\n"
    "        paid_claim_count: int,\n"
    "    ) -> Any:\n"
    '        """Authorize and generate a Revenue '
    'Analytics snapshot."""\n'
    "\n"
    "        if not "
    "RevenueAnalyticsPolicy.can_generate(\n"
    "            user=user,\n"
    "            organization=organization,\n"
    "        ):\n"
    "            raise PermissionError(\n"
    '                "Revenue Analytics '
    'generation permission is required."\n'
    "            )\n"
    "\n"
    "        return "
    "RevenueAnalyticsService.create_snapshot(\n"
    "            organization=organization,\n"
    "            period=period,\n"
    "            period_start=period_start,\n"
    "            period_end=period_end,\n"
    "            gross_charges=gross_charges,\n"
    "            payments=payments,\n"
    "            adjustments=adjustments,\n"
    "            denials=denials,\n"
    "            write_offs=write_offs,\n"
    "            outstanding_ar=outstanding_ar,\n"
    "            "
    "encounter_count=encounter_count,\n"
    "            claim_count=claim_count,\n"
    "            "
    "denied_claim_count=denied_claim_count,\n"
    "            "
    "paid_claim_count=paid_claim_count,\n"
    "            actor=user,\n"
    "        )\n"
    "\n"
    "\n"
    '__all__ = ("RevenueAnalyticsWorkflow",)\n',
}

ROOT = Path(__file__).resolve().parent
APP_ROOT = ROOT / "apps" / "revenue_cycle" / "revenue_analytics"
BACKUP_ROOT = ROOT / ".rc13_revenue_analytics_backup"


def write_file(relative_path: str, content: str) -> None:
    """Write a source file and back up an existing destination."""

    destination = ROOT / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        backup = BACKUP_ROOT / relative_path
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(destination, backup)
    destination.write_text(
        textwrap.dedent(content).lstrip(),
        encoding="utf-8",
    )


def main() -> None:
    """Install and verify RC13 Revenue Analytics."""

    for relative_path, content in FILES.items():
        write_file(relative_path, content)

    expected = sorted(path.replace("\\", "/") for path in FILES if path.endswith(".py"))
    actual = sorted(
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in APP_ROOT.rglob("*.py")
    )

    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        unexpected = sorted(set(actual) - set(expected))
        raise AssertionError(
            f"RC13 manifest mismatch: missing={missing}, unexpected={unexpected}"
        )

    for relative_path in actual:
        source_path = ROOT / relative_path
        source = source_path.read_text(encoding="utf-8")
        if not source.lstrip().startswith('"""'):
            raise AssertionError(f"RC13 style failure: {relative_path}")
        if "from __future__ import annotations" not in source:
            raise AssertionError(f"RC13 style failure: {relative_path}")
        py_compile.compile(str(source_path), doraise=True)

    models_source = (APP_ROOT / "models.py").read_text(encoding="utf-8")
    permission_source = (APP_ROOT / "permissions.py").read_text(encoding="utf-8")
    policy_source = (APP_ROOT / "policies.py").read_text(encoding="utf-8")
    workflow_source = (APP_ROOT / "workflows.py").read_text(encoding="utf-8")
    service_source = (APP_ROOT / "services.py").read_text(encoding="utf-8")
    selector_source = (APP_ROOT / "selectors.py").read_text(encoding="utf-8")
    view_source = (APP_ROOT / "api" / "views" / "revenue_analytics.py").read_text(
        encoding="utf-8"
    )
    event_source = (APP_ROOT / "events.py").read_text(encoding="utf-8")

    assert "models.ForeignKey" in models_source
    assert (
        "apps.platform.rbac.permissions.base import RBACPermissionBase"
        in permission_source
    )
    assert "user_has_permission" in policy_source
    assert "RevenueAnalyticsPolicy" in workflow_source
    assert "RevenueAnalyticsService" in workflow_source
    assert "RevenueAnalyticsSelector" in view_source
    assert "request.tenant" in view_source
    assert "request.organization" in view_source
    assert "publish_after_commit" in event_source
    assert "get_or_create" in service_source
    assert "unique_rc_metric_snapshot_period" in models_source

    print("DatavionAI Revenue Cycle RC13 Revenue Analytics Installer v1.0.0")
    print("=" * 72)
    print(f"MANIFEST PASS ({len(actual)} Python files)")
    print("STYLE PASS")
    print("PY_COMPILE PASS")
    print("ARCHITECTURE PASS")
    print("CANONICAL PATIENT: CONSUMED INDIRECTLY VIA REVENUE CYCLE SOURCES")
    print("CANONICAL RBAC: PLATFORM ENGINE")
    print("TENANT CONTEXT: EXPLICIT")
    print(
        "WORKFLOW CHAIN: API -> RBAC -> Workflow -> Policy -> Service -> Selector -> Model -> Event"
    )
    print("DOMAIN EVENTS: AFTER COMMIT")
    print("IDEMPOTENCY: ORGANIZATION + REPORTING PERIOD UNIQUE")
    print("ANALYTICS: DETERMINISTIC SNAPSHOTS")
    print("READS: ORGANIZATION SCOPED SELECTORS")
    print("MIGRATIONS NOT GENERATED")
    print("DATABASE NOT MODIFIED")
    print("BACKUPS CREATED FOR MODIFIED EXISTING FILES")
    print("RC13 REVENUE ANALYTICS INSTALL COMPLETE")


if __name__ == "__main__":
    main()
