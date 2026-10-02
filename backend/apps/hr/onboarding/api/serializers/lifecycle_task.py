from rest_framework import serializers

from apps.hr.onboarding.models import LifecycleTask

from .fields import (
    LIFECYCLE_TASK_FIELDS,
    LIFECYCLE_TASK_WRITE_FIELDS,
)


class LifecycleTaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.SerializerMethodField()

    class Meta:
        model = LifecycleTask
        fields = LIFECYCLE_TASK_FIELDS
        read_only_fields = LIFECYCLE_TASK_FIELDS

    def get_assigned_to_name(self, obj: LifecycleTask):
        return obj.assigned_to.full_name if obj.assigned_to else None


class LifecycleTaskWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifecycleTask
        fields = LIFECYCLE_TASK_WRITE_FIELDS
