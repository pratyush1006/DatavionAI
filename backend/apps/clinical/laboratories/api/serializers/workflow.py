from rest_framework import serializers


class LaboratoryTestWorkflowDataSerializer(
    serializers.Serializer,
):
    id = serializers.UUIDField()

    status = serializers.CharField()


class LaboratoryTestWorkflowResponseSerializer(
    serializers.Serializer,
):
    success = serializers.BooleanField()

    data = LaboratoryTestWorkflowDataSerializer()
