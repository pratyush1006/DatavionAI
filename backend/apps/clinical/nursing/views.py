from __future__ import annotations

from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.clinical.providers.models import Provider
from apps.platform.rbac.permissions.base import RBACPermissionBase

from .models import (
    CarePlan,
    ClinicalAlert,
    MedicationAdministration,
    NurseSchedule,
    NursingTask,
    PatientAssignment,
    ShiftHandover,
)
from .serializers import (
    CarePlanSerializer,
    ClinicalAlertSerializer,
    MedicationAdministrationSerializer,
    NurseScheduleSerializer,
    NursingTaskSerializer,
    PatientAssignmentSerializer,
    ShiftHandoverSerializer,
)


class NursingPermission(RBACPermissionBase):
    def has_permission(self, request, view):
        self.permission_code = f"nursing.{view.permission_action()}"
        return super().has_permission(request, view)


class NursingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, NursingPermission)
    http_method_names = ("get", "post", "patch", "delete", "head", "options")

    def permission_action(self):
        return {
            "list": "view",
            "retrieve": "view",
            "create": "create",
            "destroy": "delete",
        }.get(self.action, "update")

    def organization(self):
        organization = getattr(self.request, "organization", None) or getattr(
            self.request, "current_organization", None
        )
        if not organization:
            raise ValidationError("Organization context is required.")
        return organization

    def get_queryset(self):
        return self.queryset.filter(organization=self.organization())

    def perform_create(self, serializer):
        serializer.save(organization=self.organization())

    def actor(self):
        provider = Provider.objects.filter(
            organization=self.organization(), employee__user=self.request.user
        ).first()
        if not provider:
            raise ValidationError(
                "The authenticated user does not have a provider profile in this organization."
            )
        return provider

    def locked(self):
        return (
            self.queryset.model.objects.select_for_update()
            .filter(organization=self.organization())
            .get(pk=self.kwargs["pk"])
        )


class PatientAssignmentViewSet(NursingViewSet):
    queryset = PatientAssignment.objects.select_related(
        "patient", "nurse", "nurse__employee", "ward"
    )
    serializer_class = PatientAssignmentSerializer

    @action(detail=True, methods=("post",))
    def end(self, request, pk=None):
        with transaction.atomic():
            record = self.locked()
            if record.status != "active":
                raise ValidationError("Only an active assignment can be ended.")
            record.status, record.ended_at = "ended", timezone.now()
            record.save(update_fields=("status", "ended_at", "updated_at"))
        return Response(self.get_serializer(record).data)


class NursingTaskViewSet(NursingViewSet):
    queryset = NursingTask.objects.select_related(
        "patient", "assigned_nurse", "assigned_nurse__employee"
    )
    serializer_class = NursingTaskSerializer

    def _transition(self, target):
        allowed = {
            "start": ("pending", "in_progress"),
            "complete": (("pending", "in_progress"), "completed"),
            "cancel": (("pending", "in_progress"), "cancelled"),
        }
        source, destination = allowed[target]
        with transaction.atomic():
            record = self.locked()
            valid = (
                record.status in source
                if isinstance(source, tuple)
                else record.status == source
            )
            if not valid:
                raise ValidationError(
                    f"Task cannot be {target}ed from {record.status}."
                )
            record.status = destination
            fields = ["status", "updated_at"]
            if target == "complete":
                record.completed_at, record.completed_by = timezone.now(), self.actor()
                record.completion_notes = str(
                    self.request.data.get("completion_notes", "")
                )
                fields += ["completed_at", "completed_by", "completion_notes"]
            record.save(update_fields=fields)
        return Response(self.get_serializer(record).data)

    @action(detail=True, methods=("post",))
    def start(self, request, pk=None):
        return self._transition("start")

    @action(detail=True, methods=("post",))
    def complete(self, request, pk=None):
        return self._transition("complete")

    @action(detail=True, methods=("post",))
    def cancel(self, request, pk=None):
        return self._transition("cancel")


class MedicationAdministrationViewSet(NursingViewSet):
    queryset = MedicationAdministration.objects.select_related(
        "patient", "nurse", "nurse__employee", "prescription"
    )
    serializer_class = MedicationAdministrationSerializer

    @action(detail=True, methods=("post",))
    def administer(self, request, pk=None):
        with transaction.atomic():
            record = self.locked()
            if record.status != "scheduled":
                raise ValidationError("Only a scheduled dose can be administered.")
            if record.nurse_id != self.actor().id:
                raise ValidationError(
                    "Only the assigned nurse can administer this dose."
                )
            record.status, record.administered_at = "administered", timezone.now()
            record.notes = str(request.data.get("notes", record.notes))
            record.save(
                update_fields=("status", "administered_at", "notes", "updated_at")
            )
        return Response(self.get_serializer(record).data)

    @action(detail=True, methods=("post",), url_path="record-outcome")
    def record_outcome(self, request, pk=None):
        outcome = request.data.get("status")
        if outcome not in ("held", "refused", "missed"):
            raise ValidationError({"status": "Use held, refused, or missed."})
        with transaction.atomic():
            record = self.locked()
            if record.status != "scheduled":
                raise ValidationError("Only a scheduled dose can receive an outcome.")
            record.status, record.notes = outcome, str(request.data.get("notes", ""))
            record.save(update_fields=("status", "notes", "updated_at"))
        return Response(self.get_serializer(record).data)


class CarePlanViewSet(NursingViewSet):
    queryset = CarePlan.objects.select_related(
        "patient", "primary_nurse", "primary_nurse__employee"
    )
    serializer_class = CarePlanSerializer

    def perform_update(self, serializer):
        serializer.save(version=serializer.instance.version + 1)

    def _status(self, target, allowed):
        with transaction.atomic():
            record = self.locked()
            if record.status not in allowed:
                raise ValidationError(
                    f"Care plan cannot move from {record.status} to {target}."
                )
            record.status, record.version = target, record.version + 1
            record.save(update_fields=("status", "version", "updated_at"))
        return Response(self.get_serializer(record).data)

    @action(detail=True, methods=("post",))
    def activate(self, request, pk=None):
        return self._status("active", ("draft",))

    @action(detail=True, methods=("post",))
    def complete(self, request, pk=None):
        return self._status("completed", ("active",))

    @action(detail=True, methods=("post",))
    def cancel(self, request, pk=None):
        return self._status("cancelled", ("draft", "active"))


class ClinicalAlertViewSet(NursingViewSet):
    queryset = ClinicalAlert.objects.select_related("patient", "assigned_nurse")
    serializer_class = ClinicalAlertSerializer

    @action(detail=True, methods=("post",))
    def acknowledge(self, request, pk=None):
        with transaction.atomic():
            record = self.locked()
            if record.status != "open":
                raise ValidationError("Only an open alert can be acknowledged.")
            record.status, record.acknowledged_at, record.acknowledged_by = (
                "acknowledged",
                timezone.now(),
                self.actor(),
            )
            record.save(
                update_fields=(
                    "status",
                    "acknowledged_at",
                    "acknowledged_by",
                    "updated_at",
                )
            )
        return Response(self.get_serializer(record).data)

    @action(detail=True, methods=("post",))
    def escalate(self, request, pk=None):
        with transaction.atomic():
            record = self.locked()
            if record.status not in ("open", "acknowledged"):
                raise ValidationError("This alert cannot be escalated.")
            target = Provider.objects.filter(
                pk=request.data.get("escalated_to"), organization=self.organization()
            ).first()
            if not target:
                raise ValidationError(
                    {"escalated_to": "Select a provider in this organization."}
                )
            record.status, record.escalated_at, record.escalated_to = (
                "escalated",
                timezone.now(),
                target,
            )
            record.save(
                update_fields=("status", "escalated_at", "escalated_to", "updated_at")
            )
        return Response(self.get_serializer(record).data)

    @action(detail=True, methods=("post",))
    def resolve(self, request, pk=None):
        notes = str(request.data.get("resolution_notes", "")).strip()
        if not notes:
            raise ValidationError(
                {"resolution_notes": "Resolution notes are required."}
            )
        with transaction.atomic():
            record = self.locked()
            if record.status == "resolved":
                raise ValidationError("Alert is already resolved.")
            record.status, record.resolved_at, record.resolution_notes = (
                "resolved",
                timezone.now(),
                notes,
            )
            record.save(
                update_fields=(
                    "status",
                    "resolved_at",
                    "resolution_notes",
                    "updated_at",
                )
            )
        return Response(self.get_serializer(record).data)


class NurseScheduleViewSet(NursingViewSet):
    queryset = NurseSchedule.objects.select_related("nurse", "nurse__employee", "ward")
    serializer_class = NurseScheduleSerializer

    def _status(self, target, allowed):
        with transaction.atomic():
            record = self.locked()
            if record.status not in allowed:
                raise ValidationError(
                    f"Shift cannot move from {record.status} to {target}."
                )
            record.status = target
            record.save(update_fields=("status", "updated_at"))
        return Response(self.get_serializer(record).data)

    @action(detail=True, methods=("post",))
    def start(self, request, pk=None):
        return self._status("active", ("scheduled",))

    @action(detail=True, methods=("post",))
    def complete(self, request, pk=None):
        return self._status("completed", ("active",))

    @action(detail=True, methods=("post",))
    def cancel(self, request, pk=None):
        return self._status("cancelled", ("scheduled",))


class ShiftHandoverViewSet(NursingViewSet):
    queryset = ShiftHandover.objects.select_related(
        "schedule",
        "from_nurse",
        "from_nurse__employee",
        "to_nurse",
        "to_nurse__employee",
        "ward",
    ).prefetch_related("patients")
    serializer_class = ShiftHandoverSerializer

    @action(detail=True, methods=("post",))
    def submit(self, request, pk=None):
        with transaction.atomic():
            record = self.locked()
            if record.status != "draft":
                raise ValidationError("Only a draft handover can be submitted.")
            if record.from_nurse_id != self.actor().id:
                raise ValidationError(
                    "Only the outgoing nurse can submit this handover."
                )
            record.status, record.submitted_at = "submitted", timezone.now()
            record.save(update_fields=("status", "submitted_at", "updated_at"))
        return Response(self.get_serializer(record).data)

    @action(detail=True, methods=("post",))
    def accept(self, request, pk=None):
        with transaction.atomic():
            record = self.locked()
            if record.status != "submitted":
                raise ValidationError("Only a submitted handover can be accepted.")
            if record.to_nurse_id != self.actor().id:
                raise ValidationError(
                    "Only the incoming nurse can accept this handover."
                )
            record.status, record.accepted_at = "accepted", timezone.now()
            record.save(update_fields=("status", "accepted_at", "updated_at"))
        return Response(self.get_serializer(record).data)
