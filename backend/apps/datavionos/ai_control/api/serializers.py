from rest_framework import serializers


class AICapabilityToggleSerializer(serializers.Serializer):
    enabled = serializers.BooleanField()
