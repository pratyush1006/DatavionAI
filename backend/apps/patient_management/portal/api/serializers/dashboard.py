"""Read-only response serializers for the patient dashboard."""

from rest_framework import serializers


class PatientDashboardIdentitySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    display_name = serializers.CharField()


class PatientDashboardCountsSerializer(serializers.Serializer):
    upcoming_appointments = serializers.IntegerField(min_value=0)
    active_prescriptions = serializers.IntegerField(min_value=0)
    lab_reports = serializers.IntegerField(min_value=0)
    documents = serializers.IntegerField(min_value=0)


class PatientDashboardAppointmentSerializer(serializers.Serializer):
    provider_name = serializers.CharField()
    scheduled_start = serializers.DateTimeField()
    appointment_type = serializers.CharField()
    status = serializers.CharField()
    is_virtual = serializers.BooleanField()


class PatientDashboardUpdateSerializer(serializers.Serializer):
    id = serializers.CharField()
    category = serializers.CharField()
    title = serializers.CharField()
    occurred_at = serializers.DateTimeField()


class PatientDashboardSerializer(serializers.Serializer):
    patient = PatientDashboardIdentitySerializer()
    counts = PatientDashboardCountsSerializer()
    upcoming_appointment = PatientDashboardAppointmentSerializer(allow_null=True)
    health_updates = PatientDashboardUpdateSerializer(many=True)
