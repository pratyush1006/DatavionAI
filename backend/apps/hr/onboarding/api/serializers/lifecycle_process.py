from rest_framework import serializers

from apps.hr.onboarding.models import LifecycleProcess

from .fields import (
    LIFECYCLE_PROCESS_DETAIL_FIELDS,
    LIFECYCLE_PROCESS_LIST_FIELDS,
    LIFECYCLE_PROCESS_UPDATE_FIELDS,
    LIFECYCLE_PROCESS_WRITE_FIELDS,
)
from .lifecycle_task import LifecycleTaskSerializer


class LifecycleProcessBaseSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    completion_percentage = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = LifecycleProcess
        fields = ()

    def get_employee_name(self, obj: LifecycleProcess) -> str:
        return obj.employee.full_name


class LifecycleProcessListSerializer(LifecycleProcessBaseSerializer):
    employee = serializers.CharField(
        source="employee.employee_code",
        read_only=True,
    )

    class Meta(LifecycleProcessBaseSerializer.Meta):
        fields = LIFECYCLE_PROCESS_LIST_FIELDS
        read_only_fields = LIFECYCLE_PROCESS_LIST_FIELDS


class LifecycleProcessDetailSerializer(LifecycleProcessBaseSerializer):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="organization.id",
        read_only=True,
    )

    employee = serializers.CharField(
        source="employee.employee_code",
        read_only=True,
    )

    employee_id = serializers.IntegerField(
        source="employee.id",
        read_only=True,
    )

    initiated_by = serializers.SerializerMethodField()

    initiated_by_id = serializers.IntegerField(
        source="initiated_by.id",
        read_only=True,
    )

    tasks = LifecycleTaskSerializer(
        many=True,
        read_only=True,
    )

    class Meta(LifecycleProcessBaseSerializer.Meta):
        fields = LIFECYCLE_PROCESS_DETAIL_FIELDS
        read_only_fields = LIFECYCLE_PROCESS_DETAIL_FIELDS

    def get_initiated_by(self, obj: LifecycleProcess):
        return obj.initiated_by.full_name if obj.initiated_by else None


class LifecycleProcessCreateSerializer(LifecycleProcessBaseSerializer):
    class Meta(LifecycleProcessBaseSerializer.Meta):
        fields = LIFECYCLE_PROCESS_WRITE_FIELDS


class LifecycleProcessUpdateSerializer(LifecycleProcessBaseSerializer):
    class Meta(LifecycleProcessBaseSerializer.Meta):
        fields = LIFECYCLE_PROCESS_UPDATE_FIELDS
