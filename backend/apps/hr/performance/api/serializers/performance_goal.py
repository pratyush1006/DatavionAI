from rest_framework import serializers

from apps.hr.performance.models import PerformanceGoal

from .fields import (
    PERFORMANCE_GOAL_FIELDS,
    PERFORMANCE_GOAL_WRITE_FIELDS,
)


class PerformanceGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceGoal
        fields = PERFORMANCE_GOAL_FIELDS
        read_only_fields = PERFORMANCE_GOAL_FIELDS


class PerformanceGoalWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceGoal
        fields = PERFORMANCE_GOAL_WRITE_FIELDS


class PerformanceGoalNestedInputSerializer(serializers.ModelSerializer):
    """
    Used to accept goals nested inside a performance review
    create/update payload, without requiring the parent review
    to be supplied.
    """

    class Meta:
        model = PerformanceGoal
        fields = (
            "title",
            "description",
            "weight",
            "target_date",
            "status",
            "rating",
        )
