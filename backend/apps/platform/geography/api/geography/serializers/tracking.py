"""Serializers for Geography live tracking."""

from __future__ import annotations

from rest_framework import serializers


class TrackingSessionCreateSerializer(serializers.Serializer):
    tenant_id = serializers.UUIDField()
    organization_id = serializers.UUIDField(required=False, allow_null=True)
    subject_type = serializers.CharField(max_length=64)
    subject_id = serializers.CharField(max_length=128)
    metadata = serializers.DictField(required=False)


class TrackingParticipantSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    role = serializers.ChoiceField(choices=("updater", "viewer"))


class TrackingSessionSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    tenant_id = serializers.UUIDField()
    organization_id = serializers.UUIDField(allow_null=True)
    subject_type = serializers.CharField()
    subject_id = serializers.CharField()
    status = serializers.CharField()
    created_by_id = serializers.UUIDField()
    started_at = serializers.DateTimeField()
    ended_at = serializers.DateTimeField(allow_null=True)
    last_seen_at = serializers.DateTimeField(allow_null=True)
    last_latitude = serializers.FloatField(allow_null=True)
    last_longitude = serializers.FloatField(allow_null=True)
    last_accuracy_meters = serializers.FloatField(allow_null=True)
    metadata = serializers.DictField()


class TrackingLocationResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    session_id = serializers.UUIDField()
    sequence = serializers.IntegerField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    accuracy_meters = serializers.FloatField(allow_null=True)
    altitude_meters = serializers.FloatField(allow_null=True)
    speed_mps = serializers.FloatField(allow_null=True)
    heading_degrees = serializers.FloatField(allow_null=True)
    recorded_at = serializers.DateTimeField()
    received_at = serializers.DateTimeField()
    source = serializers.CharField()
    metadata = serializers.DictField()
