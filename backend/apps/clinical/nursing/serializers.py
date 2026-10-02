from __future__ import annotations

from rest_framework import serializers

from .models import (
    CarePlan,
    ClinicalAlert,
    MedicationAdministration,
    NurseSchedule,
    NursingTask,
    PatientAssignment,
    ShiftHandover,
)


class ScopedModelSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, attrs):
        organization = getattr(
            self.context["request"], "organization", None
        ) or getattr(self.context["request"], "current_organization", None)
        if not organization:
            raise serializers.ValidationError("Organization context is required.")
        for value in attrs.values():
            related_organization_id = getattr(value, "organization_id", None)
            if related_organization_id and related_organization_id != organization.id:
                raise serializers.ValidationError(
                    "Related records must belong to the current organization."
                )
        return attrs


class PatientAssignmentSerializer(ScopedModelSerializer):
    patient_name = serializers.CharField(source="patient.display_name", read_only=True)
    nurse_name = serializers.CharField(source="nurse.display_name", read_only=True)
    ward_name = serializers.CharField(source="ward.name", read_only=True)

    class Meta:
        model = PatientAssignment
        fields = "__all__"
        read_only_fields = ("status", "ended_at")


class NursingTaskSerializer(ScopedModelSerializer):
    patient_name = serializers.CharField(source="patient.display_name", read_only=True)
    nurse_name = serializers.CharField(
        source="assigned_nurse.display_name", read_only=True
    )

    class Meta:
        model = NursingTask
        fields = "__all__"
        read_only_fields = (
            "status",
            "completed_at",
            "completed_by",
            "completion_notes",
        )


class MedicationAdministrationSerializer(ScopedModelSerializer):
    patient_name = serializers.CharField(source="patient.display_name", read_only=True)
    nurse_name = serializers.CharField(source="nurse.display_name", read_only=True)

    class Meta:
        model = MedicationAdministration
        fields = "__all__"
        read_only_fields = ("status", "administered_at")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        prescription = attrs.get("prescription")
        patient = attrs.get("patient")
        if prescription and patient and prescription.patient_id != patient.id:
            raise serializers.ValidationError(
                {"patient": "Patient must match the prescription."}
            )
        return attrs


class CarePlanSerializer(ScopedModelSerializer):
    patient_name = serializers.CharField(source="patient.display_name", read_only=True)
    nurse_name = serializers.CharField(
        source="primary_nurse.display_name", read_only=True
    )

    class Meta:
        model = CarePlan
        fields = "__all__"
        read_only_fields = ("status", "version")


class ClinicalAlertSerializer(ScopedModelSerializer):
    patient_name = serializers.CharField(source="patient.display_name", read_only=True)

    class Meta:
        model = ClinicalAlert
        fields = "__all__"
        read_only_fields = (
            "status",
            "acknowledged_at",
            "acknowledged_by",
            "escalated_at",
            "resolved_at",
        )


class NurseScheduleSerializer(ScopedModelSerializer):
    nurse_name = serializers.CharField(source="nurse.display_name", read_only=True)
    ward_name = serializers.CharField(source="ward.name", read_only=True)

    class Meta:
        model = NurseSchedule
        fields = "__all__"
        read_only_fields = ("status",)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        starts = attrs.get("starts_at", getattr(self.instance, "starts_at", None))
        ends = attrs.get("ends_at", getattr(self.instance, "ends_at", None))
        if starts and ends and ends <= starts:
            raise serializers.ValidationError(
                {"ends_at": "Shift end must be after its start."}
            )
        nurse = attrs.get("nurse", getattr(self.instance, "nurse", None))
        if (
            nurse
            and starts
            and ends
            and NurseSchedule.objects.filter(
                nurse=nurse, starts_at__lt=ends, ends_at__gt=starts
            )
            .exclude(pk=getattr(self.instance, "pk", None))
            .exclude(status="cancelled")
            .exists()
        ):
            raise serializers.ValidationError(
                "This nurse already has an overlapping shift."
            )
        return attrs


class ShiftHandoverSerializer(ScopedModelSerializer):
    from_nurse_name = serializers.CharField(
        source="from_nurse.display_name", read_only=True
    )
    to_nurse_name = serializers.CharField(
        source="to_nurse.display_name", read_only=True
    )

    class Meta:
        model = ShiftHandover
        fields = "__all__"
        read_only_fields = ("status", "submitted_at", "accepted_at")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get("from_nurse") == attrs.get("to_nurse"):
            raise serializers.ValidationError(
                "Outgoing and incoming nurses must differ."
            )
        schedule, ward = attrs.get("schedule"), attrs.get("ward")
        if schedule and ward and schedule.ward_id != ward.uuid:
            raise serializers.ValidationError(
                {"ward": "Handover ward must match the schedule."}
            )
        organization = getattr(
            self.context["request"], "organization", None
        ) or getattr(self.context["request"], "current_organization", None)
        if any(
            patient.organization_id != organization.id
            for patient in attrs.get("patients", ())
        ):
            raise serializers.ValidationError(
                {"patients": "All patients must belong to the current organization."}
            )
        return attrs
