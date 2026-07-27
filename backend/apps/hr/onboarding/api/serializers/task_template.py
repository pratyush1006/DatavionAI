from rest_framework import serializers

from apps.hr.onboarding.models import LifecycleTaskTemplate

from .fields import (
    TASK_TEMPLATE_DETAIL_FIELDS,
    TASK_TEMPLATE_LIST_FIELDS,
    TASK_TEMPLATE_WRITE_FIELDS,
)


class LifecycleTaskTemplateBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifecycleTaskTemplate
        fields = ()


class LifecycleTaskTemplateListSerializer(
    LifecycleTaskTemplateBaseSerializer,
):
    class Meta(LifecycleTaskTemplateBaseSerializer.Meta):
        fields = TASK_TEMPLATE_LIST_FIELDS
        read_only_fields = TASK_TEMPLATE_LIST_FIELDS


class LifecycleTaskTemplateDetailSerializer(
    LifecycleTaskTemplateBaseSerializer,
):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="organization.id",
        read_only=True,
    )

    class Meta(LifecycleTaskTemplateBaseSerializer.Meta):
        fields = TASK_TEMPLATE_DETAIL_FIELDS
        read_only_fields = TASK_TEMPLATE_DETAIL_FIELDS


class LifecycleTaskTemplateCreateSerializer(
    LifecycleTaskTemplateBaseSerializer,
):
    class Meta(LifecycleTaskTemplateBaseSerializer.Meta):
        fields = TASK_TEMPLATE_WRITE_FIELDS


class LifecycleTaskTemplateUpdateSerializer(
    LifecycleTaskTemplateBaseSerializer,
):
    class Meta(LifecycleTaskTemplateBaseSerializer.Meta):
        fields = TASK_TEMPLATE_WRITE_FIELDS
