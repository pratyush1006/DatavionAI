from rest_framework import serializers

from apps.hr.performance.models import PerformanceReviewCycle

from .fields import (
    REVIEW_CYCLE_DETAIL_FIELDS,
    REVIEW_CYCLE_LIST_FIELDS,
    REVIEW_CYCLE_WRITE_FIELDS,
)


class PerformanceReviewCycleBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReviewCycle
        fields = ()


class PerformanceReviewCycleListSerializer(
    PerformanceReviewCycleBaseSerializer,
):
    class Meta(PerformanceReviewCycleBaseSerializer.Meta):
        fields = REVIEW_CYCLE_LIST_FIELDS
        read_only_fields = REVIEW_CYCLE_LIST_FIELDS


class PerformanceReviewCycleDetailSerializer(
    PerformanceReviewCycleBaseSerializer,
):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="organization.id",
        read_only=True,
    )

    class Meta(PerformanceReviewCycleBaseSerializer.Meta):
        fields = REVIEW_CYCLE_DETAIL_FIELDS
        read_only_fields = REVIEW_CYCLE_DETAIL_FIELDS


class PerformanceReviewCycleCreateSerializer(
    PerformanceReviewCycleBaseSerializer,
):
    class Meta(PerformanceReviewCycleBaseSerializer.Meta):
        fields = REVIEW_CYCLE_WRITE_FIELDS


class PerformanceReviewCycleUpdateSerializer(
    PerformanceReviewCycleBaseSerializer,
):
    class Meta(PerformanceReviewCycleBaseSerializer.Meta):
        fields = REVIEW_CYCLE_WRITE_FIELDS
