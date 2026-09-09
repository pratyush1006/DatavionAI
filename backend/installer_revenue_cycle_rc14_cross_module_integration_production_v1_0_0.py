"""
DatavionAI Revenue Cycle RC14 Cross-Module Integration installer.

Installs the complete RC14 bounded context and performs architecture checks.
No migrations are generated and no database operations are executed.
"""

from __future__ import annotations

import py_compile
import shutil
import textwrap
from pathlib import Path

FILES = {
    "apps/revenue_cycle/cross_module_integration/README.md": "\n"
    "# Revenue Cycle — RC14 Cross-Module "
    "Integration\n"
    "\n"
    "Cross-module integration foundation for "
    "Revenue Cycle.\n"
    "\n"
    "The bounded context provides:\n"
    "- organization-scoped integration "
    "envelopes\n"
    "- idempotent ingestion\n"
    "- explicit processing state\n"
    "- row-locked processing\n"
    "- platform RBAC\n"
    "- explicit tenant and organization "
    "context\n"
    "- workflow and policy enforcement\n"
    "- after-commit domain events\n"
    "- immutable historical integration "
    "records\n"
    "- API and admin access\n"
    "\n"
    "RC14 intentionally does not own a "
    "Patient model and does not generate "
    "migrations.\n",
    "apps/revenue_cycle/cross_module_integration/__init__.py": "\n"
    '"""Revenue Cycle cross-module '
    'integration bounded context."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "__all__ = ()\n",
    "apps/revenue_cycle/cross_module_integration/admin.py": "\n"
    '"""Django admin configuration for '
    'Revenue Cycle integration."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.contrib import admin\n"
    "\n"
    "from .models import "
    "RevenueCycleIntegrationRecord\n"
    "\n"
    "\n"
    "@admin.register(RevenueCycleIntegrationRecord)\n"
    "class "
    "RevenueCycleIntegrationRecordAdmin(admin.ModelAdmin):\n"
    '    """Admin configuration for '
    'integration records."""\n'
    "\n"
    "    list_display = (\n"
    '        "event_name",\n'
    '        "organization",\n'
    '        "source",\n'
    '        "event_type",\n'
    '        "status",\n'
    '        "attempts",\n'
    '        "created_at",\n'
    '        "processed_at",\n'
    "    )\n"
    '    list_filter = ("source", '
    '"event_type", "status")\n'
    "    search_fields = (\n"
    '        "event_name",\n'
    '        "idempotency_key",\n'
    '        "last_error",\n'
    "    )\n"
    "    readonly_fields = (\n"
    '        "organization",\n'
    '        "event_type",\n'
    '        "source",\n'
    '        "event_name",\n'
    '        "aggregate_id",\n'
    '        "idempotency_key",\n'
    '        "payload",\n'
    '        "status",\n'
    '        "attempts",\n'
    '        "last_error",\n'
    '        "processed_at",\n'
    '        "created_by",\n'
    '        "created_at",\n'
    '        "updated_at",\n'
    "    )\n"
    "\n"
    "\n"
    "__all__ = "
    '("RevenueCycleIntegrationRecordAdmin",)\n',
    "apps/revenue_cycle/cross_module_integration/api/__init__.py": "\n"
    '"""Revenue Cycle cross-module '
    'integration API package."""\n'
    "\n"
    "from __future__ import "
    "annotations\n"
    "\n"
    "__all__ = ()\n",
    "apps/revenue_cycle/cross_module_integration/api/serializers/__init__.py": "\n"
    '"""Cross-module '
    "integration API "
    'serializers."""\n'
    "\n"
    "from __future__ "
    "import annotations\n"
    "\n"
    "from .integration "
    "import "
    "RevenueCycleIntegrationRecordSerializer\n"
    "\n"
    "__all__ = "
    '("RevenueCycleIntegrationRecordSerializer",)\n',
    "apps/revenue_cycle/cross_module_integration/api/serializers/integration.py": "\n"
    '"""DRF serializers '
    "for Revenue Cycle "
    "integration "
    'records."""\n'
    "\n"
    "from __future__ "
    "import "
    "annotations\n"
    "\n"
    "from "
    "rest_framework "
    "import "
    "serializers\n"
    "\n"
    "from ...models "
    "import "
    "RevenueCycleIntegrationRecord\n"
    "\n"
    "\n"
    "class "
    "RevenueCycleIntegrationRecordSerializer(serializers.ModelSerializer):\n"
    '    """Serialize '
    "integration "
    "records and "
    "validate their "
    'envelope."""\n'
    "\n"
    "    class Meta:\n"
    "        "
    '"""Configure the '
    "integration record "
    'serializer."""\n'
    "\n"
    "        model = "
    "RevenueCycleIntegrationRecord\n"
    "        fields = "
    "(\n"
    '            "id",\n'
    "            "
    '"organization",\n'
    "            "
    '"event_type",\n'
    "            "
    '"source",\n'
    "            "
    '"event_name",\n'
    "            "
    '"aggregate_id",\n'
    "            "
    '"idempotency_key",\n'
    "            "
    '"payload",\n'
    "            "
    '"status",\n'
    "            "
    '"attempts",\n'
    "            "
    '"last_error",\n'
    "            "
    '"processed_at",\n'
    "            "
    '"created_at",\n'
    "            "
    '"updated_at",\n'
    "        )\n"
    "        "
    "read_only_fields = "
    "(\n"
    '            "id",\n'
    "            "
    '"organization",\n'
    "            "
    '"status",\n'
    "            "
    '"attempts",\n'
    "            "
    '"last_error",\n'
    "            "
    '"processed_at",\n'
    "            "
    '"created_at",\n'
    "            "
    '"updated_at",\n'
    "        )\n"
    "\n"
    "    def "
    "validate_idempotency_key(self, "
    "value):\n"
    '        """Require '
    "a non-empty "
    "integration "
    "idempotency "
    'key."""\n'
    "\n"
    "        if not "
    "value.strip():\n"
    "            raise "
    "serializers.ValidationError(\n"
    "                "
    '"idempotency_key '
    'is required."\n'
    "            )\n"
    "        return "
    "value.strip()\n"
    "\n"
    "    def "
    "validate_event_name(self, "
    "value):\n"
    '        """Require '
    "a non-empty "
    "integration event "
    'name."""\n'
    "\n"
    "        if not "
    "value.strip():\n"
    "            raise "
    "serializers.ValidationError(\n"
    "                "
    '"event_name is '
    'required."\n'
    "            )\n"
    "        return "
    "value.strip()\n"
    "\n"
    "    def "
    "validate_payload(self, "
    "value):\n"
    '        """Require '
    "the event payload "
    "to be a JSON "
    'object."""\n'
    "\n"
    "        if not "
    "isinstance(value, "
    "dict):\n"
    "            raise "
    "serializers.ValidationError(\n"
    "                "
    '"payload must be '
    'an object."\n'
    "            )\n"
    "        return "
    "value\n"
    "\n"
    "\n"
    "__all__ = "
    '("RevenueCycleIntegrationRecordSerializer",)\n',
    "apps/revenue_cycle/cross_module_integration/api/views/__init__.py": "\n"
    '"""Cross-module integration '
    'API views."""\n'
    "\n"
    "from __future__ import "
    "annotations\n"
    "\n"
    "from .integration import "
    "RevenueCycleIntegrationIngestAPIView\n"
    "from .integration import "
    "RevenueCycleIntegrationListAPIView\n"
    "from .integration import "
    "RevenueCycleIntegrationProcessAPIView\n"
    "\n"
    "__all__ = (\n"
    "    "
    '"RevenueCycleIntegrationIngestAPIView",\n'
    "    "
    '"RevenueCycleIntegrationListAPIView",\n'
    "    "
    '"RevenueCycleIntegrationProcessAPIView",\n'
    ")\n",
    "apps/revenue_cycle/cross_module_integration/api/views/integration.py": "\n"
    '"""DRF views for Revenue '
    "Cycle cross-module "
    'integration."""\n'
    "\n"
    "from __future__ import "
    "annotations\n"
    "\n"
    "from uuid import UUID\n"
    "\n"
    "from rest_framework "
    "import status\n"
    "from "
    "rest_framework.permissions "
    "import IsAuthenticated\n"
    "from "
    "rest_framework.response "
    "import Response\n"
    "from "
    "rest_framework.views "
    "import APIView\n"
    "\n"
    "from ...constants import "
    "IntegrationEventType\n"
    "from ...constants import "
    "IntegrationRecordStatus\n"
    "from ...constants import "
    "IntegrationSource\n"
    "from ...policies import "
    "CrossModuleIntegrationPolicy\n"
    "from ...selectors import "
    "CrossModuleIntegrationSelector\n"
    "from ...workflows import "
    "CrossModuleIntegrationWorkflow\n"
    "from ..serializers "
    "import "
    "RevenueCycleIntegrationRecordSerializer\n"
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
    "organization.tenant_id "
    "!= tenant.id:\n"
    "        raise "
    'PermissionError("Organization '
    "does not belong to the "
    'active tenant.")\n'
    "    return tenant, "
    "organization\n"
    "\n"
    "\n"
    "class "
    "RevenueCycleIntegrationListAPIView(APIView):\n"
    '    """List '
    "organization-scoped "
    'integration records."""\n'
    "\n"
    "    permission_classes = "
    "(IsAuthenticated,)\n"
    "\n"
    "    def get(self, "
    "request):\n"
    '        """Return '
    "filtered integration "
    'records."""\n'
    "\n"
    "        _, organization "
    "= _context(request)\n"
    "        if not "
    "CrossModuleIntegrationPolicy.can_list(\n"
    "            "
    "user=request.user,\n"
    "            "
    "organization=organization,\n"
    "        ):\n"
    "            return "
    "Response(status=status.HTTP_403_FORBIDDEN)\n"
    "\n"
    "        status_filter = "
    'request.query_params.get("status")\n'
    "        source_filter = "
    'request.query_params.get("source")\n'
    "\n"
    "        if (\n"
    "            "
    "status_filter\n"
    "            and "
    "status_filter not in "
    "IntegrationRecordStatus.values\n"
    "        ):\n"
    "            return "
    "Response(\n"
    "                "
    '{"detail": "Unsupported '
    'integration status."},\n'
    "                "
    "status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "        if source_filter "
    "and source_filter not in "
    "IntegrationSource.values:\n"
    "            return "
    "Response(\n"
    "                "
    '{"detail": "Unsupported '
    'integration source."},\n'
    "                "
    "status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "\n"
    "        records = "
    "CrossModuleIntegrationSelector.records(\n"
    "            "
    "organization_id=organization.id,\n"
    "            "
    "status=status_filter,\n"
    "            "
    "source=source_filter,\n"
    "        )\n"
    "        return "
    "Response(\n"
    "            "
    "RevenueCycleIntegrationRecordSerializer(\n"
    "                "
    "records,\n"
    "                "
    "many=True,\n"
    "            ).data\n"
    "        )\n"
    "\n"
    "\n"
    "class "
    "RevenueCycleIntegrationIngestAPIView(APIView):\n"
    '    """Ingest a '
    "cross-module integration "
    'event."""\n'
    "\n"
    "    permission_classes = "
    "(IsAuthenticated,)\n"
    "\n"
    "    def post(self, "
    "request):\n"
    '        """Ingest an '
    "integration envelope "
    "through the workflow "
    'layer."""\n'
    "\n"
    "        _, organization "
    "= _context(request)\n"
    "        serializer = "
    "RevenueCycleIntegrationRecordSerializer(\n"
    "            "
    "data=request.data\n"
    "        )\n"
    "        "
    "serializer.is_valid(raise_exception=True)\n"
    "\n"
    "        event_type = "
    'serializer.validated_data["event_type"]\n'
    "        source = "
    'serializer.validated_data["source"]\n'
    "\n"
    "        if event_type "
    "not in "
    "IntegrationEventType.values:\n"
    "            return "
    "Response(\n"
    "                "
    '{"detail": "Unsupported '
    "integration event "
    'type."},\n'
    "                "
    "status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "        if source not in "
    "IntegrationSource.values:\n"
    "            return "
    "Response(\n"
    "                "
    '{"detail": "Unsupported '
    'integration source."},\n'
    "                "
    "status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "\n"
    "        try:\n"
    "            result = "
    "CrossModuleIntegrationWorkflow.ingest(\n"
    "                "
    "user=request.user,\n"
    "                "
    "organization=organization,\n"
    "                "
    "event_type=event_type,\n"
    "                "
    "source=source,\n"
    "                "
    'event_name=serializer.validated_data["event_name"],\n'
    "                "
    'aggregate_id=serializer.validated_data["aggregate_id"],\n'
    "                "
    'idempotency_key=serializer.validated_data["idempotency_key"],\n'
    "                "
    'payload=serializer.validated_data["payload"],\n'
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
    "        except "
    "ValueError as exc:\n"
    "            return "
    "Response(\n"
    "                "
    '{"detail": str(exc)},\n'
    "                "
    "status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "\n"
    "        return "
    "Response(\n"
    "            "
    "RevenueCycleIntegrationRecordSerializer(result).data,\n"
    "            "
    "status=status.HTTP_201_CREATED,\n"
    "        )\n"
    "\n"
    "\n"
    "class "
    "RevenueCycleIntegrationProcessAPIView(APIView):\n"
    '    """Process a pending '
    "cross-module integration "
    'record."""\n'
    "\n"
    "    permission_classes = "
    "(IsAuthenticated,)\n"
    "\n"
    "    def post(self, "
    "request, record_id: "
    "UUID):\n"
    '        """Process an '
    "integration record "
    "through the workflow "
    'layer."""\n'
    "\n"
    "        _, organization "
    "= _context(request)\n"
    "        try:\n"
    "            result = "
    "CrossModuleIntegrationWorkflow.process(\n"
    "                "
    "user=request.user,\n"
    "                "
    "organization=organization,\n"
    "                "
    "record_id=record_id,\n"
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
    "        except "
    "ValueError as exc:\n"
    "            return "
    "Response(\n"
    "                "
    '{"detail": str(exc)},\n'
    "                "
    "status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "        except "
    "RevenueCycleIntegrationRecord.DoesNotExist:\n"
    "            return "
    "Response(\n"
    "                "
    '{"detail": "Integration '
    'record not found."},\n'
    "                "
    "status=status.HTTP_404_NOT_FOUND,\n"
    "            )\n"
    "\n"
    "        return "
    "Response(\n"
    "            "
    "RevenueCycleIntegrationRecordSerializer(result).data,\n"
    "            "
    "status=status.HTTP_200_OK,\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    "    "
    '"RevenueCycleIntegrationIngestAPIView",\n'
    "    "
    '"RevenueCycleIntegrationListAPIView",\n'
    "    "
    '"RevenueCycleIntegrationProcessAPIView",\n'
    ")\n",
    "apps/revenue_cycle/cross_module_integration/apps.py": "\n"
    '"""Django application configuration for '
    'cross-module integration."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.apps import AppConfig\n"
    "\n"
    "\n"
    "class "
    "CrossModuleIntegrationConfig(AppConfig):\n"
    '    """Configure Revenue Cycle '
    'cross-module integration."""\n'
    "\n"
    "    default_auto_field = "
    '"django.db.models.BigAutoField"\n'
    "    name = "
    '"apps.revenue_cycle.cross_module_integration"\n'
    "    label = "
    '"revenue_cycle_cross_module_integration"\n'
    '    verbose_name = "Revenue Cycle '
    'Cross-Module Integration"\n'
    "\n"
    "\n"
    "__all__ = "
    '("CrossModuleIntegrationConfig",)\n',
    "apps/revenue_cycle/cross_module_integration/constants.py": "\n"
    '"""Constants for Revenue Cycle '
    'cross-module integration."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.db import models\n"
    "\n"
    "\n"
    "class "
    "IntegrationRecordStatus(models.TextChoices):\n"
    '    """Supported integration record '
    'states."""\n'
    "\n"
    '    PENDING = "PENDING", "Pending"\n'
    '    PROCESSED = "PROCESSED", '
    '"Processed"\n'
    '    FAILED = "FAILED", "Failed"\n'
    '    IGNORED = "IGNORED", "Ignored"\n'
    "\n"
    "\n"
    "class "
    "IntegrationSource(models.TextChoices):\n"
    '    """Supported Revenue Cycle '
    'source contexts."""\n'
    "\n"
    '    ELIGIBILITY = "ELIGIBILITY", '
    '"Eligibility"\n'
    "    INSURANCE_VERIFICATION = "
    '"INSURANCE_VERIFICATION", "Insurance '
    'Verification"\n'
    "    PRIOR_AUTHORIZATION = "
    '"PRIOR_AUTHORIZATION", "Prior '
    'Authorization"\n'
    "    CHARGE_CAPTURE = "
    '"CHARGE_CAPTURE", "Charge Capture"\n'
    '    CODING = "CODING", "Coding"\n'
    "    CLAIM_SCRUBBING = "
    '"CLAIM_SCRUBBING", "Claim '
    'Scrubbing"\n'
    "    CLAIM_SUBMISSION = "
    '"CLAIM_SUBMISSION", "Claim '
    'Submission"\n'
    "    PAYMENT_POSTING = "
    '"PAYMENT_POSTING", "Payment '
    'Posting"\n'
    '    ERA = "ERA", "ERA"\n'
    '    DENIALS = "DENIALS", "Denials"\n'
    '    APPEALS = "APPEALS", "Appeals"\n'
    "    ACCOUNTS_RECEIVABLE = "
    '"ACCOUNTS_RECEIVABLE", "Accounts '
    'Receivable"\n'
    "    REVENUE_ANALYTICS = "
    '"REVENUE_ANALYTICS", "Revenue '
    'Analytics"\n'
    "\n"
    "\n"
    "class "
    "IntegrationEventType(models.TextChoices):\n"
    '    """Supported integration event '
    'categories."""\n'
    "\n"
    "    PATIENT_CONTEXT = "
    '"PATIENT_CONTEXT", "Patient '
    'Context"\n'
    '    CLAIM_CONTEXT = "CLAIM_CONTEXT", '
    '"Claim Context"\n'
    "    PAYMENT_CONTEXT = "
    '"PAYMENT_CONTEXT", "Payment '
    'Context"\n'
    '    AR_CONTEXT = "AR_CONTEXT", "AR '
    'Context"\n'
    "    ANALYTICS_CONTEXT = "
    '"ANALYTICS_CONTEXT", "Analytics '
    'Context"\n'
    "\n"
    "\n"
    "__all__ = (\n"
    '    "IntegrationEventType",\n'
    '    "IntegrationRecordStatus",\n'
    '    "IntegrationSource",\n'
    ")\n",
    "apps/revenue_cycle/cross_module_integration/events.py": "\n"
    '"""Domain events for Revenue Cycle '
    'cross-module integration."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from typing import Any\n"
    "from uuid import UUID\n"
    "\n"
    "from apps.core.events import "
    "DomainEvent\n"
    "from apps.core.events import "
    "publish_after_commit\n"
    "\n"
    "\n"
    "class "
    "CrossModuleIntegrationEvent(DomainEvent):\n"
    '    """Represent a cross-module Revenue '
    'Cycle integration event."""\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        event_type: str,\n"
    "        aggregate_id: UUID,\n"
    "        payload: dict[str, Any],\n"
    "    ) -> None:\n"
    '        """Initialize an integration '
    'domain event."""\n'
    "\n"
    "        super().__init__(\n"
    "            event_type=event_type,\n"
    "            aggregate_id=aggregate_id,\n"
    "            payload=payload,\n"
    "        )\n"
    "\n"
    "\n"
    "def publish_integration_event(\n"
    "    *,\n"
    "    event_type: str,\n"
    "    aggregate_id: UUID,\n"
    "    payload: dict[str, Any],\n"
    ") -> None:\n"
    '    """Publish an integration event '
    "after the current transaction "
    'commits."""\n'
    "\n"
    "    publish_after_commit(\n"
    "        CrossModuleIntegrationEvent(\n"
    "            event_type=event_type,\n"
    "            aggregate_id=aggregate_id,\n"
    "            payload=payload,\n"
    "        )\n"
    "    )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "CrossModuleIntegrationEvent",\n'
    '    "publish_integration_event",\n'
    ")\n",
    "apps/revenue_cycle/cross_module_integration/migrations/__init__.py": "\n"
    '"""Cross-module '
    "integration "
    'migrations."""\n'
    "\n"
    "from __future__ import "
    "annotations\n"
    "\n"
    "__all__ = ()\n",
    "apps/revenue_cycle/cross_module_integration/models.py": "\n"
    '"""Persistent integration records for '
    "Revenue Cycle cross-module "
    'coordination."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.conf import settings\n"
    "from django.db import models\n"
    "from django.db.models import Q\n"
    "\n"
    "from apps.core.models import BaseModel\n"
    "\n"
    "from .constants import "
    "IntegrationEventType\n"
    "from .constants import "
    "IntegrationRecordStatus\n"
    "from .constants import "
    "IntegrationSource\n"
    "\n"
    "\n"
    "class "
    "RevenueCycleIntegrationRecord(BaseModel):\n"
    '    """Persist an organization-scoped '
    "integration message and processing "
    'state."""\n'
    "\n"
    "    organization = models.ForeignKey(\n"
    '        "organizations.Organization",\n'
    "        on_delete=models.PROTECT,\n"
    "        "
    'related_name="revenue_cycle_integration_records",\n'
    "    )\n"
    "    event_type = models.CharField(\n"
    "        max_length=30,\n"
    "        "
    "choices=IntegrationEventType.choices,\n"
    "    )\n"
    "    source = models.CharField(\n"
    "        max_length=30,\n"
    "        "
    "choices=IntegrationSource.choices,\n"
    "    )\n"
    "    event_name = "
    "models.CharField(max_length=150)\n"
    "    aggregate_id = models.UUIDField()\n"
    "    idempotency_key = "
    "models.CharField(max_length=200)\n"
    "    payload = "
    "models.JSONField(default=dict)\n"
    "    status = models.CharField(\n"
    "        max_length=20,\n"
    "        "
    "choices=IntegrationRecordStatus.choices,\n"
    "        "
    "default=IntegrationRecordStatus.PENDING,\n"
    "        db_index=True,\n"
    "    )\n"
    "    attempts = "
    "models.PositiveIntegerField(default=0)\n"
    "    last_error = "
    "models.TextField(blank=True)\n"
    "    processed_at = "
    "models.DateTimeField(null=True, "
    "blank=True)\n"
    "    created_by = models.ForeignKey(\n"
    "        settings.AUTH_USER_MODEL,\n"
    "        on_delete=models.SET_NULL,\n"
    "        null=True,\n"
    "        blank=True,\n"
    "        "
    'related_name="revenue_cycle_integration_records",\n'
    "    )\n"
    "\n"
    "    class Meta:\n"
    '        """Configure integration '
    'uniqueness and query indexes."""\n'
    "\n"
    "        db_table = "
    '"revenue_cycle_integration_records"\n'
    '        ordering = ("-created_at",)\n'
    "        constraints = (\n"
    "            models.UniqueConstraint(\n"
    '                fields=("organization", '
    '"idempotency_key"),\n'
    "                "
    'name="unique_rc_integration_idempotency",\n'
    "            ),\n"
    "            models.CheckConstraint(\n"
    "                "
    "condition=Q(attempts__gte=0),\n"
    "                "
    'name="rc_integration_attempts_non_negative",\n'
    "            ),\n"
    "        )\n"
    "        indexes = (\n"
    "            models.Index(\n"
    '                fields=("organization", '
    '"status", "created_at"),\n'
    "                "
    'name="rc_integration_status_idx",\n'
    "            ),\n"
    "            models.Index(\n"
    '                fields=("organization", '
    '"source", "created_at"),\n'
    "                "
    'name="rc_integration_source_idx",\n'
    "            ),\n"
    "            models.Index(\n"
    '                fields=("organization", '
    '"aggregate_id"),\n'
    "                "
    'name="rc_integration_aggregate_idx",\n'
    "            ),\n"
    "        )\n"
    "\n"
    "    def __str__(self) -> str:\n"
    '        """Return a stable integration '
    'record label."""\n'
    "\n"
    "        return "
    'f"{self.source}:{self.event_name}:{self.idempotency_key}"\n'
    "\n"
    "\n"
    "__all__ = "
    '("RevenueCycleIntegrationRecord",)\n',
    "apps/revenue_cycle/cross_module_integration/permissions.py": "\n"
    '"""RBAC permissions for Revenue '
    "Cycle cross-module "
    'integration."""\n'
    "\n"
    "from __future__ import "
    "annotations\n"
    "\n"
    "from "
    "apps.platform.rbac.permissions.base "
    "import RBACPermissionBase\n"
    "\n"
    "\n"
    "class "
    "CrossModuleIntegrationPermission(RBACPermissionBase):\n"
    '    """Define canonical '
    'integration permissions."""\n'
    "\n"
    "    LIST = "
    '"revenue_cycle.cross_module_integration.list"\n'
    "    VIEW = "
    '"revenue_cycle.cross_module_integration.view"\n'
    "    PROCESS = "
    '"revenue_cycle.cross_module_integration.process"\n'
    "\n"
    "\n"
    "__all__ = "
    '("CrossModuleIntegrationPermission",)\n',
    "apps/revenue_cycle/cross_module_integration/policies.py": "\n"
    '"""Authorization policies for Revenue '
    'Cycle integration."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from typing import Any\n"
    "\n"
    "from apps.platform.rbac.engines "
    "import user_has_permission\n"
    "\n"
    "from .permissions import "
    "CrossModuleIntegrationPermission\n"
    "\n"
    "\n"
    "class CrossModuleIntegrationPolicy:\n"
    '    """Evaluate organization-scoped '
    'integration permissions."""\n'
    "\n"
    "    @staticmethod\n"
    "    def can_list(*, user: Any, "
    "organization: Any) -> bool:\n"
    '        """Return whether the actor '
    'can list integration records."""\n'
    "\n"
    "        return user_has_permission(\n"
    "            user=user,\n"
    "            "
    "permission=CrossModuleIntegrationPermission.LIST,\n"
    "            "
    "organization=organization,\n"
    "        )\n"
    "\n"
    "    @staticmethod\n"
    "    def can_view(*, user: Any, "
    "organization: Any) -> bool:\n"
    '        """Return whether the actor '
    'can view integration records."""\n'
    "\n"
    "        return user_has_permission(\n"
    "            user=user,\n"
    "            "
    "permission=CrossModuleIntegrationPermission.VIEW,\n"
    "            "
    "organization=organization,\n"
    "        )\n"
    "\n"
    "    @staticmethod\n"
    "    def can_process(*, user: Any, "
    "organization: Any) -> bool:\n"
    '        """Return whether the actor '
    'can process integration records."""\n'
    "\n"
    "        return user_has_permission(\n"
    "            user=user,\n"
    "            "
    "permission=CrossModuleIntegrationPermission.PROCESS,\n"
    "            "
    "organization=organization,\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = "
    '("CrossModuleIntegrationPolicy",)\n',
    "apps/revenue_cycle/cross_module_integration/selectors.py": "\n"
    '"""Organization-scoped selectors for '
    "Revenue Cycle integration "
    'records."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from uuid import UUID\n"
    "\n"
    "from django.db.models import "
    "QuerySet\n"
    "\n"
    "from .models import "
    "RevenueCycleIntegrationRecord\n"
    "\n"
    "\n"
    "class "
    "CrossModuleIntegrationSelector:\n"
    '    """Provide organization-scoped '
    'integration record reads."""\n'
    "\n"
    "    @staticmethod\n"
    "    def records(\n"
    "        *,\n"
    "        organization_id: UUID,\n"
    "        status: str | None = None,\n"
    "        source: str | None = None,\n"
    "    ) -> "
    "QuerySet[RevenueCycleIntegrationRecord]:\n"
    '        """Return filtered '
    'integration records."""\n'
    "\n"
    "        queryset = "
    "RevenueCycleIntegrationRecord.objects.filter(\n"
    "            "
    "organization_id=organization_id,\n"
    "        )\n"
    "        if status:\n"
    "            queryset = "
    "queryset.filter(status=status)\n"
    "        if source:\n"
    "            queryset = "
    "queryset.filter(source=source)\n"
    "        return "
    'queryset.order_by("-created_at")\n'
    "\n"
    "\n"
    "__all__ = "
    '("CrossModuleIntegrationSelector",)\n',
    "apps/revenue_cycle/cross_module_integration/services.py": "\n"
    '"""Transactional services for Revenue '
    'Cycle cross-module integration."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from typing import Any\n"
    "from uuid import UUID\n"
    "\n"
    "from django.db import IntegrityError\n"
    "from django.db import transaction\n"
    "from django.utils import timezone\n"
    "\n"
    "from .constants import "
    "IntegrationRecordStatus\n"
    "from .events import "
    "publish_integration_event\n"
    "from .models import "
    "RevenueCycleIntegrationRecord\n"
    "\n"
    "\n"
    "class CrossModuleIntegrationService:\n"
    '    """Persist and process '
    "organization-scoped integration "
    'messages."""\n'
    "\n"
    "    @staticmethod\n"
    "    @transaction.atomic\n"
    "    def ingest(\n"
    "        *,\n"
    "        organization: Any,\n"
    "        event_type: str,\n"
    "        source: str,\n"
    "        event_name: str,\n"
    "        aggregate_id: UUID,\n"
    "        idempotency_key: str,\n"
    "        payload: dict[str, Any],\n"
    "        actor: Any = None,\n"
    "    ) -> "
    "RevenueCycleIntegrationRecord:\n"
    '        """Create one integration '
    "record, returning an existing "
    'idempotent record."""\n'
    "\n"
    "        if not idempotency_key:\n"
    "            raise "
    'ValueError("idempotency_key is '
    'required.")\n'
    "        if not event_name:\n"
    "            raise "
    'ValueError("event_name is '
    'required.")\n'
    "        if not isinstance(payload, "
    "dict):\n"
    '            raise ValueError("payload '
    'must be an object.")\n'
    "\n"
    "        existing = "
    "RevenueCycleIntegrationRecord.objects.filter(\n"
    "            "
    "organization=organization,\n"
    "            "
    "idempotency_key=idempotency_key,\n"
    "        ).first()\n"
    "        if existing:\n"
    "            return existing\n"
    "\n"
    "        try:\n"
    "            record = "
    "RevenueCycleIntegrationRecord.objects.create(\n"
    "                "
    "organization=organization,\n"
    "                "
    "event_type=event_type,\n"
    "                source=source,\n"
    "                "
    "event_name=event_name,\n"
    "                "
    "aggregate_id=aggregate_id,\n"
    "                "
    "idempotency_key=idempotency_key,\n"
    "                payload=payload,\n"
    "                created_by=actor,\n"
    "            )\n"
    "        except IntegrityError:\n"
    "            record = "
    "RevenueCycleIntegrationRecord.objects.get(\n"
    "                "
    "organization=organization,\n"
    "                "
    "idempotency_key=idempotency_key,\n"
    "            )\n"
    "\n"
    "        publish_integration_event(\n"
    "            "
    'event_type="revenue_cycle.integration.record_ingested",\n'
    "            aggregate_id=record.id,\n"
    "            payload={\n"
    '                "organization_id": '
    "str(organization.id),\n"
    '                "event_name": '
    "record.event_name,\n"
    '                "source": '
    "record.source,\n"
    '                "status": '
    "record.status,\n"
    "            },\n"
    "        )\n"
    "        return record\n"
    "\n"
    "    @staticmethod\n"
    "    @transaction.atomic\n"
    "    def process(\n"
    "        *,\n"
    "        organization: Any,\n"
    "        record_id: UUID,\n"
    "        actor: Any,\n"
    "    ) -> "
    "RevenueCycleIntegrationRecord:\n"
    '        """Process a pending '
    "integration record with row-level "
    'locking."""\n'
    "\n"
    "        record = "
    "RevenueCycleIntegrationRecord.objects.select_for_update().get(\n"
    "            "
    "organization_id=organization.id,\n"
    "            id=record_id,\n"
    "        )\n"
    "\n"
    "        if record.status == "
    "IntegrationRecordStatus.PROCESSED:\n"
    "            return record\n"
    "        if record.status == "
    "IntegrationRecordStatus.IGNORED:\n"
    '            raise ValueError("Ignored '
    "integration records cannot be "
    'processed.")\n'
    "\n"
    "        record.attempts += 1\n"
    "\n"
    "        try:\n"
    "            "
    "CrossModuleIntegrationService._validate_payload(record)\n"
    "        except ValueError as exc:\n"
    "            record.status = "
    "IntegrationRecordStatus.FAILED\n"
    "            record.last_error = "
    "str(exc)\n"
    "            record.save(\n"
    "                update_fields=[\n"
    '                    "status",\n'
    '                    "last_error",\n'
    '                    "attempts",\n'
    '                    "updated_at",\n'
    "                ]\n"
    "            )\n"
    "            raise\n"
    "\n"
    "        record.status = "
    "IntegrationRecordStatus.PROCESSED\n"
    '        record.last_error = ""\n'
    "        record.processed_at = "
    "timezone.now()\n"
    "        record.save(\n"
    "            update_fields=[\n"
    '                "status",\n'
    '                "last_error",\n'
    '                "processed_at",\n'
    '                "attempts",\n'
    '                "updated_at",\n'
    "            ]\n"
    "        )\n"
    "\n"
    "        publish_integration_event(\n"
    "            "
    'event_type="revenue_cycle.integration.record_processed",\n'
    "            aggregate_id=record.id,\n"
    "            payload={\n"
    '                "organization_id": '
    "str(organization.id),\n"
    '                "processed_by": '
    "str(actor.id),\n"
    '                "event_name": '
    "record.event_name,\n"
    '                "attempts": '
    "record.attempts,\n"
    "            },\n"
    "        )\n"
    "        return record\n"
    "\n"
    "    @staticmethod\n"
    "    def _validate_payload(\n"
    "        record: "
    "RevenueCycleIntegrationRecord,\n"
    "    ) -> None:\n"
    '        """Validate the minimum '
    'envelope required for processing."""\n'
    "\n"
    "        required = {\n"
    '            "event_name": '
    "record.event_name,\n"
    '            "event_type": '
    "record.event_type,\n"
    '            "source": record.source,\n'
    "        }\n"
    "        if any(not value for value in "
    "required.values()):\n"
    "            raise "
    'ValueError("Integration event '
    'envelope is incomplete.")\n'
    "\n"
    "\n"
    "__all__ = "
    '("CrossModuleIntegrationService",)\n',
    "apps/revenue_cycle/cross_module_integration/tests/__init__.py": "\n"
    '"""Cross-module integration '
    'tests."""\n'
    "\n"
    "from __future__ import "
    "annotations\n"
    "\n"
    "__all__ = ()\n",
    "apps/revenue_cycle/cross_module_integration/tests/test_invariants.py": "\n"
    '"""Architecture tests '
    "for Revenue Cycle "
    "cross-module "
    'integration."""\n'
    "\n"
    "from __future__ import "
    "annotations\n"
    "\n"
    "from django.test import "
    "SimpleTestCase\n"
    "\n"
    "from ..models import "
    "RevenueCycleIntegrationRecord\n"
    "\n"
    "\n"
    "class "
    "CrossModuleIntegrationArchitectureTests(SimpleTestCase):\n"
    '    """Verify '
    "non-negotiable "
    "integration "
    'architecture."""\n'
    "\n"
    "    def "
    "test_organization_scope_exists(self) "
    "-> None:\n"
    '        """Verify '
    "integration records are "
    'organization scoped."""\n'
    "\n"
    "        field = "
    'RevenueCycleIntegrationRecord._meta.get_field("organization")\n'
    "        "
    "self.assertIsNotNone(field.remote_field.model)\n"
    "\n"
    "    def "
    "test_idempotency_constraint_exists(self) "
    "-> None:\n"
    '        """Verify '
    "organization-scoped "
    "idempotency is "
    'enforced."""\n'
    "\n"
    "        constraint_names "
    "= {\n"
    "            "
    "constraint.name\n"
    "            for "
    "constraint in "
    "RevenueCycleIntegrationRecord._meta.constraints\n"
    "        }\n"
    "        self.assertIn(\n"
    "            "
    '"unique_rc_integration_idempotency",\n'
    "            "
    "constraint_names,\n"
    "        )\n"
    "\n"
    "    def "
    "test_processing_state_exists(self) "
    "-> None:\n"
    '        """Verify '
    "integration processing "
    "has explicit lifecycle "
    'states."""\n'
    "\n"
    "        field = "
    'RevenueCycleIntegrationRecord._meta.get_field("status")\n'
    "        "
    "self.assertEqual(field.default, "
    '"PENDING")\n'
    "\n"
    "\n"
    "__all__ = "
    '("CrossModuleIntegrationArchitectureTests",)\n',
    "apps/revenue_cycle/cross_module_integration/urls.py": "\n"
    '"""URL routes for Revenue Cycle '
    'cross-module integration."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.urls import path\n"
    "\n"
    "from .api.views import "
    "RevenueCycleIntegrationIngestAPIView\n"
    "from .api.views import "
    "RevenueCycleIntegrationListAPIView\n"
    "from .api.views import "
    "RevenueCycleIntegrationProcessAPIView\n"
    "\n"
    "app_name = "
    '"revenue_cycle_cross_module_integration"\n'
    "\n"
    "urlpatterns = [\n"
    "    path(\n"
    '        "records/",\n'
    "        "
    "RevenueCycleIntegrationListAPIView.as_view(),\n"
    '        name="record-list",\n'
    "    ),\n"
    "    path(\n"
    '        "records/ingest/",\n'
    "        "
    "RevenueCycleIntegrationIngestAPIView.as_view(),\n"
    '        name="record-ingest",\n'
    "    ),\n"
    "    path(\n"
    "        "
    '"records/<uuid:record_id>/process/",\n'
    "        "
    "RevenueCycleIntegrationProcessAPIView.as_view(),\n"
    '        name="record-process",\n'
    "    ),\n"
    "]\n"
    "\n"
    '__all__ = ("app_name", "urlpatterns")\n',
    "apps/revenue_cycle/cross_module_integration/workflows.py": "\n"
    '"""Workflow orchestration for '
    "Revenue Cycle cross-module "
    'integration."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from typing import Any\n"
    "from uuid import UUID\n"
    "\n"
    "from .policies import "
    "CrossModuleIntegrationPolicy\n"
    "from .services import "
    "CrossModuleIntegrationService\n"
    "\n"
    "\n"
    "class "
    "CrossModuleIntegrationWorkflow:\n"
    '    """Orchestrate authorized '
    'integration operations."""\n'
    "\n"
    "    @staticmethod\n"
    "    def ingest(\n"
    "        *,\n"
    "        user: Any,\n"
    "        organization: Any,\n"
    "        event_type: str,\n"
    "        source: str,\n"
    "        event_name: str,\n"
    "        aggregate_id: UUID,\n"
    "        idempotency_key: str,\n"
    "        payload: dict[str, Any],\n"
    "    ) -> Any:\n"
    '        """Authorize and ingest an '
    'integration record."""\n'
    "\n"
    "        if not "
    "CrossModuleIntegrationPolicy.can_process(\n"
    "            user=user,\n"
    "            "
    "organization=organization,\n"
    "        ):\n"
    "            raise PermissionError(\n"
    '                "Revenue Cycle '
    "integration processing permission is "
    'required."\n'
    "            )\n"
    "\n"
    "        return "
    "CrossModuleIntegrationService.ingest(\n"
    "            "
    "organization=organization,\n"
    "            event_type=event_type,\n"
    "            source=source,\n"
    "            event_name=event_name,\n"
    "            "
    "aggregate_id=aggregate_id,\n"
    "            "
    "idempotency_key=idempotency_key,\n"
    "            payload=payload,\n"
    "            actor=user,\n"
    "        )\n"
    "\n"
    "    @staticmethod\n"
    "    def process(\n"
    "        *,\n"
    "        user: Any,\n"
    "        organization: Any,\n"
    "        record_id: UUID,\n"
    "    ) -> Any:\n"
    '        """Authorize and process an '
    'integration record."""\n'
    "\n"
    "        if not "
    "CrossModuleIntegrationPolicy.can_process(\n"
    "            user=user,\n"
    "            "
    "organization=organization,\n"
    "        ):\n"
    "            raise PermissionError(\n"
    '                "Revenue Cycle '
    "integration processing permission is "
    'required."\n'
    "            )\n"
    "\n"
    "        return "
    "CrossModuleIntegrationService.process(\n"
    "            "
    "organization=organization,\n"
    "            record_id=record_id,\n"
    "            actor=user,\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = "
    '("CrossModuleIntegrationWorkflow",)\n',
}

ROOT = Path(__file__).resolve().parent
APP_ROOT = ROOT / "apps" / "revenue_cycle" / "cross_module_integration"
BACKUP_ROOT = ROOT / ".rc14_cross_module_integration_backup"


def write_file(relative_path: str, content: str) -> None:
    """Write one file and preserve an existing version in a backup directory."""

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
    """Install and verify RC14."""

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
            f"RC14 manifest mismatch: missing={missing}, unexpected={unexpected}"
        )

    for relative_path in actual:
        source_path = ROOT / relative_path
        source = source_path.read_text(encoding="utf-8")
        if not source.lstrip().startswith('"""'):
            raise AssertionError(f"RC14 style failure: {relative_path}")
        if "from __future__ import annotations" not in source:
            raise AssertionError(f"RC14 style failure: {relative_path}")
        py_compile.compile(str(source_path), doraise=True)

    models_source = (APP_ROOT / "models.py").read_text(encoding="utf-8")
    permission_source = (APP_ROOT / "permissions.py").read_text(encoding="utf-8")
    policy_source = (APP_ROOT / "policies.py").read_text(encoding="utf-8")
    workflow_source = (APP_ROOT / "workflows.py").read_text(encoding="utf-8")
    service_source = (APP_ROOT / "services.py").read_text(encoding="utf-8")
    selector_source = (APP_ROOT / "selectors.py").read_text(encoding="utf-8")
    event_source = (APP_ROOT / "events.py").read_text(encoding="utf-8")
    view_source = (APP_ROOT / "api" / "views" / "integration.py").read_text(
        encoding="utf-8"
    )

    assert "organization = models.ForeignKey" in models_source
    assert "unique_rc_integration_idempotency" in models_source
    assert "RBACPermissionBase" in permission_source
    assert "user_has_permission" in policy_source
    assert "CrossModuleIntegrationPolicy" in workflow_source
    assert "CrossModuleIntegrationService" in workflow_source
    assert "select_for_update" in service_source
    assert "CrossModuleIntegrationSelector" in view_source
    assert "request.tenant" in view_source
    assert "request.organization" in view_source
    assert "publish_after_commit" in event_source

    # RC14 must not introduce a patient model or legacy patient dependency.
    all_sources = "\n".join(
        (ROOT / relative_path).read_text(encoding="utf-8") for relative_path in expected
    )
    assert "class Patient(" not in all_sources
    assert "apps.clinical.patients" not in all_sources
    assert "to='patients.patient'" not in all_sources

    print("DatavionAI Revenue Cycle RC14 Cross-Module Integration Installer v1.0.0")
    print("=" * 72)
    print(f"MANIFEST PASS ({len(actual)} Python files)")
    print("STYLE PASS")
    print("PY_COMPILE PASS")
    print("ARCHITECTURE PASS")
    print("CANONICAL PATIENT: NO PATIENT MODEL OWNED")
    print("CANONICAL RBAC: PLATFORM ENGINE")
    print("TENANT CONTEXT: EXPLICIT")
    print(
        "WORKFLOW CHAIN: API -> RBAC -> Workflow -> Policy -> "
        "Service -> Selector -> Model -> Event"
    )
    print("DOMAIN EVENTS: AFTER COMMIT")
    print("IDEMPOTENCY: ORGANIZATION + KEY UNIQUE")
    print("CONCURRENCY: SELECT_FOR_UPDATE PROCESSING")
    print("INTEGRATION: IDEMPOTENT EVENT ENVELOPES")
    print("MIGRATIONS NOT GENERATED")
    print("DATABASE NOT MODIFIED")
    print("BACKUPS CREATED FOR MODIFIED EXISTING FILES")
    print("RC14 CROSS-MODULE INTEGRATION INSTALL COMPLETE")


if __name__ == "__main__":
    main()
