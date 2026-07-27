from rest_framework import serializers

from apps.hr.performance.models import PerformanceReview

from .fields import (
    PERFORMANCE_REVIEW_DETAIL_FIELDS,
    PERFORMANCE_REVIEW_LIST_FIELDS,
    PERFORMANCE_REVIEW_WRITE_FIELDS,
)
from .performance_goal import (
    PerformanceGoalNestedInputSerializer,
    PerformanceGoalSerializer,
)


class PerformanceReviewBaseSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = PerformanceReview
        fields = ()

    def get_employee_name(self, obj: PerformanceReview) -> str:
        return obj.employee.full_name


class PerformanceReviewListSerializer(PerformanceReviewBaseSerializer):
    cycle = serializers.CharField(
        source="cycle.name",
        read_only=True,
    )

    employee = serializers.CharField(
        source="employee.employee_code",
        read_only=True,
    )

    reviewer = serializers.SerializerMethodField()

    class Meta(PerformanceReviewBaseSerializer.Meta):
        fields = PERFORMANCE_REVIEW_LIST_FIELDS
        read_only_fields = PERFORMANCE_REVIEW_LIST_FIELDS

    def get_reviewer(self, obj: PerformanceReview):
        return obj.reviewer.full_name if obj.reviewer else None


class PerformanceReviewDetailSerializer(PerformanceReviewBaseSerializer):
    cycle = serializers.CharField(
        source="cycle.name",
        read_only=True,
    )

    cycle_id = serializers.IntegerField(
        source="cycle.id",
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

    reviewer = serializers.SerializerMethodField()

    reviewer_id = serializers.IntegerField(
        source="reviewer.id",
        read_only=True,
    )

    goals = PerformanceGoalSerializer(
        many=True,
        read_only=True,
    )

    class Meta(PerformanceReviewBaseSerializer.Meta):
        fields = PERFORMANCE_REVIEW_DETAIL_FIELDS
        read_only_fields = PERFORMANCE_REVIEW_DETAIL_FIELDS

    def get_reviewer(self, obj: PerformanceReview):
        return obj.reviewer.full_name if obj.reviewer else None


class PerformanceReviewCreateSerializer(PerformanceReviewBaseSerializer):
    goals = PerformanceGoalNestedInputSerializer(
        many=True,
        required=False,
    )

    class Meta(PerformanceReviewBaseSerializer.Meta):
        fields = PERFORMANCE_REVIEW_WRITE_FIELDS


class PerformanceReviewUpdateSerializer(PerformanceReviewBaseSerializer):
    goals = PerformanceGoalNestedInputSerializer(
        many=True,
        required=False,
    )

    class Meta(PerformanceReviewBaseSerializer.Meta):
        fields = PERFORMANCE_REVIEW_WRITE_FIELDS


class PerformanceReviewAcknowledgeSerializer(serializers.Serializer):
    employee_comments = serializers.CharField(
        required=False,
        allow_blank=True,
    )
