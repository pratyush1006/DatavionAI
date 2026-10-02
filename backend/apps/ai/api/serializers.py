"""AI API serializers."""

from __future__ import annotations

from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    application_code = serializers.CharField(max_length=40)
    module_code = serializers.CharField(max_length=120)
    resource_type = serializers.CharField(max_length=120)
    resource_id = serializers.CharField(max_length=160)
    messages = serializers.ListField(child=serializers.DictField(), min_length=1)
    provider = serializers.CharField(max_length=40, required=False, allow_blank=True)
    model = serializers.CharField(max_length=160, required=False, allow_blank=True)
    temperature = serializers.FloatField(default=0.0, min_value=0.0, max_value=2.0)
    max_tokens = serializers.IntegerField(default=2048, min_value=1, max_value=128000)

    def validate_messages(self, value):
        for message in value:
            if message.get("role") not in {"system", "user", "assistant", "tool"}:
                raise serializers.ValidationError("Invalid message role")
            if (
                not isinstance(message.get("content"), str)
                or not message["content"].strip()
            ):
                raise serializers.ValidationError("Message content is required")
        return value


class RAGIndexSerializer(serializers.Serializer):
    knowledge_base_id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    source_uri = serializers.CharField(required=False, allow_blank=True)


class RAGSearchSerializer(serializers.Serializer):
    knowledge_base_id = serializers.UUIDField()
    query = serializers.CharField(min_length=1)
    top_k = serializers.IntegerField(default=5, min_value=1, max_value=50)
